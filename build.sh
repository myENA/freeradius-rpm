#!/usr/bin/env bash
set -ex  ## we like things verbose

## ensure we have a full dev stack
sudo yum groupinstall -y "Development Tools"

## install other helpers
sudo yum install -y epel-release mock rpmdevtools rpm-devel

## fetch and install couchbase repo
curl -o /tmp/cb-temp.rpm http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-4-x86_64.rpm
sudo yum install -y /tmp/cb-temp.rpm

## setup our build path
rpmdev-setuptree

## link the specs
ln -sf /tmp/build/SPECS/*.spec $HOME/rpmbuild/SPECS/

## link the sources
find /tmp/build/SOURCES -type f -exec ln -sf {} $HOME/rpmbuild/SOURCES/ \;

## download sources
for spec in $HOME/rpmbuild/SPECS/*.spec; do
    spectool -g -R $spec
done

## install build dependencies
sudo yum-builddep -y $HOME/rpmbuild/SPECS/*.spec

## build packages - disable checking of standard paths
QA_RPATHS=0x0001 rpmbuild -ba $HOME/rpmbuild/SPECS/*.spec

## copy built files out of the vagrant/docker environment
## skip if you are doing this manually
if [ -f /.dockerenv ] || [ -f /.doing_the_vagrant ]; then
    sudo cp -rf $HOME/rpmbuild/RPMS $HOME/rpmbuild/SRPMS /tmp/artifacts/
fi
