#
#!/bin/bash

export PGPASSWORD=postgres
export PAW='$pbkdf2-sha512$25000$vRdijFHKOecc4zwHIASAkA$UqPsZKMLlcQoVPucDI2rC2WKlpjp3AngTX2S5YzgnniWYF2KQPuqWHMkyxelThbq6HxGoq6fW5rfqRwN4cD.CA'

psql -h localhost  --username=auraska postgres -c "create database  $1;" || true
echo "created database $1"

psql -h localhost -vU auraska -d  $1 < /tmp/dump.sql
echo "Done restoring db, finishing up user rights for the new db"

psql  -h localhost  -U auraska -d $1 -c  "grant connect on database $1 to auraska;"
psql  -h localhost  -U auraska -d $1 -c "grant usage on schema public to auraska;"
psql  -h localhost  -U auraska -d $1 -c "grant all privileges on all tables in schema public to auraska;"
psql  -h localhost  -U auraska -d $1 -c "grant all privileges on all sequences in schema public to auraska;"

echo "Updating odoo admin user with password 'admins'"
psql  -h localhost  -U auraska -d $1 -c "update res_users set password='$PAW' where id=2;"
psql  -h localhost  -U auraska -d $1 -c "update ir_config_parameter set value=False where key='auth_signup.reset_password';"
exit
