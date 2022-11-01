#
#!/bin/bash

echo "Enter odoo container name"
read -p "Odoo container name:" odoo_container

echo "Enter db container name"
read -p "Db container name:" db_container

echo "Enter new db name"
read -p "Db name:" db_name

echo "Enter dump zip to restore"
read -p "Dump zip:" dumpfile

# zip_files=()
# for file in $(ls $dumpfile);
# do
#     echo $file
#     zip_files+=($file)
# done
# echo $zip_files
# echo "Select file number to extract from"

unzip $dumpfile -d /tmp/restore

echo "copying files into respective docker containers"
docker cp /tmp/restore/filestore $odoo_container:/var/lib/odoo/
docker cp odoo_container.sh $odoo_container:/tmp

echo "done copying into odoo, moving to db files"

docker cp /tmp/restore/dump.sql $db_container:/tmp/
docker cp db_container.sh  $db_container:/tmp/

echo "removing dump files"
rm -rf /tmp/restore

echo "Going into docker container"
docker exec -itu root $odoo_container sh /tmp/odoo_container.sh $db_name
echo "Finished copying and adjusting file in odoo container"

echo "Entering postgres container to create db and restore your dump"
docker exec -itu root $db_container sh /tmp/db_container.sh $db_name

echo "Finished copying and restoring db in db container"
exit
