############
# BASE STAGE
############

FROM ubuntu:22.04 AS base_stage

ENV DEBIAN_FRONTEND=noninteractive

# TZ will be overwritten by "docker run" to match the host TZ.
# These lines are still needed to create the correct links/files.
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python3.10 and other utilities
RUN apt-get update && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-dev python3.10-venv python3-pip ffmpeg libsm6 libxext6 curl

# clean up apt
RUN rm -rf /var/lib/apt/lists/*

# create python venv and install python utils
RUN python3.10 -m venv /venv
RUN /venv/bin/python -m pip install --no-cache-dir --upgrade pip wheel hatch setuptools

# add python venv to system path
ENV PATH="$PATH:/venv/bin"

# install node and yarn
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" && \
    nvm install 20.13.1 && \
    npm install --global yarn

# add node to system path
ENV PATH="$PATH:/root/.nvm/versions/node/v20.13.1/bin"

####################
# REQUIREMENTS STAGE
####################

FROM base_stage AS requirements_stage

# extract python requirements
COPY pyproject.toml README.md /eyegway/
WORKDIR /eyegway
RUN /venv/bin/hatch dep show requirements -p > /eyegway/requirements.txt

#############
# BUILD STAGE
#############

FROM base_stage AS build_stage

# build eyegway
COPY pyproject.toml README.md /eyegway/
COPY eyegway/ /eyegway/eyegway
WORKDIR /eyegway
RUN /venv/bin/hatch build -t wheel

# build webui
COPY web /web
WORKDIR /web/eyegway-svelte
RUN yarn install && yarn build

##############
# DEPLOY STAGE
##############

FROM base_stage AS deploy_stage

# install python requirements
COPY --from=requirements_stage /eyegway/requirements.txt /tmp/eyegway/
RUN /venv/bin/python -m pip install --no-cache-dir --upgrade \
                     -r /tmp/eyegway/requirements.txt \
                     -f http://wheels.eyecan.ai:8000 \
                     --trusted-host wheels.eyecan.ai:8000

# install eyegway
COPY --from=build_stage /eyegway/dist /tmp/eyegway/
RUN /venv/bin/python -m pip install --no-cache-dir --upgrade "$(find /tmp/eyegway -name *.whl)"

# install webui
COPY --from=build_stage /web /web
RUN rm -r /web/eyegway-svelte/src
