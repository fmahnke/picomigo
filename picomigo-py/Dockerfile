FROM registry.mahnke.tech/dbox/python:latest

# RUN --mount=type=cache,id=pacman-cache,target=/var/cache/pacman,sharing=locked \
#    pacman --noconfirm -Syu \
#    package \

# RUN pacman --noconfirm -Scc

ARG source_name=pico-dev
ARG source_dir=/usr/local/src/$source_name
ARG build_dir=/build

RUN mkdir -p $source_dir && chmod 777 $source_dir
RUN mkdir -p $build_dir && chmod 777 $build_dir

WORKDIR $source_dir

COPY . .

ENV PDM_CACHE_DIR=/var/cache/pdm

RUN --mount=type=cache,id=pdm-cache,target=$PDM_CACHE_DIR,sharing=locked \
    pdm install

ENV PATH="$source_dir/.venv/bin:$PATH"

WORKDIR $build_dir
