#!/bin/bash

python3 get_urls.py > url_test.txt

head -n 10 url_test.txt > 10_urls.txt

python3 get_description.py < 10_urls.txt