本项目基于python+django+uwsgi+mysql+redis技术栈开发

# Getting started

```shell
$ pip install pipreqs
$ pipreqs ./
$ pip install -r requirements.txt
$ pip install django-cors-headers # 由于这个模块没有被直接引入，pipreq无法识别到
$ python manage.py runserver 0.0.0.0:8000
...
Starting development server at http://0.0.0.0:8000/
```

# 使用uwsgi启动服务

```shell
$ uwsgi --ini uwsgi.ini # 请先安装uwsgi
[uWSGI] getting INI configuration from uwsgi.ini
```