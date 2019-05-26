## TOC
* [Overview](#overview-of-scalable-odoo)
* [OS Installation](#os-installation-and-configuration)
  * [Nginx](#nginx)
  * [dehydrated](#dehydrated)
  * [apply/update the certificates to GCP load balancing](#applyupdate-the-certificates-to-gcp-load-balancing)
  * [GCP firewall rule for shutting off HTTP(S) access from everywhere but the load balancing service](#gcp-firewall-rule-for-shutting-off-https-access-from-everywhere-but-the-load-balancing-service)
* [GCP](#gcp)
* [Odoo installation and configuration](#odoo-installation-and-configuration)
  * [security](https://github.com/MRLIVING/odoo#security)
  * [configure outgoing email](#configure-outgoing-email)  
* [Reference](https://github.com/MRLIVING/odoo#reference)  

## Overview of scalable odoo
![](https://drive.google.com/uc?id=1HIilc_Xnc_ct7msmaO6sfdbTZduAX_hN)

## OS installation and configuration 
The following instructions are based on Ubuntu 18.04 LTS.

### time zone and ntp
```
dpkg-reconfigure tzdata
apt-get install ntp
```

### [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/#official-debian-ubuntu-packages)
#### install
```
sudo apt update
sudo apt install nginx
```

#### configuration (/etc/nginx/sites-available/default)
```
if ($http_x_forwarded_proto = "http") {
    return 301 https://$host$request_uri; 
}

...

location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    try_files $uri $uri/ =404;
    
    proxy_set_header   X-Forwarded-For $remote_addr;
    proxy_set_header   Host $http_host;
    proxy_pass         "http://127.0.0.1:8069";
}

# map /var/www/dehydrated/
location /.well-known/acme-challenge/ {
    alias /var/www/dehydrated/;
}
```

### [dehydrated](https://wiki.gslin.org/wiki/Dehydrated) 
#### [install](https://wiki.gslin.org/wiki/Dehydrated#.E5.AE.89.E8.A3.9D)
```
sudo add-apt-repository ppa:gslin/dehydrated-lite
sudo apt update
sudo apt install dehydrated-lite
```

#### configuration
```
sudo mkdir /etc/dehydrated
sudo touch /etc/dehydrated/config
sudo touch /etc/dehydrated/domains.txt
```

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

### [apply/update the certificates to GCP load balancing](https://blog.gcp.expert/gcp-letsencrypt-ssl/) 
* new Frontend IP and port for HTTPS from web UI **at first time**
  * keep the `${target_proxy_name}` (under `Network services/Load balancing/Target-proxies`) as the parameters of the following commands.
  
* create the certificates into `Network services/Load balancing/Certificate` 
```
gcloud compute ssl-certificates create ${cert_name_in_lb}-$(date +%Y%m%d) \
--certificate /etc/dehydrated/certs/${domain_name}/fullchain.pem \
--private-key /etc/dehydrated/certs/${domain_name}/privkey.pem
```

* update SSL cretificates before expiration
```
gcloud compute target-https-proxies update ${target_proxy_name} \
--ssl-certificates ${cert_name_in_lb}-$(date +%Y%m%d)
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

### [num2words](https://pypi.org/project/num2words/)
```
apt-get install python3-pip
pip3 install num2words
```

### [xlrd](https://pypi.org/project/xlrd/)
* enable to import data from Excel file format, i.e. xls
```
pip3 install xlrd
```

### [xlwt](https://pypi.org/project/xlwt/)
* a library for writing data and formatting information to older Excel files (ie: .xls)
```
pip3 install xlwt
```

### Chinese font
* display Chinese char correctly in PDF
```
sudo apt-get install ttf-wqy-zenhei
```

## GCP
### [GCP firewall rule for shutting off HTTP(S) access from everywhere but the load balancing service](https://cloud.google.com/load-balancing/docs/https/cross-region-example#shutting_off_https_access_from_everywhere_but_the_load_balancing_service)
* allows traffic from `130.211.0.0/22` and `35.191.0.0/16` to the odoo instances.
  * [firewall rules for load balancer and the health checker](https://cloud.google.com/load-balancing/docs/https/#firewall_rules)

### [startup script](https://cloud.google.com/compute/docs/startupscript#providing_a_startup_script)
* copy `odoo.conf` from [GCS](https://cloud.google.com/storage) to `/etc/odoo/`
* add cloud SQL Domain-IP mapping to `/etc/hosts`
* `mkdir` and `chmod` odoo `${data_dir}`

## Odoo installation and configuration
* [v12](https://www.odoo.com/documentation/12.0/setup/install.html#repository)
```
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/12.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
apt-get update && apt-get install odoo
```

* [v11](https://www.odoo.com/documentation/11.0/setup/install.html#repository)

### [Security](https://www.odoo.com/documentation/12.0/setup/deploy.html#security)
* `list_db = False` in `odoo.conf`
  * blocking the database selection and management screens.
* always check [Security recommandations](https://www.odoo.com/documentation/12.0/setup/deploy.html#security) if setting up a public server

### Enable Multi-Websites
* Website => Configuration => Settings => Features => Multi-Websites 

### Enable Multi-companies
* Settings => General Settings => Multi-companies => Multi-companies

### Enable Multiple Sales Prices
* Settings => Website => Pricing => Multiple Sales Prices per Product => Prices computed from formulas (discounts, margins, roundings)

### Configure odoo with remote database
* /etc/odoo/odoo.conf  
  As the security issue, don't use `postgre` as the `db_user`.  
  If so, you'll get the error message, e.g. `Using the database user 'postgres' is a security risk, aborting.root@odoo12-prod:/etc/odoo`
  
###   
  
### apps and modules
* Website - website (Technical Name)
* eCommerce - website_sale
* eCommerce Delivery - website_sale_delivery
* Blogs - website_blog
* Website Live Chat - website_livechat
* ~[Website Coupon Code](https://www.odoo.com/apps/modules/12.0/website_coupon/) - website_coupon~
* [Website Coupons & Vouchers](https://apps.odoo.com/apps/modules/12.0/website_voucher/) - coupon & promotion
* Contacts - contacts
* Cancel Journal Entries - account_cancel
* CRM - crm
* Inventory - stock
* Purchase - purchase
* Sales - sale_management
* Expenses - hr_expense
* [om_account_accountant](https://apps.odoo.com/apps/modules/12.0/om_account_accountant/), [如何找回 Odoo 12 的財會功能](https://richsoda.com/blog/odoo-1/post/odoo-12-4)
* [l10n_tw_standard_ifrss-12.0.zip](https://drive.google.com/open?id=1KL8pr_Yna5I7FXHnpIylp_avCVlj81_S)
* [Theme Clarico](https://apps.odoo.com/apps/themes/12.0/theme_clarico/)
  1. copy `emipro_theme_base/` and `theme_clarico/` into addons directory.
  2. restart the odoo server and update "App List"
  3. install `emipro_theme_base`
  4. Website => Configuration => Settings => "CHOOSE THEME"
  5. [change a theme font](https://shop.emiprotechnologies.com/documentation/theme-clarico?version=12#topic1142)
     * [Noto Sans TC
](https://fonts.google.com/specimen/Noto+Sans+TC)
  * [user guide](https://shop.emiprotechnologies.com/documentation/theme-clarico?version=12)

### configure outgoing email
* [use gmail server to send outgoing emails](https://www.odoo.com/documentation/user/12.0/discuss/email_servers.html)
  * [use the Gmail SMTP Server](https://support.google.com/a/answer/176600?hl=en)
    * [let less secure apps access your account](https://support.google.com/accounts/answer/6010255?hl=en)
* [how to Utilize Google’s Free SMTP Server to Send Emails](https://kinsta.com/knowledgebase/free-smtp-server/)

### [sign in with Google account](https://www.odoo.com/documentation/user/12.0/general/auth/google.html)

### User default page after login
* Settings => Users => select an user => Preferences (tab) => Home Action => select a preferred action.

### Product Categories
* Inventory => Configurations => Products => Product Categories 

### Countries and States
* Contacts => Configuration => Localization => Countries => key in "Taiwan" in [Search...] bar ) => States

### [Set Default Country in model](https://www.odoo.com/es_ES/forum/ayuda-1/question/set-default-country-123462#answer_123469)
* set country with python script.


## Reference
* [Deploying Odoo](https://www.odoo.com/documentation/12.0/setup/deploy.html)
* [Certbot - dehydrated](https://github.com/lukas2511/dehydrated)
* [GCP LB with Let’s encrypt and auto renew certificate](https://blog.gcp.expert/gcp-letsencrypt-ssl)
* [redirect HTTP to HTTPS under GCP Load Balancing with NGINX](https://serverfault.com/questions/862725/how-can-you-redirect-http-to-https-gcp-load-balancing#answers-header)
* [How to deploy Odoo 12 on Ubuntu 18.04](https://linuxize.com/post/how-to-deploy-odoo-12-on-ubuntu-18-04/)
  * [Binding a Node.js App to Port 80 with Nginx](https://eladnava.com/binding-nodejs-port-80-using-nginx/)
* [Odoo12 Accounting](https://richsoda.com/blog/odoo-1/post/odoo-12-4?fbclid=IwAR1IupXnkadSyA2cOaZn7cPBRhPdd1ob7MixyOfYzmuJpHRZLAnB81_Brw0)
* [Odoo - Outgoing mail setting](https://www.odoo.com/documentation/user/12.0/discuss/email_servers.html#how-to-use-a-g-suite-server)
* [Odoo - Configuration File](https://vishnuarukat.xyz/articles/odoo9-configuration-files#log)
* [Command-line interface: odoo-bin](https://www.odoo.com/documentation/12.0/reference/cmdline.html)
* [Odoo - How to change the users first page in Odoo community](https://www.targetintegration.com/change-users-first-page-login-odoo-community/)
* [Odoo - How to Create a Module in Odoo 12](https://www.cybrosys.com/blog/how-to-create-module-in-odoo12)
* [Godaddy - types of DNS records](https://www.godaddy.com/garage/dns-records-a-beginners-guide/)
