FROM jenkins/jenkins:lts

USER root

# Create workspace directory with correct permissions
RUN mkdir -p /var/jenkins_home/workspace && \
    chown -R jenkins:jenkins /var/jenkins_home/workspace

# Install Python and Docker
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    python --version

# Docker installation
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli docker-buildx-plugin docker-compose-plugin && \
    apt-get clean

# Add jenkins to docker group
RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins