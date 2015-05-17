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


from fabric.api import execute
from fabric.api import task

import fabfile
from common import enable_services
from common import create_vm, start_vm
import manageiq
import openshift


MANAGEIQ_VM_NAME = 'manageiq01'
OPENSHIFT_VM_NAME = 'openshift01'


@task(name='run-job')
def run_job():
    """
    Container management ci job
    """
    enable_services(['libvirtd'])

    # setup vms
    manageiq_vm = create_vm(MANAGEIQ_VM_NAME)
    openshift_vm = create_vm(OPENSHIFT_VM_NAME)
    execute(start_vm, hosts=[manageiq_vm['ip'], openshift_vm['ip']])
    execute(fabfile.host_init, hosts=[manageiq_vm['ip'], openshift_vm['ip']])

    # deploy
    execute(manageiq.deploy, hosts=manageiq_vm['ip'])
    execute(openshift.deploy, hosts=openshift_vm['ip'])

    # start
    execute(manageiq.start, hosts=manageiq_vm['ip'])
    execute(openshift.start, hosts=openshift_vm['ip'])