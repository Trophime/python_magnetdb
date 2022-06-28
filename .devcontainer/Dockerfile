FROM trophime/magnettools:1.0.6-poetry

USER root
EXPOSE 8000

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Setup demo environment variables
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    OMPI_MCA_btl_vader_single_copy_mechanism=none \
    GOPATH=${HOME}/go \
    PATH=${PATH}:/usr/local/go/bin

# This Dockerfile adds a non-root user with sudo access. Use the "remoteUser"
# property in devcontainer.json to use it. On Linux, the container user's GID/UIDs
# will be updated to match your local UID/GID (when using the dockerFile property).
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=999
ARG USER_GID=$USER_UID

ARG SVERSION=3.7.4
ARG GVERSION=1.14.12
ARG OS=linux
ARG ARCH=amd64
    
# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    # \
    # Verify git, process tools, lsb-release (useful for CLI installs) installed\
    && apt-get -y install git iproute2 procps lsb-release \
    #\
    # Install C++ tools\
    && apt-get -y install curl wget libpq-dev \
    && apt-get -y install build-essential python3-minimal libpython3.8-dev \
    && apt-get -y install python-is-python3 python3-pip python3-jinja2 \
    && apt-get -y install python3-autopep8 black yapf3 python3-bandit flake8 pydocstyle pylint python3-pytest mypy \
    && apt-get -y install texlive-latex-base texlive-latex-extra dvipng \
    && apt-get -y install python3-gmsh \
    && apt-get -y remove pyflakes python-pkg-resources python-pyflakes libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib python2-minimal python2.7 python2.7-minimal \
    && apt-get -y install nmap vim-nox \
    #\
    # install singularity \
    && apt-get install -y  build-essential uuid-dev libgpgme-dev squashfs-tools libseccomp-dev pkg-config cryptsetup-bin \
    && cd /usr/local \
    && wget https://dl.google.com/go/go$GVERSION.$OS-$ARCH.tar.gz \
    && tar -C /usr/local -xzvf go$GVERSION.$OS-$ARCH.tar.gz \
    && rm go$GVERSION.$OS-$ARCH.tar.gz \
    && wget https://github.com/hpcng/singularity/releases/download/v${SVERSION}/singularity-${SVERSION}.tar.gz \
    && tar -xzf singularity-${SVERSION}.tar.gz \
    && rm -f singularity-${SVERSION}.tar.gz \
    && cd singularity \
    && ./mconfig \
    && make -C ./builddir \
    && make -C ./builddir install \
    #\
    # Install frontend stuff \
    && python -m pip install --upgrade pip \
    #\
    # Install node \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install nodejs \
    && curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /usr/share/keyrings/yarnkey.gpg >/dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install yarn \
    && rm -f /tmp/nodejs-install.js \
    # Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.\
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && apt-get install -y sudo \
    && if [ "$(lsb_release -cs)" = "focal" ]; then echo "Set disable_coredump false" > /etc/sudo.conf; fi \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # add github ssh key
    && mkdir ~vscode/.ssh/ \
    && ssh-keyscan github.com >> ~vscode/.ssh/known_hosts \
    && chown -R vscode.$USER_GID ~vscode/.ssh \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

USER $USERNAME
# Install backend stuff for database+api
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - 
# eventually remove poetry.lock

USER root

# Setup demo environment variables
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    OMPI_MCA_btl_vader_single_copy_mechanism=none \
    GOPATH=${HOME}/go \
    PATH=$PATH:${GOPATH}/bin:$HOME/.poetry/bin

