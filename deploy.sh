#!/bin/bash
set -e
cd infra/terraform
terraform init
terraform apply -auto-approve
IP=$(terraform output -raw instance_ip)
echo "Instance IP: $IP"
cd ../ansible
echo "[ai_vm]" > inventory.ini
echo "$IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa" >> inventory.ini
ansible-playbook -i inventory.ini playbook.yml
