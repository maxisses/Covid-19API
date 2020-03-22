# Provisioning with Ansible

The infrastructure can be provisioned using ansible.

## Getting Started
Install ansible on your system. From the project root, go to `./ansible`.
In the command line run
```shell
ansible-playbook playbook.yaml
```
to get everything set up.

You can specify user, remote IP, host-key check, etc. optionally, like this:
```shell
ansible-playbook \
-u <user> \ # modify user
--key-file  ~/.ssh/<key-file>.pem \ # provide SSH key
--ssh-common-args '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null' \ # skip host key checking
-i <inventory-file> \ # use different inventory file
-vvvv \ # very verbose
playbook.yaml 
```

## Test
For testing, within the specific role, execute:
```shell
molecule converge # --debug optionally
```