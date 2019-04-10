## Overview of scalable odoo
![](https://drive.google.com/uc?id=1HIilc_Xnc_ct7msmaO6sfdbTZduAX_hN)

## Installation (based on Ubuntu 18.04 LTS)
### Nginx
```
sudo apt update
sudo apt install nginx
```

### [v12](https://www.odoo.com/documentation/12.0/setup/install.html#repository) or [v11](https://www.odoo.com/documentation/11.0/setup/install.html#repository)
* v12
```
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/12.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
apt-get update && apt-get install odoo
```

* v11
```
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/11.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
apt-get update && apt-get install odoo
```

### [Wkhtmltopdf](https://wkhtmltopdf.org/index.html)
* [Installation for Odoo 11/12 on Ubuntu 18.04](https://medium.com/@hendrasj/install-odoo-12-and-wkhtmltopdf-on-ubuntu-18-04-or-debian-9-160c2e10f123#8fae)
```
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo apt install -f
```
* [compatible version status](https://github.com/odoo/odoo/wiki/Wkhtmltopdf)
* [downloads](https://wkhtmltopdf.org/downloads.html)


## Configure odoo with remote database
* /etc/odoo/odoo.conf  
  As the security issue, don't use `postgre` as the `db_user`.  
  If so, you'll get the error message, e.g. `Using the database user 'postgres' is a security risk, aborting.root@odoo12-prod:/etc/odoo`

## Reference
* [Certbot - dehydrated](https://github.com/lukas2511/dehydrated)
* [GCP LB with Let’s encrypt and auto renew certificate](https://blog.gcp.expert/gcp-letsencrypt-ssl)
* [redirect HTTP to HTTPS under GCP Load Balancing with NGINX](https://serverfault.com/questions/862725/how-can-you-redirect-http-to-https-gcp-load-balancing#answers-header)
* [How to deploy Odoo 12 on Ubuntu 18.04](https://linuxize.com/post/how-to-deploy-odoo-12-on-ubuntu-18-04/)
  * [Binding a Node.js App to Port 80 with Nginx](https://eladnava.com/binding-nodejs-port-80-using-nginx/)
* [Odoo12 Accounting](https://richsoda.com/blog/odoo-1/post/odoo-12-4?fbclid=IwAR1IupXnkadSyA2cOaZn7cPBRhPdd1ob7MixyOfYzmuJpHRZLAnB81_Brw0)
* [Godaddy - types of DNS records](https://www.godaddy.com/garage/dns-records-a-beginners-guide/)
