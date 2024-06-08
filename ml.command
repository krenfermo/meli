#!/bin/sh 

kill -9 $(lsof -ti:8989)
exec /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome   --remote-debugging-port=8989 --user-data-dir=/Users/joaquinpro/Documents/proyectos/meli/chrome
echo "abre chrome"