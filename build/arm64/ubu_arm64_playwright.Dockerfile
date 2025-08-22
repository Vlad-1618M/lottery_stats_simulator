
# _________ Build Args:
ARG PW_VERSION=v1.52.0

# Stage 1: # _________ Playwright | get browsers installed:
FROM mcr.microsoft.com/playwright/python:${PW_VERSION}-jammy AS pw-browsers
ARG PW_VERSION

# _________ Install Python package | pip in base image
RUN pip install --no-cache-dir playwright==${PW_VERSION#v} && \
    playwright install --with-deps chromium firefox webkit

# Stage 2: # _________ Runtime | Ubuntu Jammy + Python 3.13:
FROM ubuntu:22.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# _________ Install Python 3.13 + pip
RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common curl gnupg && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y --no-install-recommends \
        # python3.13 python3.13-dev python3.13-distutils && \
        python3.13 python3.13-dev && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13 && \
    python3.13 -m pip install --no-cache-dir --upgrade setuptools wheel && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1 && \
    update-alternatives --set python3 /usr/bin/python3.13 && \
    rm -rf /var/lib/apt/lists/*

# _________ Copy pre-installed Playwright browsers from Build Stage:
COPY --from=pw-browsers /ms-playwright /ms-playwright

# _________ Runtime dependencies:
RUN apt-get update && apt-get install -y --no-install-recommends \
# RUN apt-get update && apt-get install -y \
        bat make shellcheck jq tree vim iputils-ping cron netcat-openbsd \
        libnss3 libatk1.0-0 libdrm2 libgbm1 libasound2 \
        fonts-liberation fonts-dejavu fonts-unifont \
    && rm -rf /var/lib/apt/lists/*

# _________ Working dir + repo source:
WORKDIR /lotto
COPY . .

# _________ Install Python dependencies:
RUN pip install --no-cache-dir -r deps/requirements.txt && \
    playwright install-deps

# _________ Env Vars:
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PYTHONPATH="/lotto/src"
ENV PATH="/usr/local/go/bin:$PATH"

# _________ Entrypoint:
COPY build/shell_tools/entrypoint.sh /lotto/entrypoint.sh
RUN chmod +x /lotto/entrypoint.sh

RUN python3 --version && python3 -m pip --version
CMD ["/lotto/entrypoint.sh"]
