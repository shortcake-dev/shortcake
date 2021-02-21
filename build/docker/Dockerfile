ARG ARCH_VERSION="base-devel-20210214.0.15477"
ARG BUILD_DATE="2021/02/20"

################################################################################

FROM archlinux:${ARCH_VERSION} AS build-dep

# Reuse argument from previous build scope
ARG BUILD_DATE

# Use Arch archive to freeze packages to a certain date
RUN echo "Server=https://archive.archlinux.org/repos/${BUILD_DATE}/\$repo/os/\$arch" \
        | tee /etc/pacman.d/mirrorlist && \
    pacman -Syyuu --noconfirm

# Install dependencies
RUN pacman --noconfirm -S \
    postgresql \
    python python-pip python-poetry

# Setup poetry
WORKDIR /poetry/
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install -vvv

USER postgres
