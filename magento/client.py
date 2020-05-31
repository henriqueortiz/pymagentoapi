"""
magento.client

Generic Api for Magento
"""

import six
import json
import requests
from magento.utils import camel_2_snake


class ClientApiMeta(type):
    """
    A Metaclass that automatically injects objects that inherit from API
    as properties.
    """

    def __new__(meta, name, bases, dct):
        abstract = dct.get('__abstract__', False)
        Klass = super(ClientApiMeta, meta).__new__(meta, name, bases, dct)

        if not abstract:
            setattr(
                API, camel_2_snake(name),
                property(lambda self: self.get_instance_of(Klass))
            )

        return Klass


@six.add_metaclass(ClientApiMeta)
class Api(object):
    """
    Generic Api to connect Magento rest api
    """

    def __init__(self, domain, integration_token=None, username=None, password=None):
        self.username = username
        self.password = password
        self.domain = domain
        self.search_filters = 'searchCriteria[filter_groups][0][filters][0][field]={}' \
                              '&searchCriteria[filter_groups][0][filters][0][value]={}' \
                              '&searchCriteria[filter_groups][0][filters][0][condition_type]={}'
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        if not integration_token:
            self.token = self.get_admin_token()
        else:
            self.token = integration_token

    def get_admin_token(self):
        url = '{}/rest/V1/integration/admin/token'.format(self.domain)
        credencials = {}
        credencials['username'] = self.username
        credencials['password'] = self.password

        payload = json.dumps(credencials)
        headers = {
            'content-type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text.replace('"', '')