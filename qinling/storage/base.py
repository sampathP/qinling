# Copyright 2017 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import abc

import six
from stevedore import driver

from qinling import exceptions as exc

STORAGE_PROVIDER = None


@six.add_metaclass(abc.ABCMeta)
class PackageStorage(object):
    """PackageStorage interface."""

    @abc.abstractmethod
    def store(self, project_id, funtion, data):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve(self, project_id, function):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, project_id, function):
        raise NotImplementedError


def load_storage_provider(conf):
    global STORAGE_PROVIDER

    if not STORAGE_PROVIDER:
        try:
            mgr = driver.DriverManager(
                'qinling.storage.provider',
                conf.storage.provider,
                invoke_on_load=True,
                invoke_args=[conf]
            )

            STORAGE_PROVIDER = mgr.driver
        except Exception as e:
            raise exc.StorageProviderException(
                'Failed to load storage provider: %s. Error: %s' %
                (conf.storage.provider, str(e))
            )

    return STORAGE_PROVIDER
