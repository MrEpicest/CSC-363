# syntax=docker/dockerfile:1
FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      bc dc \
      python3 python3-venv python3-pip \
      ca-certificates bash \
 && rm -rf /var/lib/apt/lists/*

# Hard fail if tools are missing
RUN command -v bc \
 && command -v dc \
 && dc -e '2 3 + p' | grep -qx '5' \
 && command -v python3

ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} student \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash student

USER student
WORKDIR /work
CMD ["/bin/bash"]
