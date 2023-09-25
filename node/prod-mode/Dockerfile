# syntax=docker.io/docker/dockerfile:1.4
FROM --platform=linux/riscv64 cartesi/python:3.10-slim-jammy as build-stage

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential=12.9ubuntu3 \
    && apt install -y --no-install-recommends curl \
    && rm -rf /var/apt/lists/*

# install rust compiler
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache \
    && find /usr/local/lib -type d -name __pycache__ -exec rm -r {} +

# runtime stage: produces final image that will be executed
FROM --platform=linux/riscv64 cartesi/python:3.10-slim-jammy

COPY --from=build-stage /opt/venv /opt/venv

WORKDIR /opt/cartesi/dapp
COPY ./entrypoint.sh .
COPY ../backend.py .
