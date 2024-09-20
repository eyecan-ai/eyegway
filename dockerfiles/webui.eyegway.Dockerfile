FROM node:21

ADD . /eyegway

WORKDIR /eyegway/web/eyegway-svelte

RUN cd /eyegway/web/eyegway-svelte && yarn install && yarn build
