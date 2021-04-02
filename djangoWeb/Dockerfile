FROM python:3.6-alpine
EXPOSE 8000
COPY . /djangoWeb
WORKDIR /djangoWeb
ENV DJANGOWEBDEBUG=False
RUN apk add gcc libc-dev linux-headers && pip install -r requirements.txt && python manage.py collectstatic
CMD ["uwsgi", "--ini", "uwsgi.ini"]