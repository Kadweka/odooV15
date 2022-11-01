FROM odoo:15.0
USER root
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8

RUN apt-get update

COPY . /mnt/extra-addons
# RUN pip3 install -r . /mnt/requirements.txt
USER odoo
