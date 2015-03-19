#!/usr/bin/env bash

cd /mnt
mkdir -p target
rm -f python-*.deb
/var/lib/gems/1.8/bin/fpm -s python -t deb .
for i in $(cat requirements.txt.freeze); do /var/lib/gems/1.8/bin/fpm -s python -t deb $i; done
ls python-*.deb | xargs mv -t target

