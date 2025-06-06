# Dockerfile
FROM ubuntu:latest

# Install OpenSSH server
RUN apt-get update && apt-get install -y openssh-server sudo net-tools

# Create a user for SSH access (optional, but good practice)
RUN useradd -rm -d /home/sshuser -s /bin/bash -g root -G sudo sshuser
RUN echo 'sshuser:password' | chpasswd # CHANGE 'password' to a strong password

# Allow root login (optional, and generally not recommended for production)
# RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# Configure SSH server
RUN mkdir /var/run/sshd
RUN sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config
# If you want to use public key authentication instead of password
# RUN mkdir /home/sshuser/.ssh && \
#     chmod 700 /home/sshuser/.ssh
# COPY your_public_key.pub /home/sshuser/.ssh/authorized_keys # Place your actual public key here
# RUN chmod 600 /home/sshuser/.ssh/authorized_keys
# RUN chown -R sshuser:sshuser /home/sshuser/.ssh

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]