sudo ln -s /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo rm -rf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -s /home/box/web/etc/gunicorn-wsgi.conf   /etc/gunicorn.d/gunicorn-wsgi
sudo ln -s /home/box/web/etc/gunicorn-django.conf   /etc/gunicorn.d/gunicorn-django
sudo /etc/init.d/gunicorn restart
#sudo /etc/init.d/mysql start
