#!/bin/bash

dropdb capstone_test
createdb capstone_test
psql -U postgres -d capstone_test -f capstone_app/database/capstone.sql
