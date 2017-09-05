a2enmod ssl

mkdir /etc/apache2/ssl
openssl req $@ -new -x509 -days 365 -nodes -out /etc/apache2/ssl/apache.pem -keyout /etc/apache2/ssl/apache.pem
chmod 600 /etc/apache2/ssl/apache.pem


echo '
 <VirtualHost *:443>
  ServerAdmin user@host.com
  DocumentRoot /var/www/html
  SSLEngine on
  SSLCertificateFile /etc/apache2/ssl/apache.pem
								       
  ErrorLog  /home/marc/error.log
  CustomLog /home/marc/access.log combined
 </VirtualHost>
' >>/etc/apache2/sites-enabled/000-default.conf

apachectl configtest
/etc/init.d/apache2 reload
