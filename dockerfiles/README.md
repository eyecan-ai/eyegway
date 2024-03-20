# DOCKERFILES

To build eyegway docker image:

```
docker build -f dockerfiles/Dockerfile_eyegway -t eyegway:latest --add-host wheels.eyecan.ai:192.168.178.23 .
```

To build eyegway webui docker image:

```
docker build -f dockerfiles/Dockerfile_eyegway_webui -t eyegway_webui:latest --build-arg EYEGWAY_HOST=$EYEGWAY_HOST --build-arg WEBUI_TITLE=$WEBUI_TITLE .
```