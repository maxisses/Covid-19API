# Provisioning with Ansible

The infrastructure can be provisioned using ansible.

## Getting Started
Install ansible on your system. From the project root, go to `./ansible`.
In the command line run
```shell
ansible-playbook playbook.yaml
```
to get everything set up. That is:
* create a cron job
* install docker (if not installed)
* install python3 (if not installed) and necessary packages
* run the `flaskAPIwDocker` in a docker container
* Profit! ;)

You can specify user, remote IP, host-key check, etc. optionally, like this:
```shell
ansible-playbook \
-u <user> \ # modify user
--key-file  ~/.ssh/<key-file>.pem \ # provide SSH key
--ssh-common-args '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null' \ # skip host key checking
-i <inventory-file> \ # use different inventory file
-b \ # become
-vvvv \ # very verbose
playbook.yaml 
```

**Note**, that the setup is designed to run on an Ubuntu Linux with user `ubuntu` since ansible tasks
are using apt only (this may change in future versions). The provisioning can easily be adapted by
changing all fields with `CHANGE` mentions.

## Test
For testing, within the specific role, execute:
```shell
molecule converge [--debug]
```

## Example Using AWS EC2 Instance
### Prerequisites
* AWS Account
* ansible is installed on your local system

### Next Steps
* in the AWS console, create an EC2 instance with public IP and SSH keypair
  * copy the private key and change permissions to "read only" (`400`)
  * note the public IP of the EC2 instance 
* modify the `./ansible/inventory` file to use your IP
* from local, run:
```shell script
ansible-playbook \
-u ubuntu \
--key-file <path-to-key-file>.pem \
--ssh-common-args '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null' \
-i <inventory-file> \
-b \
-vvvv \
./ansible/playbook.yaml 
```
* wait a few minutes
After that, you can access the API via `<publicIP>:5000/<endpoint>`, e.g.,
```shell script
curl 35.180.191.100:5000/get_total_cases
```