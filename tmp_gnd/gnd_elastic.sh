#!/bin/bash

# Get Elastic 5 in a container (in userspace with podman)
podman pull docker.elastic.co/elasticsearch/elasticsearch:5.6.16
podman run --name es_five -p 9205:9200  -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xmx1g -Xms1g" elasticsearch:5.6.16

podman start -a es_five

# Get Elastic 7 in a container (in userspace with podman)
podman run --name es_seven -p 9207:9200 -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xmx1g -Xms1g" elasticsearch:7.6.1

podman start -a es_seven
