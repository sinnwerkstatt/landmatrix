#!/bin/bash

podman run --name es_seven -p 9201:9200 -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xmx1g -Xms1g" elasticsearch:7.6.1
podman start -a es_seven

#podman stop es_seven
