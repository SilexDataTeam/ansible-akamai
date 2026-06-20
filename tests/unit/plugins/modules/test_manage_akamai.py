# Copyright: (c) 2024, Silex Data
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)
import json
from unittest.mock import MagicMock, patch

import pytest
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
from ansible_collections.silexdata.akamai.plugins.modules import manage_akamai


class AnsibleExitJson(Exception):
    """Raised by the patched exit_json to halt module execution in tests."""


class AnsibleFailJson(Exception):
    """Raised by the patched fail_json to halt module execution in tests."""


def exit_json(*args, **kwargs):
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


def set_module_args(args):
    """Prepare module arguments the way Ansible would pass them on stdin."""
    serialized = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(serialized)


@pytest.fixture(autouse=True)
def patch_ansible_module(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)


EDGE_AUTH = {
    "host": "akab-example.luna.akamaiapis.net",
    "client_token": "akab-client-token",
    "client_secret": "client-secret",
    "access_token": "akab-access-token",
}


def test_get_request_file_reads_json(tmp_path):
    payload = {"productId": "prd_Alta", "propertyName": "my.new.property.com"}
    body_file = tmp_path / "body.json"
    body_file.write_text(json.dumps(payload))

    assert manage_akamai.get_request_file(str(body_file)) == payload


def test_requires_one_of_edge_config_or_edge_auth():
    """Neither edge_config nor edge_auth -> module must fail."""
    set_module_args({"endpoint": "/siteshield/v1/maps", "method": "GET"})
    with pytest.raises(AnsibleFailJson):
        manage_akamai.main()


def test_edge_config_and_edge_auth_are_mutually_exclusive(tmp_path):
    edgerc = tmp_path / ".edgerc"
    edgerc.write_text("[default]\nhost = example\n")
    set_module_args(
        {
            "endpoint": "/siteshield/v1/maps",
            "method": "GET",
            "edge_config": str(edgerc),
            "edge_auth": EDGE_AUTH,
        }
    )
    with pytest.raises(AnsibleFailJson):
        manage_akamai.main()


@patch.object(manage_akamai, "EdgeGridAuth", create=True)
@patch.object(manage_akamai.requests, "Session")
def test_authenticate_get_success(mock_session_cls, _mock_edgegrid):
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"siteShieldMaps": []}

    session = MagicMock()
    session.get.return_value = response
    mock_session_cls.return_value = session

    params = {
        "endpoint": "/siteshield/v1/maps",
        "method": "GET",
        "section": "default",
        "body": None,
        "headers": None,
        "edge_config": None,
        "edge_auth": EDGE_AUTH,
    }

    is_error, has_changed, result = manage_akamai.authenticate(params)

    assert is_error is False
    assert has_changed is False
    assert result == {"siteShieldMaps": []}
    session.get.assert_called_once()


@patch.object(manage_akamai, "EdgeGridAuth", create=True)
@patch.object(manage_akamai.requests, "Session")
def test_authenticate_get_error_status(mock_session_cls, _mock_edgegrid):
    response = MagicMock()
    response.status_code = 404
    response.json.return_value = {"detail": "not found"}

    session = MagicMock()
    session.get.return_value = response
    mock_session_cls.return_value = session

    params = {
        "endpoint": "/siteshield/v1/maps/does-not-exist",
        "method": "GET",
        "section": "default",
        "body": None,
        "headers": None,
        "edge_config": None,
        "edge_auth": EDGE_AUTH,
    }

    is_error, has_changed, result = manage_akamai.authenticate(params)

    assert is_error is True
    assert has_changed is False
    assert result == {"detail": "not found"}
