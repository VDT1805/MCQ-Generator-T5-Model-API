# FROM alpine:latest
# RUN apk update
# RUN apk add py-pip
# RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade --break-system-packages pip 
# ENV PIP_BREAK_SYSTEM_PACKAGES 1
# WORKDIR /app
# COPY . /app
# RUN pip --no-cache-dir install -r requirements.txt
# CMD ["python3", "app.py"]
# FROM python:3.10
# # Create a new group and user with a home directory
# RUN groupadd -r demouser && useradd -r -m -g demouser demouser

# # Create a new directory and set the necessary permissions
# RUN mkdir /app && chown -R demouser:demouser /app

# # Switch to the new user
# USER demouser

# # Set the working directory
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY --chown=demouser:demouser . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Run app.py when the container launches
# CMD ["python3", "app.py"]
# Use python slim
FROM python:3.10-slim

# Set the working directory within the container
WORKDIR /app

# Copy necessary files to the container
COPY . /app

# Create a virtual environment in the container
RUN python3 -m venv .venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

    # Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt 

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENTRYPOINT [ "python3" ]

# Run app.py when the container launches
CMD [ "app.py" ]