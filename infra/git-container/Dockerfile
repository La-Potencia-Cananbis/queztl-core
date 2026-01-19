# Queztl-Core Git Container
# Self-hosted Git server with web UI and automation
FROM gitea/gitea:1.21

# Install additional tools
USER root
RUN apk add --no-cache \
    git-lfs \
    python3 \
    py3-pip \
    curl \
    bash \
    jq \
    openssh-client

# Install Python tools for automation
RUN pip3 install --no-cache-dir \
    gitpython \
    pygithub \
    requests \
    pyyaml

# Create automation scripts directory
RUN mkdir -p /opt/git-automation

# Copy automation scripts
COPY scripts/ /opt/git-automation/
RUN chmod +x /opt/git-automation/*.sh

# Set up Git hooks directory
RUN mkdir -p /data/gitea/git/hooks

USER git
EXPOSE 3000 22

ENTRYPOINT ["/usr/bin/entrypoint"]
CMD ["/bin/s6-svscan", "/etc/s6"]
