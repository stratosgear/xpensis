FROM elasticsearch:latest

RUN /usr/share/elasticsearch/bin/plugin install mobz/elasticsearch-head
RUN /usr/share/elasticsearch/bin/plugin install delete-by-query
RUN /usr/share/elasticsearch/bin/plugin install lmenezes/elasticsearch-kopf/2.0

#ADD ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
