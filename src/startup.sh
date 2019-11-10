#!/usr/bin/env bash
set -ex

sleep 5
python seed_postgres.py
sleep 5
python seed_mongo.py
sleep 5
python seed_neo4j.py