# Copyright 2018 Zegami Ltd

"""Collection commands."""
import sys
from datetime import datetime

from colorama import Fore, Style

from . import (
    config,
    datasets,
    imagesets,
    http,
)


def get(log, session, args):
    """Get a collection."""
    coll_id = args.id if args.id is not None else ""
    url = "{}collections/{}".format(
        http.get_api_url(args.url, args.project),
        coll_id)
    log.debug('GET: {}'.format(url))
    response_json = http.get(session, url)
    log.print_json(response_json, "collection", "get", shorten=False)


def create(log, session, args):
    """Create a collection."""
    time_start = datetime.now()
    url = "{}collections/".format(
        http.get_api_url(args.url, args.project),)
    log.debug('POST: {}'.format(url))

    # parse config
    configuration = config.parse_args(args, log)
    if "name" not in configuration:
        log.error('Collection name missing from config file')
        sys.exit(1)

    collection_version = configuration.get('collection_version', 1)

    # use name from config
    coll = {
        "name": configuration["name"],
    }
    # use description and enable_clustering from config
    for key in ["description", "enable_clustering", "enable_image_info", "use_wsi"]:
        if key in configuration:
            coll[key] = configuration[key]

    # replace empty description with an empty string
    if 'description' in coll and coll["description"] is None:
        coll["description"] = ''

    # check multiple image sources config
    if collection_version == 2 and 'image_sources' in configuration:
        coll['version'] = 2
        coll['image_sources'] = []
        for source in configuration['image_sources']:
            if "source_name" not in source:
                log.error('Image source name missing from config file')
                sys.exit(1)
            if source['source_name'] is None:
                log.error('Image source name cannot be empty')
                sys.exit(1)
            coll['image_sources'].append({'name': source['source_name']})

    # create the collection
    response_json = http.post_json(session, url, coll)
    log.print_json(response_json, "collection", "post", shorten=False)
    coll = response_json["collection"]

    dataset_config = dict(
        configuration, id=coll["upload_dataset_id"]
    )
    if 'file_config' in dataset_config:
        if 'path' in dataset_config['file_config'] or 'directory' in dataset_config['file_config']:
            datasets.update_from_dict(log, session, dataset_config)

    if collection_version == 2:
        for source in configuration['image_sources']:
            source_name = source['source_name']
            imageset_config = dict(source)
            imageset_config["file_config"] = {}
            for property in ['paths', 'recursive', 'mime_type']:
                if property in source:
                    imageset_config["file_config"][property] = source[property]
            imageset_config["url"] = configuration["url"]
            imageset_config["project"] = configuration["project"]
            imageset_config["dataset_id"] = coll["dataset_id"]
            imageset_config["collection_id"] = coll["id"]
            for coll_source in coll["image_sources"]:
                if coll_source['name'] == source_name:
                    imageset_config["id"] = coll_source["imageset_id"]
            imagesets.update_from_dict(log, session, imageset_config)
    else:
        imageset_config = dict(
            configuration, id=coll["imageset_id"]
        )
        imageset_config["dataset_id"] = coll["dataset_id"]
        imageset_config["collection_id"] = coll["id"]
        imagesets.update_from_dict(log, session, imageset_config)

    delta_time = datetime.now() - time_start
    log.debug("Collection uploaded in {}".format(delta_time))

    return coll


def update(log, session, args):
    """Update a collection."""
    log('colection id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Update collection command coming soon.')


def delete(log, session, args):
    """Delete a collection."""
    url = "{}collections/{}".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('DELETE: {}'.format(url))
    http.delete(session, url)
    log('collection {highlight}{id}{reset} deleted',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)


def init(log, session, args):
    url = "{}collections/".format(
        http.get_api_url(args.url, args.project))
    log.debug('INIT: {}'.format(url))


def publish(log, session, args):
    """Publish a collection."""
    coll_id = args.id if args.id is not None else ""

    # check for config
    if 'config' not in args:
        log.error('Configuration file path missing')
        sys.exit(1)

    configuration = config.parse_config(args.config, log)

    # get publish details
    publish_config = configuration['publish_config']
    if publish_config is None:
        log.error(
            "Missing {highlight}publish_config{reset} parameter".format(
                highlight=Fore.YELLOW,
                reset=Style.RESET_ALL,
            )
        )
        sys.exit(1)

    url = "{}collections/{}/{}".format(
        http.get_api_url(args.url, args.project),
        coll_id,
        'publish' if publish_config['publish'] is True else 'unpublish'
    )
    log.debug('POST: {}'.format(url))

    publish_options = {
        "project": publish_config['destination_project'],
    }

    response_json = http.post_json(session, url, publish_options)
    log.print_json(response_json, "collection", "update", shorten=False)
