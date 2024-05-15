# DOCKERFILES

To build eyegway docker image:

```
docker build -f dockerfiles/Dockerfile_eyegway -t eyegway:latest --add-host wheels.eyecan.ai:192.168.178.23 .
```

To build eyegway webui docker image:

```
docker build -f dockerfiles/Dockerfile_eyegway_webui -t eyegway_webui:latest .
```

To build a single docker with eyegway and eyegway webui:

```
docker build -f dockerfiles/Dockerfile_eyegway_full -t eyegway_full:latest --add-host wheels.eyecan.ai:192.168.178.23 .
```