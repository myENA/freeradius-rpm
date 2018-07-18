# RPM Spec for FreeRADIUS 3.x

RPM build plan for FreeRADIUS in the ENA environment.  The build is based on the [koji](https://koji.fedoraproject.org/koji/) build indicated in the `%changelog` section of the SPEC file.

# Building

The RPMs may be built with [Docker](#with-docker), [Vagrant](#with-vagrant), or [manual](#manual).

Whatever way you choose you will need to do a few basic things first.

```bash
git clone https://github.com/myENA/freeradius-rpm  ## check out this code
cd freeradius-rpm                                  ## uhh... you should know
mkdir -p artifacts                                 ## prep the artifacts location
```

## With Docker

```bash
docker build -t ena/freeradius-rpm .                                 ## build the image
docker run -v $PWD/artifacts:/tmp/artifacts -it ena/freeradius-rpm   ## run the image and build the RPMs
```

## With Vagrant

```bash
vagrant up        ## provision and build the RPMs
```

## Manual

```bash
cat build.sh      ## read the script
```

## Result

Fifteen RPMs will be written to the `artifacts/RPMS/x86_64/` folder:
1. artifacts/RPMS/x86_64/freeradius-3.0.17-0.el7.centos.x86_64.rpm
2. artifacts/RPMS/x86_64/freeradius-couchbase-3.0.17-0.el7.centos.x86_64.rpm
3. artifacts/RPMS/x86_64/freeradius-debuginfo-3.0.17-0.el7.centos.x86_64.rpm
4. artifacts/RPMS/x86_64/freeradius-devel-3.0.17-0.el7.centos.x86_64.rpm
5. artifacts/RPMS/x86_64/freeradius-doc-3.0.17-0.el7.centos.x86_64.rpm
6. artifacts/RPMS/x86_64/freeradius-krb5-3.0.17-0.el7.centos.x86_64.rpm
7. artifacts/RPMS/x86_64/freeradius-ldap-3.0.17-0.el7.centos.x86_64.rpm
8. artifacts/RPMS/x86_64/freeradius-mysql-3.0.17-0.el7.centos.x86_64.rpm
9. artifacts/RPMS/x86_64/freeradius-perl-3.0.17-0.el7.centos.x86_64.rpm
10. artifacts/RPMS/x86_64/freeradius-postgresql-3.0.17-0.el7.centos.x86_64.rpm
11. artifacts/RPMS/x86_64/freeradius-python-3.0.17-0.el7.centos.x86_64.rpm
12. artifacts/RPMS/x86_64/freeradius-rest-3.0.17-0.el7.centos.x86_64.rpm
13. artifacts/RPMS/x86_64/freeradius-sqlite-3.0.17-0.el7.centos.x86_64.rpm
14. artifacts/RPMS/x86_64/freeradius-unixODBC-3.0.17-0.el7.centos.x86_64.rpm
15. artifacts/RPMS/x86_64/freeradius-utils-3.0.17-0.el7.centos.x86_64.rpm

Go forth and get you're RADIUS on!
