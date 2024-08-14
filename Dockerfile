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