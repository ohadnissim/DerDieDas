#!/bin/sh
# Copies the site (the same files GitHub Pages serves) into www/ for the app bundle.
set -e
cd "$(dirname "$0")/.."
rm -rf www && mkdir www
cp ../index.html www/
cp -R ../audio ../img ../data www/
