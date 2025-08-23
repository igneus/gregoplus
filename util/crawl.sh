#!/bin/bash

# Crawl the whole site for broken views

HOME=http://localhost:8000/
DIR=wget_tmp_dir
LOG=wget_crawl.log

# --spider does not save the visited pages, which would be desirable,
# but unfortunately it doesn't keep track of pages already visited
wget --recursive \
     --level=inf \
     --no-verbose \
     --directory-prefix $DIR \
     $HOME \
2>&1 | tee $LOG \
| grep --before-context=1 'ERROR'

echo '------------------'
echo "$(grep ERROR $LOG | wc -l) errors found"
echo "Complete log written to $LOG"

# rm -r $DIR
