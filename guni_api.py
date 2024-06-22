 
###  AGREGAR 
import gunicorn
#import ssl

###

# host y puerto de escucha
bind = '0.0.0.0:9000'
#numero de conexiones maxima en espera de respuesta
backlog = 2048
# Configuracion de los workers
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

#configuración servidor
#servicio
daemon = True
pidfile = './bitacoras/pidAPI'

#logging
errorlog = './bitacoras/errorAPI.log'
loglevel = 'info'
accesslog = './bitacoras/accessAPI.log'
access_log_format = '%(t)s %({x-forwarded-for}i)s %(h)s %({ssl_protocol}x)s %({ssl_cipher}x)s %(T)s \"%(r)s\" %(s)s %(b)s'
 
 
# SSL
#certfile = '/apps/GUNICORN/certificado/server.crt'
#keyfile = '/apps/GUNICORN/certificado/server.key'
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
## COMENTAR Y AGREGAR
#cipher = 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES256-GCM-SHA384'
###

#context.set_ciphers(cipher)
#ssl_context=context

### AGREGAR
gunicorn.SERVER_SOFTWARE = 'WSGI Compatible'
###


 