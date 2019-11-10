FROM python:3.6
WORKDIR /app
COPY . /app
RUN pip install SQLAlchemy pandas psycopg2 mongoengine py2neo 
CMD ["/bin/bash","/app/startup.sh"]