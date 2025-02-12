ARG nodever=22.11.0

FROM node:${nodever} AS build

COPY ./web/eyegway-svelte /opt/eyecan.ai/eyegway-web
WORKDIR /opt/eyecan.ai/eyegway-web
RUN corepack enable && yarn set version stable && yarn install && yarn build

FROM node:${nodever} AS production

WORKDIR /opt/eyecan.ai/eyegway-web
COPY --from=build /opt/eyecan.ai/eyegway-web/build ./build
COPY --from=build /opt/eyecan.ai/eyegway-web/node_modules ./node_modules
COPY --from=build /opt/eyecan.ai/eyegway-web/package.json ./package.json

ENTRYPOINT [ "node" ]
CMD [ "build" ]
