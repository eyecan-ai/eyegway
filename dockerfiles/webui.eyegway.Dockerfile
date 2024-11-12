ARG nodever=22

FROM node:${nodever} AS build

WORKDIR /tmp/eyegway-web-deps
RUN --mount=type=bind,source=./web/eyegway-svelte,target=/tmp/eyegway-web-deps \
    corepack enable && yarn set version stable && yarn install && yarn build

FROM node:${nodever} AS production

WORKDIR /opt/eyecan.ai/eyegway-web
COPY --from=build /tmp/eyegway-web-deps/build ./build
COPY --from=build /tmp/eyegway-web-deps/node_modules ./node_modules
COPY --from=build /tmp/eyegway-web-deps/package.json ./package.json

ENTRYPOINT [ "node" ]
CMD [ "build" ]
