---
title: "AWS lightsail Ubuntu instance hosting wordpress/gitlab"
date: 2025-07-25T03:13:18Z
lastmod: 2025-07-25T13:40:54Z
draft: true
slug: "aws-lightsail-ubuntu-instance-hosting-wordpress-gitlab"
categories: ["Journal"]
author: "Kane"
aliases:
  - /index.php/blog/journal/aws-lightsail-ubuntu-instance-hosting-wordpress-gitlab
joomla_id: 90
---

[Create a lightsail instance](https://docs.aws.amazon.com/lightsail/latest/userguide/getting-started-with-amazon-lightsail.html) for Ubuntu 22. Make sure you have at least 4GB RAM

Attach a static IP to the instance

![static-ip](/images/lightsail-static-ip.png)

Update my Godaddy DNS records to point to Lightsail instance:

![](/images/godaddy-dns-record.png)

Create a new ssh key pair (I used gitbash): `ssh-keygen`. Add the public key to AWS lightsail instance.

Open the ssh console window within AWS lightsail:

![](/images/lightsail-console.png)

[Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) nevermind... I decided to skip terraform for now.

Install nginx, ufw, fail2ban: `sudo apt install nginx ufw fail2ban -y`

Install GitLab:

`curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash`
`sudo EXTERNAL_URL="http://gitlab.humblewizards.com" apt install gitlab-ee`

At this point I slept on it and decided "fuck it gitlab instance is going to cost me $40 per month and I'd rather just put my crap out there in the public".
