 
###  AGREGAR 
import gunicorn
###

# host y puerto de escucha
bind = '0.0.0.0:8000'
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
pidfile = './bitacoras/pid'

#logging
errorlog = './bitacoras/error.log'
loglevel = 'info'
accesslog = './bitacoras/access.log'
access_log_format = '%(t)s %({x-forwarded-for}i)s %(h)s %({ssl_protocol}x)s %({ssl_cipher}x)s %(T)s \"%(r)s\" %(s)s %(b)s'
 
 

### AGREGAR
gunicorn.SERVER_SOFTWARE = 'WSGI Compatible'
###
