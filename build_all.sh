#!/usr/bin/env bash

cd /mnt
dpkg-buildpackage -us -uc -I -i
mkdir target
mv ../pydatacatalog_*.deb target/
