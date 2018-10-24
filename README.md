# HPC-SIG Lab Setup

Infrastructure scripts for the HPC-SIG lab at Linaro.

The repo is split into two main parts: static and dynamic.

## Static

This is the part that will be deployed in the first install of the machines, once they're all provisioned and set.

Dependencies:
 * Real hardware or VMs, doesn't matter
 * All have to have IPs on the same network and root access
 * Ansible installed in a machine with access to all of them
 * Correct configuration on `vars` for your lab

There are four playbooks:
 1. `jenkins.yml`: Installs Jenkins, setup users, LDAP access, permissions, tokens, etc.
 2. `jobs.yml`: Installs the lab's jobs using Jenkins Job Builder
 3. `mrp.yml`: Copies the preseeds needed for the jobs into Mr-Provisioner
 4. `fs.yml`: Prepares the file server's SFTP, cache and web front-end

Both `jenkins` and `fs` playbooks only need to be done once.

The `jobs` playbook needs to be executed every time the jobs or views change (`files/*.yml` or `files/views`).

The `mrp` playbook only need to be executed when the preseeds change (`files/preseeds`).

The root directories: `tasks`, `templates` and `vars` refer to the initial static setup *only*, not the Jobs' roles.

## Dynamic

Once the jobs are installed into Jenkins, they will clone this repository (again) for every job. The branch that gets checked out is controlled by an argument.

So, if the changes are in the jobs' Ansible playbooks (`files/ansible`), then it is not needed to re-run the `jobs.yml` playbook to re-install it.

Furthermore, it is much easier to test the automation if we keep the changes to the Ansible part because:
 1. We don't need to touch the Jenkins server
 2. We can use branches to stage differences and only push to master after validation

If there are steps in the static jobs description that make it hard to stage / automate / move labs, we need to report issues and move them to either the jobs' Ansible playbook or some configuration file that different sites can use locally.
