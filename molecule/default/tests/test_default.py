import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


@pytest.mark.parametrize('service', [
    'pghero-web',
    'pghero-web-1',
])
def test_test_pghero_unit(host, service):
    svc = host.service(service)
    assert svc.is_running
    assert svc.is_enabled


@pytest.mark.parametrize('config, value', [
    ('PORT', '3001'),
    ('DATABASE_URL', 'postgres://bogus:bogus@127.0.0.1/?sslmode=disable'),
    ('PGHERO_USERNAME', 'bogus'),
    ('PGHERO_PASSWORD', 'bogus')
])
def test_pghero_config(host, config, value):
    assert host.check_output("pghero config:get %s" % config) == value
