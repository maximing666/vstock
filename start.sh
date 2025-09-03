#!/bin/bash
apt-get update && apt-get install -y telnet
cd /opt/conda/vstock/ && conda install --file requirements.txt
python manage.py makemigrations
#--fake-initial 检查数据库，如果表已存在且结构与模型匹配，就跳过创建，只标记迁移状态
python manage.py migrate --fake-initial  
python manage.py runserver 0.0.0.0:18001