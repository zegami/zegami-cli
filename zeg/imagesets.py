# Copyright 2018 Zegami Ltd

"""Collection commands."""
import concurrent.futures
import os
import sys
import uuid

from colorama import Fore, Style

from tqdm import tqdm


from . import (
    config,
    http,
)


MIMES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}


def get(log, session, args):
    """Get an image set."""
    log('imageset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('Get imageset command coming soon.')


def update(log, session, args):
    """Update an image set."""
    create_url = "{}imagesets/{}/image_url".format(
        http.get_api_url(args.url, args.project),
        args.id)
    complete_url = "{}imagesets/{}/images".format(
        http.get_api_url(args.url, args.project),
        args.id)
    log.debug('POST: {}'.format(create_url))
    log.debug('POST: {}'.format(complete_url))

    # check for config
    if 'config' not in args:
        log.error('Configuration file path missing')
        sys.exit(1)

    configuration = config.parse_config(args.config)

    # get image paths
    file_config = configuration['file_config']
    if file_config is None:
        log.error(
            "Missing {highlight}paths{reset} parameter".format(
                highlight=Fore.YELLOW,
                reset=Style.RESET_ALL,
            )
        )
        sys.exit(1)
    # check colleciton id, dataset and join column name
    collection_id = configuration['collection_id']
    if collection_id is None:
        log.error(
            "Collection id is missing."
        )
        sys.exit(1)
    dataset_id = configuration['dataset_id']
    if dataset_id is None:
        log.error(
            "Dataset id is missing."
        )
        sys.exit(1)
    dataset_column = configuration['dataset_column']
    if dataset_column is None:
        log.error(
            "Dataset join column is missing."
        )
        sys.exit(1)

    with concurrent.futures.ThreadPoolExecutor(http.CONCURRENCY) as executor:
        paths = _resolve_paths(file_config['paths'])
        futures = [
            executor.submit(
                _upload_image,
                path,
                session,
                create_url,
                complete_url,
                log,
            ) for path in paths
        ]
        kwargs = {
            'total': len(futures),
            'unit': 'image',
            'unit_scale': True,
            'leave': True
        }
        for f in tqdm(concurrent.futures.as_completed(futures), **kwargs):
            pass

    join_url = "{}datasets/".format(
        http.get_api_url(args.url, args.project)
    )
    log.debug('POST: {}'.format(join_url))

    join_data = {
        'name': 'join dataset',
        'source': {
            'imageset_id': args.id,
            'dataset_id': dataset_id,
            'imageset_name_join_to_dataset': {
                'dataset_column': dataset_column,
            },
        },
    }

    # create the join dataset
    join_response = http.post_json(session, join_url, join_data)
    collection_url = "{}collections/{}".format(
        http.get_api_url(args.url, args.project),
        collection_id,
    )
    # update the collection with the new dataset
    log.debug('PUT: {}'.format(collection_url))
    # first need to get the collection object
    collection_response = http.get(session, collection_url)
    collection = collection_response['collection']
    collection['join_dataset_id'] = join_response['dataset']['id']
    http.put_json(session, collection_url, collection)


def delete(log, session, args):
    """Delete an image set."""
    log('imageset id: {highlight}{id}{reset}',
        highlight=Fore.GREEN,
        id=args.id,
        reset=Style.RESET_ALL)
    log.warn('delete imageset command coming soon.')


def _resolve_paths(paths):
    """Resolve all paths to a list of files."""
    allowed_ext = tuple(MIMES.keys())

    resolved = []
    for path in paths:
        if os.path.isdir(path):
            resolved.extend(
                entry.path for entry in os.scandir(path)
                if entry.is_file() and entry.name.lower().endswith(allowed_ext)
            )
        elif os.path.isfile(path) and path.lower().endswith(allowed_ext):
            resolved.append(path)
    return resolved


def _upload_image(path, session, create_url, complete_url, log):
    file_name = os.path.basename(path)
    file_ext = os.path.splitext(path)[-1]
    file_mime = MIMES.get(file_ext, MIMES['.jpg'])

    with open(path, 'rb') as f:
        info = {
            "image": {
                "blob_id": str(uuid.uuid4()),
                "name": file_name,
                "size": os.path.getsize(path),
                "mimetype": file_mime
            }
        }
        try:
            # First create file object
            create = http.post_json(session, create_url, info)
            # Post file to storage location
            url = create["url"]
            if url.startswith("/"):
                url = 'https://storage.googleapis.com{}'.format(url)
            http.put_file(session, url, f, file_mime)
            # confirm
            http.post_json(session, complete_url, info)
        except Exception as ex:
            log.error("Upload failed: {}".format(ex))
