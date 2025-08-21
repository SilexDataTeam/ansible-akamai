#!/usr/bin/env python

from six.moves.urllib.parse import urljoin
from ansible.module_utils.basic import *
import requests
import json

try:
    from akamai.edgegrid import EdgeGridAuth, EdgeRc
except ImportError:
    print("Please install `edgegrid-python` using pip")
from os.path import expanduser

DOCUMENTATION = """
---
module: akamai
short_description: Module to use edgerc auth with Edgegrid to interact with the Akamai API
author:
    - Jacob Hudson (@jacob-hudson)
    - Matt Hyclak (@mhyclak-silex)
version_added: 2.4
description:
    - Interacts with the Akamai API using the Python EdgeGrid library.

options:
    endpoint:
        description:
            - Endpoint of the URL you wish to interact with
        required: true
        type: str
    method:
        description:
            - HTTP method to perform
        required: true
        choices: [GET, PATCH, POST, PUT]
        type: str
    section:
        description:
            - Section of the edgerc file to parse.
        required: false
        default: default
        type: str
    body:
        description:
            - Additional data to submit with the HTTP request
        required: false
        type: str
    headers:
        description:
            - Additional headers to submit with the HTTP request
        required: false
        type: str
    edge_config:
        description:
            - Path to the edgerc file with authentication details
        required: false
        type: str
    edge_auth:
        description:
            - Dictionary containing host, client_token, client_secret and auth_token
        required: false
        type: dict
"""

EXAMPLES = ''' examples '''

def get_request_file(json_file):
    with open(json_file, "r") as j:
        body = json.load(j)

    return body

def authenticate(params):
    s = requests.Session()

    # values from ansible
    endpoint = params["endpoint"]

    if params["edge_config"]:
        if params["edge_config"].startswith('~'):
            # get home location
            home = expanduser("~")
            filename = params["edge_config"].replace('~', home)
        else:
            filename = params["edge_config"]

        # extract edgerc properties
        edgerc = EdgeRc(filename)

        # values from ansible
        section = params["section"]

        # creates baseurl for akamai
        baseurl = 'https://%s' % edgerc.get(section, 'host')
        s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

    if params["edge_auth"]:
        # creates baseurl for akamai
        baseurl = 'https://%s' % params["edge_auth"]['host']
        s.auth = EdgeGridAuth(
            client_token=params["edge_auth"]['client_token'],
            client_secret=params["edge_auth"]['client_secret'],
            access_token=params["edge_auth"]['access_token']
        )

    if params["method"] == "GET":
        response = s.get(urljoin(baseurl, endpoint))
        if response.status_code not in [400, 401, 404]:
            return False, False, response.json()
        else:
            return True, False, response.json()
    elif params["method"] == "PATCH":
        if params["body"] is not None:
            body = get_request_file(params["body"])
            headers = {'content-type': 'application/json'}
            response = s.patch(urljoin(baseurl, endpoint), json=body, headers=headers)
        else:
            headers = {'content-type': 'application/json'}
            response = s.patch(urljoin(baseurl, endpoint), headers=headers)
        if response.status_code not in [400, 401, 404]:
            return False, True, response.json()
        else:
            return True, False, response.json()
    elif params["method"] == "POST":
        if params["body"] is not None:
            body = get_request_file(params["body"])
            headers = {'content-type': 'application/json'}
            response = s.post(urljoin(baseurl, endpoint), json=body, headers=headers)
        else:
            headers = {'content-type': 'application/json'}
            response = s.post(urljoin(baseurl, endpoint), headers=headers)
        if response.status_code not in [400, 401, 404]:
            return False, True, response.json()
        else:
            return True, False, response.json()
    elif params["method"] == "PUT":
        if params["body"] is not None:
            body = get_request_file(params["body"])
            headers = {'content-type': 'application/json'}
            response = s.put(urljoin(baseurl, endpoint), json=body, headers=headers)
        else:
            headers = {'content-type': 'application/json'}
            response = s.put(urljoin(baseurl, endpoint), headers=headers)
        if response.status_code not in [400, 401, 404]:
            return False, True, response.json()
        else:
            return True, False, response.json()
    else:  # error
        pass


def main():
    fields = {
        "section": {"required": False, "type": "str", "default": "default"},
        "endpoint": {"required": True, "type": "str"},
        "method": {"required": True, "type": "str"},
        "body": {"required": False, "type": "str"},
        "headers": {"required": False, "type": "str"},
        "edge_config": {"required": False, "type": "str"},
        "edge_auth": {
            "required": False,
            "type": "dict",
            "options": {
                "host": {"required": True, "type": "str"},
                "client_token": {"required": True, "type": "str"},
                "client_secret": {"required": True, "type": "str"},
                "access_token": {"required": True, "type": "str"}
            }
        }
    }

    required_list = [
        ('edge_config', 'edge_auth'),
    ]

    module = AnsibleModule(argument_spec=fields, mutually_exclusive=required_list, required_one_of=required_list)

    is_error, has_changed, result = authenticate(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, msg=result)
    else:
        module.fail_json(msg=result)

if __name__ == "__main__":
    main()
