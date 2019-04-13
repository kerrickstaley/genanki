FROM ubuntu:bionic as base

# Install as many dependencies as possible before copying the project since
# copying the project may invalidate Docker's image cache, and installing all
# this takes quite a long time.
RUN apt-get update && apt-get install -y \
        curl \
        git \
        make \
        portaudio19-dev \
        python-all-dev \
        python3-pip \
        python3.6 \
        sudo
RUN pip3 install -U \
        cached-property \
        frozendict \
        pystache \
        pyyaml \
        twine \
        virtualenv
RUN curl -fLOsS https://raw.githubusercontent.com/dae/anki/master/requirements.txt && \
        pip3 install -r requirements.txt && \
        rm requirements.txt

# Copy the entire project. This layer will be rebuilt whenever a file has
# changed in the project directory.
COPY . /genanki
WORKDIR /genanki

FROM base AS test
RUN ./setup_tests.sh
RUN ./run_tests.sh
