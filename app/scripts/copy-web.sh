#!/bin/sh
# Copies the site (the same files GitHub Pages serves) into www/ for the app bundle.
set -e
cd "$(dirname "$0")/.."
rm -rf www && mkdir www
cp ../index.html ../phon.js www/   # phon.js: the Aussprache-Helfer, loaded by index.html
cp -R ../audio ../img ../data ../fonts www/
