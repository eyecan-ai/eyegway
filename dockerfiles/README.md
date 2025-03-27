# :whale: Running Eyegway With Docker

Three docker images are provided to run Eyegway with Docker:

```bash
# Eyegway server
docker build -f dockerfiles/server.eyegway.Dockerfile -t eyecan/eyegway:latest .

# Eyegway webui
docker build -f dockerfiles/webui.eyegway.Dockerfile -t eyecan/eyegway-ui:latest .
```

Then, start the server with:

```bash
docker run -d --rm -p 55221:55221 eyecan/eyegway:latest --port 55221

# with 6 workers
docker run -d --rm -p 55221:55221 eyecan/eyegway:latest --port 55221 --workers 6

# with root path /api
docker run -d --rm -p 55221:55221 eyecan/eyegway:latest --port 55221 --root-path /api

# with TLS key and certificate (HTTPS)
# NB: better using secrets for the key and certificate!
docker run -d --rm -p 55221:55221 -v /path/to/key.pem:/key.pem -v /path/to/cert.pem:/cert.pem eyecan/eyegway:latest --port 55221 --ssl-keyfile /key.pem --ssl-certfile /cert.pem
```

And the webui with:

```bash
docker run -d --rm -p 5173:3000 eyecan/eyegway-ui:latest

# with eyegway server at https://my.server.com:10001
docker run -d --rm -p 5173:3000 -e 'PUBLIC_EYEGWAY_HOST=https://my.server.com:10001' eyecan/eyegway-ui:latest
```
