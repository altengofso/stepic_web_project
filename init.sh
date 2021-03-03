sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
sudo pip3 install django==2.0.7
sudo ln -s /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo rm -rf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -s /home/box/web/etc/gunicorn-wsgi.conf   /etc/gunicorn.d/gunicorn-wsgi
sudo ln -s /home/box/web/etc/gunicorn-django.conf   /etc/gunicorn.d/gunicorn-django
sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/mysql start
mysql -uroot -e "create database if not exists ask;"
mysql -uroot -e "grant all privileges on ask.* to 'box'@'localhost';"
mysql -uroot -e "flush privileges;"
~/web/ask/manage.py makemigrations
~/web/ask/manage.py migrate
