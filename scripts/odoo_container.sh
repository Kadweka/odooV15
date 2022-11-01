#
#!/bin/bash

cd /var/lib/odoo/
mv filestore $1/
mkdir filestore && mv $1 filestore/
chown -R odoo.odoo .
echo "$(ls)"
exit
