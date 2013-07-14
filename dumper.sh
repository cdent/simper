#!/bin/sh

# dump the database so we can store it somewhere for later

echo '.dump' | sqlite3 content.db > /tmp/mycontentdb.$$

python butler.py add < /tmp/mycontentdb.$$ || echo "failed to inject datadump"
