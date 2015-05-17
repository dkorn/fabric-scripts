#
# Copyright 2015 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import task


import manageiq


PROVIDER_NAME = 'openshift01'
OPENSHIFT = './_output/local/go/bin/openshift'


@task(name='os-create-example-app')
def create_example_app():
    """creates an example app: 'hello-openshift'"""
    with cd('origin'):
        run('{0} cli create -f '
            'examples/hello-openshift/hello-pod.json'.format(OPENSHIFT))


@task(name='os-create-provider')
def create_openshit_provider():
    """add OpenShift as a provider in ManageIQ"""
    provider_id = manageiq.create_provider(PROVIDER_NAME, env.host)
    manageiq.refresh_provider(provider_id, env.host)
