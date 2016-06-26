FROM python:2.7-alpine
MAINTAINER Stratos Gerakakis <stratosgear@gmail.com>
# http://nickjanetakis.com/blog/alpine-based-docker-images-make-a-difference-in-real-world-apps

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

# ADD ./requirements/prod.txt requirements.txt

ADD . .
RUN apk add --no-cache --virtual .build-deps \
  build-base postgresql-dev libffi-dev nodejs

RUN   npm install -g npm \
    && npm install -g bower
RUN  pip install -r requirements/prod.txt \
    && bower --allow-root install
# RUN find /usr/local \
#         \( -type d -a -name test -o -name tests \) \
#         -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
#         -exec rm -rf '{}' + \
#     && runDeps="$( \
#         scanelf --needed --nobanner --recursive /usr/local \
#                 | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#                 | sort -u \
#                 | xargs -r apk info --installed \
#                 | sort -u \
#     )" \
#     && apk add --virtual .rundeps $runDeps \
#     && apk del .build-deps

# ADD . .

ENV FLASKEXPENSES_ENV prod

COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

EXPOSE 5544

CMD ["/tmp/entrypoint.sh"]
#CMD ["python2 /app/manage.py server"]
