FROM python:3.8

# create and set working directory
RUN mkdir "/performance-storage-service"
WORKDIR "/performance-storage-service"

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV PORT=8080

# Install project dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN groupadd -r django && useradd -r -g django django
COPY . .
RUN chown -R django .

EXPOSE 8080
HEALTHCHECK --interval=10m --timeout=5s\
  CMD curl -f http://localhost:$PORT/performance-results/health/ || exit 1

USER django
CMD gunicorn --bind 0.0.0.0:$PORT pss_project.wsgi:application
