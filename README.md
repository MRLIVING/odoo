## Overview of scalable odoo
![](https://drive.google.com/uc?id=1HIilc_Xnc_ct7msmaO6sfdbTZduAX_hN)

## Installation
### [v11](https://www.odoo.com/documentation/11.0/setup/install.html#repository)


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
