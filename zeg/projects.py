# Copyright 2018 Zegami Ltd

"""Project commands."""
from . import (
    http,
)


def enumerate(log, session, args):
    """Get a list of available workspaces (projects)."""
    url = "{}/oauth/userinfo/".format(
        args.url)
    log.debug('GET: {}'.format(url))
    response_json = http.get(session, url)
    abv_output = {}
    for p in response_json["projects"]:
        abv_output[p['id']] = p['name']
    log.print_json(abv_output, "projects", "list", shorten=False)
