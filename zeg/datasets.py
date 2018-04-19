# Copyright 2018 Zegami Ltd

"""Collection commands."""
import os
import sys
from datetime import datetime
from tempfile import mkstemp

from colorama import Fore, Style

from . import (
    config,
    http,
    sql,
)


MIMES = {
    ".tab": "text/tab-separated-values",
    ".tsv": "text/tab-separated-values",
    ".csv": "text/csv",
    ".xlsx": "application/vnd.openxmlformats-officedocument" +
             ".spreadsheetml.sheet",
}


def get(log, session, args):
    """Get a data set."""
    url = "{}datasets/{}".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('GET: {}'.format(url))
    response_json = http.get(session, url)
    log.print_json(response_json, "dataset", "get")


def update(log, session, args):
    """Update a data set."""
    url = "{}datasets/{}/file/".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('POST: {}'.format(url))

    # check for config
    if 'config' not in args:
        log.error('Configuration file path missing')
        sys.exit(1)

    configuration = config.parse_config(args.config)

    # get update config
    if 'file_config' in configuration:
        (
            file_path,
            file_name,
            file_mime
        ) = _file_type_update(log, configuration['file_config'])
    elif 'sql_config' in configuration:
        (
            file_path,
            file_name,
            file_mime
        ) = _sql_type_update(log, configuration['sql_config'])
    else:
        log.error(
            "Missing {highlight}path{reset} or "
            "{highlight}directory{reset} parameter".format(
                highlight=Fore.YELLOW,
                reset=Style.RESET_ALL,
            )
        )
        sys.exit(1)

    log.debug("File path: {}".format(file_path))
    log.debug("File name: {}".format(file_name))
    log.debug("File mime: {}".format(file_mime))

    with open(file_path) as f:
        response_json = http.post_file(
            session,
            url,
            file_name,
            f,
            file_mime)
        log.print_json(response_json, "dataset", "update")


def delete(log, args):
    """Delete an data set."""
    log('dataset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('delete dataset command coming soon.')


def _file_type_update(log, file_config):
    """Load file and update data set."""
    if 'path' in file_config:
        file_path = file_config['path']
    elif 'directory' in file_config:
        file_path = _get_most_recent_file(file_config['directory'])

    if file_path is None:
        log.error('Data file not found.')
        sys.exit(1)

    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_path)[-1]
    file_mime = MIMES.get(file_ext, MIMES['.csv'])
    return (file_name, file_ext, file_mime)


def _sql_type_update(log, sql_config):
    """Query database and convert to csv file."""
    if 'connection' not in sql_config:
        log.error('Connection string not found.')
        sys.exit(1)
    if 'query' not in sql_config:
        log.error('Query not found.')
        sys.exit(1)
    if not sql.have_driver:
        log.error('No sql driver found, is sqlalchemy installed?')
        sys.exit(1)

    statement = sql.create_statement(sql_config['query'])
    engine = sql.create_engine(sql_config['connection'], log.verbose)
    mime_type = '.csv'
    with engine.connect() as connection:
        result = connection.execute(statement)
        # write to a comma delimited file
        fd, name = mkstemp(suffix=mime_type, prefix='zeg-dataset')
        with open(fd, 'w') as output:
            # write headers
            output.write(str(result.keys())[1:-1] + '\n')
            for row in result:
                row_as_string = [_handle_sql_types(value) for value in row]
                output.write(str(row_as_string)[1:-1] + '\n')
    return (name, mime_type, MIMES[mime_type])


def _handle_sql_types(value):
    """Convert types into Zegami friendly string format."""
    if type(value) is datetime:
        return value.isoformat()
    return str(value)


def _newest_ctime(entry):
    return -entry.stat().st_ctime, entry.name


def _get_most_recent_file(path):
    """Get the most recent file in a directory."""
    allowed_ext = tuple(MIMES.keys())
    files_iter = (
        entry for entry in os.scandir(path)
        if entry.is_file() and entry.name.lower().endswith(allowed_ext)
    )
    for entry in sorted(files_iter, key=_newest_ctime):
        return entry.path
    return None
