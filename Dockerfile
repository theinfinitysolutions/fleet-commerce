# Use the official Python image from the Docker Hub
FROM python:3.10.2-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install the psycopg2 package
RUN pip install psycopg2-binary

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

CMD ["python","manage.py","runserver","0.0.0.0:7007"]
