ARG pyver=3.10
ARG debianver=bookworm

FROM python:${pyver}-${debianver} AS venv_stage

# create a generic virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM venv_stage AS requirements_stage

# install hatch in the virtual environment
RUN pip install --no-cache-dir --upgrade pip wheel hatch

# use hatch to generate requirements.txt
COPY pyproject.toml /opt/eyecan.ai/
WORKDIR /opt/eyecan.ai
RUN hatch dep show requirements -p > requirements.txt

FROM venv_stage AS deps_stage

# copy requirements.txt
COPY --from=requirements_stage /opt/eyecan.ai/requirements.txt /opt/eyecan.ai/

# install dependencies in the virtual environment
WORKDIR /opt/eyecan.ai
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir --upgrade -r requirements.txt

FROM deps_stage AS install_stage

# install the package in the virtual environment of the dependencies
RUN --mount=type=bind,source=.,target=/tmp/eyegway \
    pip install --no-cache-dir --upgrade /tmp/eyegway

FROM python:${pyver}-${debianver} AS deploy_stage

# opencv requirements
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# copy the virtual environment where the wheel is installed
COPY --from=install_stage /opt/venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set the webserver as the entrypoint
ENTRYPOINT [ "uvicorn", "--factory", "eyegway.hubs.rest.api:HubsRestAPI", "--host", "0.0.0.0" ]
