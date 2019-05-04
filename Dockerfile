FROM debian:stretch

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    libreadline-dev \
    libffi-dev \
    git pkg-config

RUN apt-get install -y \
    make \
    unrar-free \
    autoconf \
    automake \
    libtool \
    gcc \
    g++ \
    gperf \
    flex \
    bison \
    texinfo \
    gawk \
    ncurses-dev \
    libexpat-dev \
    python-dev \
    python \
    python-serial \
    sed \
    git \
    unzip \
    bash \
    help2man \
    wget \
    bzip2 \
    libtool-bin \
    python3

RUN useradd -m -s /bin/bash builder

WORKDIR /home/builder
RUN chown -R builder:builder /home/builder

USER builder
RUN git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
RUN cd esp-open-sdk && make
ENV PATH="/home/builder/esp-open-sdk/xtensa-lx106-elf/bin:${PATH}"


RUN git clone --recurse-submodules https://github.com/micropython/micropython.git
#RUN cd ./micropython/ports/esp8266 && \
#    make