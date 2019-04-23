## TOC
* Installation

## Overview of scalable odoo
![](https://drive.google.com/uc?id=1HIilc_Xnc_ct7msmaO6sfdbTZduAX_hN)

## Installation (based on Ubuntu 18.04 LTS)
### [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/#official-debian-ubuntu-packages)
#### install
```
sudo apt update
sudo apt install nginx
```

#### configuration
```
if ($http_x_forwarded_proto = "http") {
    return 301 https://$host$request_uri; 
}
```

### [dehydrated](https://wiki.gslin.org/wiki/Dehydrated) 
#### configuration
/etc/dehydrated/config
```
KEYSIZE=2048
```

/etc/dehydrated/domains.txt
```
${domain_name}
```

#### create ssl certificates
1. accept these terms of service **at first time only**
```
sudo dehydrated --register --accept-terms
```

2. Sign/renew non-existent/changed/expiring certificates
```
sudo dehydrated -c
```

### [apply/update the certificates to GCP Load Balancing](https://blog.gcp.expert/gcp-letsencrypt-ssl/) 
* create the certificates into `Load balancing/Certificate` 
```
gcloud compute ssl-certificates create ${cert_name_in_lb} \
--certificate /etc/dehydrated/certs/${domain_name}/fullchain.pem \
--private-key /etc/dehydrated/certs/${domain_name}/privkey.pem
```
* new Frontend IP and port for HTTPS from web UI **at first time**
  * keep the `${target_proxy_name}` as update parameters 

* update SSL cretificates before expiration
```
gcloud compute target-https-proxies update ${target_proxy_name} \
--ssl-certificates ${cert_name_in_lb}
```

### [GCP firewall rule for shutting off HTTP(S) access from everywhere but the load balancing service](https://cloud.google.com/load-balancing/docs/https/#firewall_rules)
* allows traffic from `130.211.0.0/22` and `35.191.0.0/16` to the odoo instances.

### [Wkhtmltopdf](https://wkhtmltopdf.org/index.html)
* [Installation for Odoo 11/12 on Ubuntu 18.04](https://medium.com/@hendrasj/install-odoo-12-and-wkhtmltopdf-on-ubuntu-18-04-or-debian-9-160c2e10f123#8fae)
```
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo apt install -f
```
* [compatible version status](https://github.com/odoo/odoo/wiki/Wkhtmltopdf)
* [downloads](https://wkhtmltopdf.org/downloads.html)

### num2words
```
apt-get install python3-pip
pip3 install num2words
```

### Odoo
* [v12](https://www.odoo.com/documentation/12.0/setup/install.html#repository)
```
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/12.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
apt-get update && apt-get install odoo
```

* [v11](https://www.odoo.com/documentation/11.0/setup/install.html#repository)
```
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/11.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
apt-get update && apt-get install odoo
```

#### configure odoo with remote database
* /etc/odoo/odoo.conf  
  As the security issue, don't use `postgre` as the `db_user`.  
  If so, you'll get the error message, e.g. `Using the database user 'postgres' is a security risk, aborting.root@odoo12-prod:/etc/odoo`

#### [Theme Clarico](https://apps.odoo.com/apps/themes/12.0/theme_clarico/)
1. copy `emipro_theme_base` and `emipro_theme_base` into addons directory.
2. restart the odoo server and update "App List"
3. install `emipro_theme_base`
4. Website => Configuration => Settings => "CHOOSE THEME"

* [user guide](https://shop.emiprotechnologies.com/documentation/theme-clarico?version=12)

#### configure outgoing email
* [Send email from an app](https://support.google.com/a/answer/176600?hl=en)


## Reference
* [Deploying Odoo](https://www.odoo.com/documentation/12.0/setup/deploy.html)
* [Certbot - dehydrated](https://github.com/lukas2511/dehydrated)
* [GCP LB with Let’s encrypt and auto renew certificate](https://blog.gcp.expert/gcp-letsencrypt-ssl)
* [redirect HTTP to HTTPS under GCP Load Balancing with NGINX](https://serverfault.com/questions/862725/how-can-you-redirect-http-to-https-gcp-load-balancing#answers-header)
* [How to deploy Odoo 12 on Ubuntu 18.04](https://linuxize.com/post/how-to-deploy-odoo-12-on-ubuntu-18-04/)
  * [Binding a Node.js App to Port 80 with Nginx](https://eladnava.com/binding-nodejs-port-80-using-nginx/)
* [Odoo12 Accounting](https://richsoda.com/blog/odoo-1/post/odoo-12-4?fbclid=IwAR1IupXnkadSyA2cOaZn7cPBRhPdd1ob7MixyOfYzmuJpHRZLAnB81_Brw0)
* [Odoo - Outgoing mail setting](https://www.odoo.com/documentation/user/12.0/discuss/email_servers.html#how-to-use-a-g-suite-server)
* [Godaddy - types of DNS records](https://www.godaddy.com/garage/dns-records-a-beginners-guide/)
