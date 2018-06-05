#!/usr/bin/env python3
import jinja2
import os
import sys


class ProvisioningJobMaker(object):
    def __init__(self, working_dirp, machine_list, provisioner_url,
                 provisioner_token):
        self.working_dir = working_dirp
        self.machine_list = machine_list.split(',')
        self.provurl = provisioner_url
        self.token = provisioner_token

    def help(self):
        print('You are using ' + str(len(sys.argv)) + ' args instead of [13,15]')

    def _generateInventory(self, target_ip = '127.0.0.1'):
        inventory= """[localhost]
{{target}}"""

        inventory_template = jinja2.Template(inventory)
        rendered_inventory = inventory_template.render({
            'target': target_ip
        })

        host_file_path = os.path.join(self.working_dir, 'hosts')
        hosts = open(host_file_path, 'w')
        hosts.write(rendered_inventory)
        hosts.close()

    def _generatePlaybook(self, kernel_desc,initrd_desc, preseed_name,
                          preseed_type, machine_arch, machine_subarch,
                          kernel_options = '', kernel_path =
                          '/dev/null', initrd_path = '/dev/null', preseed_path
                         = '/dev/null'):
        playbook="""
{% for machine in machine_list %}
- hosts: localhost
  vars:
          mr_provisioner_machine_name: "{{machine}}"
          mr_provisioner_kernel_description: "{{kdesc}}"
          mr_provisioner_initrd_description: "{{irddesc}}"
          mr_provisioner_kernel_path: "{{kpath}}"
          mr_provisioner_initrd_path: "{{irdpath}}"
          mr_provisioner_kernel_options: "{{kopts}}"
          mr_provisioner_url: "{{provurl}}"
          mr_provisioner_auth_token: "{{provtoken}}"
          mr_provisioner_preseed_name: "{{preseed_name}}"
          mr_provisioner_preseed_type: "{{preseed_type}}"
          mr_provisioner_preseed_path: "{{preseed_path}}"
          mr_provisioner_arch: "{{arch}}"
          mr_provisioner_subarch: "{{subarch}}"
  roles:
          - role: ansible-role-provision-mr-provisioner
{% endfor %}

- hosts: mr_provisioner_hosts
  remote_user: root
  gather_facts: no
  tasks:
      - name: Wait for host for 3600 seconds, but only start checking after 60 seconds
        wait_for_connection:
              delay: 60
              timeout: 3600

      - name: If the host's SSH is up, we can wipe the root password
        shell: 'passwd -l root'"""

        playbook_template = jinja2.Template(playbook)
        rendered_playbook = playbook_template.render({
            'machine_list': self.machine_list,
            'kdesc': kernel_desc,
            'irddesc': initrd_desc,
            'kpath': kernel_path,
            'irdpath': initrd_path,
            'kopts': kernel_options,
            'provurl': self.provurl,
            'provtoken': self.token,
            'preseed_name': preseed_name,
            'preseed_type': preseed_type,
            'preseed_path': preseed_path,
            'arch': machine_arch,
            'subarch': machine_subarch
        })

        name = 'provisioning' + self.machine_list[0] + '.yml'
        file_playbook_path = os.path.join(self.working_dir, name)
        file_playbook = open(file_playbook_path, 'w')
        file_playbook.write(rendered_playbook)
        file_playbook.close()

    def _generateAnsConf(self, host_key_checking = 'False', timeout = '300'):
        conf ="""
[defaults]
host_key_checking = {{host_key_checking}}
timeout = {{timeout}}
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/facts_cache
fact_caching_timeout = 7200


[ssh_connection]
pipelining = False"""
        conf_template = jinja2.Template(conf)
        rendered_conf = conf_template.render({
            'host_key_checking': host_key_checking,
            'timeout': timeout
        })
        file_ansconf_path = os.path.join(self.working_dir, 'ansible.cfg')
        file_ansconf = open(file_ansconf_path, 'w')
        file_ansconf.write(rendered_conf)
        file_ansconf.close()

maker = ProvisioningJobMaker(sys.argv[1], sys.argv[2],
                             sys.argv[3], sys.argv[4])
maker._generateInventory()
maker._generateAnsConf()
if len(sys.argv) == 13:
    maker._generatePlaybook(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8],
                        sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12])
elif len(sys.argv) == 14:
    maker._generatePlaybook(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8],
                        sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12],
                            sys.argv[13])
elif len(sys.argv) == 15:
    maker._generatePlaybook(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8],
                        sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12],
                            sys.argv[13], sys.argv[14])
else:
    maker.help()
