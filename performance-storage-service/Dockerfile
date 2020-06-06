FROM python:3.7

# create and set working directory
RUN mkdir "/performance-storage-service"
WORKDIR "/performance-storage-service"

# Add current directory code to working directory
ADD . "/performance-storage-service/"

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV PORT=8080

# install environment dependencies
RUN pip install --upgrade pip

# Install project dependencies
RUN pip install -r requirements.txt

EXPOSE 8080
CMD gunicorn --bind 0.0.0.0:$PORT pss_project.wsgi:application
