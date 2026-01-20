# QueztlOS Builder Container
# Debian-based environment for building the distro
FROM debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y \
    debootstrap \
    squashfs-tools \
    xorriso \
    isolinux \
    syslinux-common \
    git \
    curl \
    wget \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create build user
RUN useradd -m -s /bin/bash builder && \
    echo "builder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set working directory
WORKDIR /workspace

# Copy repo
COPY . /workspace/

# Set permissions
RUN chown -R builder:builder /workspace

USER builder

CMD ["/bin/bash"]
