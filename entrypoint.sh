#!/usr/bin/bash

celery -A fampay beat -l INFO --detach
celery -A fampay worker -l DEBUG -P threads
kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n'  ' ') > /dev/null 2>&1\n


 celery -A cai_ds_project_rbac worker -B -l INFO -P threads


