# odoo 12
### Configure odoo with remote database
* /etc/odoo/odoo.conf  
  As the security issue, don't use `postgre` as the `db_user`.  
  If so, you'll get the error message, e.g. `Using the database user 'postgres' is a security risk, aborting.root@odoo12-prod:/etc/odoo`

## Reference
* [Certbot - dehydrated](https://github.com/lukas2511/dehydrated)
* [GCP LB with Let’s encrypt and auto renew certificate](https://blog.gcp.expert/gcp-letsencrypt-ssl/#more-49)
