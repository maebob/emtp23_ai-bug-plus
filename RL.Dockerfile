# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install OpenSSH server and any other utilities you may need
RUN apt-get update && apt-get install -y openssh-server

# Configure SSH
RUN echo 'root:your_password' | chpasswd
RUN mkdir -p /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Add the following line to enable password authentication in SSH
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# Expose any other ports you need
EXPOSE 80

# Define environment variable
ENV absolute_project_path /app



# Start the SSH server and your Python script
CMD ["python", "src/agent_ppo/ppo_agent.py"] 
