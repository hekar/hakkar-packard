FROM mcr.microsoft.com/devcontainers/python:1-3.13-bullseye

ENV PYTHONUNBUFFERED 1

# Install necessary packages including database clients
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends curl git unzip postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Install dbmate for database migrations
ADD https://github.com/amacneil/dbmate/releases/download/v1.12.1/dbmate-linux-amd64 /usr/local/bin/dbmate
RUN chmod +x /usr/local/bin/dbmate

# Switch to vscode user for pyenv installation
USER vscode

# Install pyenv
RUN curl https://pyenv.run | bash \
  && echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc \
  && echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

# Install NVM for Node.js version management
RUN export NVM_DIR="$HOME/.nvm" \
  && git clone https://github.com/nvm-sh/nvm.git "$NVM_DIR" \
  && cd "$NVM_DIR" \
  && git checkout "$(git describe --abbrev=0 --tags)" \
  && echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc \
  && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc \
  && echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc

# Switch back to root user
USER root 