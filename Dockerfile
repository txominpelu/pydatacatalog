
FROM debian:squeeze

MAINTAINER Inigo Mediavilla <imediavilla@viadeoteam.com>

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install python python-setuptools ruby-dev gcc rubygems

RUN gem install fpm

# To build the package:  /var/lib/gems/1.8/bin/fpm -s python -t deb .
