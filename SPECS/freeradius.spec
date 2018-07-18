Summary: High-performance and highly configurable free RADIUS server
Name: freeradius
Version: 3.0.17
Release: 0%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Daemons
URL: http://www.freeradius.org/

# Is elliptic curve cryptography supported?
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%global HAVE_EC_CRYPTO 1
%else
%global HAVE_EC_CRYPTO 0
%endif

%global dist_base freeradius-server-%{version}

Source0: ftp://ftp.freeradius.org/pub/radius/%{dist_base}.tar.bz2
Source100: radiusd.service
Source102: freeradius-logrotate
Source103: freeradius-pam-conf
Source104: freeradius-tmpfiles.conf

Patch1: freeradius-Adjust-configuration-to-fit-Red-Hat-specifics.patch
Patch2: freeradius-Use-system-crypto-policy-by-default.patch

%global docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: zlib-devel
BuildRequires: net-snmp-devel
BuildRequires: net-snmp-utils
BuildRequires: readline-devel
BuildRequires: libpcap-devel
BuildRequires: systemd-units
BuildRequires: libtalloc-devel
BuildRequires: pcre-devel

%if ! 0%{?rhel}
BuildRequires: libyubikey-devel
BuildRequires: ykclient-devel
%endif

# Require OpenSSL version we built with, or newer, to avoid startup failures
# due to runtime OpenSSL version checks.
Requires: openssl >= %(rpm -q --queryformat '%%{EPOCH}:%%{VERSION}' openssl)
Requires(pre): shadow-utils glibc-common
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
The FreeRADIUS Server Project is a high performance and highly configurable
GPL'd free RADIUS server. The server is similar in some respects to
Livingston's 2.0 server.  While FreeRADIUS started as a variant of the
Cistron RADIUS server, they don't share a lot in common any more. It now has
many more features than Cistron or Livingston, and is much more configurable.

FreeRADIUS is an Internet authentication daemon, which implements the RADIUS
protocol, as defined in RFC 2865 (and others). It allows Network Access
Servers (NAS boxes) to perform authentication for dial-up users. There are
also RADIUS clients available for Web servers, firewalls, Unix logins, and
more.  Using RADIUS allows authentication and authorization for a network to
be centralized, and minimizes the amount of re-configuration which has to be
done when adding or deleting new users.

%package doc
Group: Documentation
Summary: FreeRADIUS documentation

%description doc
All documentation supplied by the FreeRADIUS project is included
in this package.

%package utils
Group: System Environment/Daemons
Summary: FreeRADIUS utilities
Requires: %{name} = %{version}-%{release}
Requires: libpcap >= 0.9.4

%description utils
The FreeRADIUS server has a number of features found in other servers,
and additional features not found in any other server. Rather than
doing a feature by feature comparison, we will simply list the features
of the server, and let you decide if they satisfy your needs.

Support for RFC and VSA Attributes Additional server configuration
attributes Selecting a particular configuration Authentication methods

%package devel
Group: System Environment/Daemons
Summary: FreeRADIUS development files
Requires: %{name} = %{version}-%{release}

%description devel
Development headers and libraries for FreeRADIUS.

%package ldap
Summary: LDAP support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: openldap-devel

%description ldap
This plugin provides the LDAP support for the FreeRADIUS server project.

%package krb5
Summary: Kerberos 5 support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: krb5-devel

%description krb5
This plugin provides the Kerberos 5 support for the FreeRADIUS server project.

%package perl
Summary: Perl support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%{?fedora:BuildRequires: perl-devel}
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::Embed)

%description perl
This plugin provides the Perl support for the FreeRADIUS server project.

%package python
Summary: Python support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: python-devel

%description python
This plugin provides the Python support for the FreeRADIUS server project.

%package mysql
Summary: MySQL support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: mysql-devel

%description mysql
This plugin provides the MySQL support for the FreeRADIUS server project.

%package postgresql
Summary: Postgresql support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: postgresql-devel

%description postgresql
This plugin provides the postgresql support for the FreeRADIUS server project.

%package sqlite
Summary: SQLite support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: sqlite-devel

%description sqlite
This plugin provides the SQLite support for the FreeRADIUS server project.

%package unixODBC
Summary: Unix ODBC support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: unixODBC-devel

%description unixODBC
This plugin provides the unixODBC support for the FreeRADIUS server project.

%package rest
Summary: REST support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: libcurl-devel
BuildRequires: json-c-devel

%description rest
This plugin provides the REST support for the FreeRADIUS server project.

%package couchbase
Summary: Couchbase support for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildRequires: libcouchbase-devel
BuildRequires: json-c-devel 

%description couchbase
This plugin provides the Couchbase support for the FreeRADIUS server project.

%prep
%setup -q -n %{dist_base}
# Note: We explicitly do not make patch backup files because 'make install'
# mistakenly includes the backup files, especially problematic for raddb config files.
patch -p1 --no-backup-if-mismatch --fuzz=0 < %{PATCH1}
patch -p1 --no-backup-if-mismatch --fuzz=0 < %{PATCH2}

## enable rlm_couchbase
echo rlm_couchbase >> src/modules/stable

%build
# Force compile/link options, extra security for network facing daemon
%global _hardened_build 1

%configure \
        --libdir=%{_libdir}/freeradius \
        --disable-openssl-version-check \
        --with-udpfromto \
        --with-threads \
        --with-docdir=%{docdir} \
        --with-rlm-sql_postgresql-include-dir=/usr/include/pgsql \
        --with-rlm-sql-postgresql-lib-dir=%{_libdir} \
        --with-rlm-sql_mysql-include-dir=/usr/include/mysql \
        --with-mysql-lib-dir=%{_libdir}/mysql \
        --with-unixodbc-lib-dir=%{_libdir} \
        --with-rlm-dbm-lib-dir=%{_libdir} \
        --with-rlm-krb5-include-dir=/usr/kerberos/include \
        --without-rlm_eap_ikev2 \
        --without-rlm_eap_tnc \
        --without-rlm_sql_iodbc \
        --without-rlm_sql_firebird \
        --without-rlm_sql_db2 \
        --without-rlm_sql_oracle \
        --without-rlm_unbound \
        --without-rlm_redis \
        --without-rlm_rediswho \
        --without-rlm_cache_memcached

make

%install
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/radiusd
make install R=$RPM_BUILD_ROOT

# logs
mkdir -p $RPM_BUILD_ROOT/var/log/radius/radacct
touch $RPM_BUILD_ROOT/var/log/radius/{radutmp,radius.log}

install -D -m 644 %{SOURCE100} $RPM_BUILD_ROOT/%{_unitdir}/radiusd.service
install -D -m 644 %{SOURCE102} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/radiusd
install -D -m 644 %{SOURCE103} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/radiusd

mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}%{_localstatedir}/run/radiusd/
install -d -m 0700 %{buildroot}%{_localstatedir}/run/radiusd/tmp
install -m 0644 %{SOURCE104} %{buildroot}%{_tmpfilesdir}/radiusd.conf

# install SNMP MIB files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/
install -m 644 mibs/*RADIUS*.mib $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/

# remove unneeded stuff
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.crt
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.csr
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.der
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.key
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.pem
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.p12
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/index.*
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/serial*
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/dh
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/random

rm -f $RPM_BUILD_ROOT/usr/sbin/rc.radiusd
rm -f $RPM_BUILD_ROOT/usr/bin/rbmonkey
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.la

rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/main/mssql

rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/ippool/oracle
rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/ippool-dhcp/oracle
rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/main/oracle
rm -r $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/moonshot-targeted-ids

rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/unbound
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-config/unbound/default.conf
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/redis*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/abfab*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/moonshot-targeted-ids
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/policy.d/abfab*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/policy.d/moonshot-targeted-ids
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/sites-available/abfab*

rm $RPM_BUILD_ROOT/%{_libdir}/freeradius/rlm_test.so

# remove unsupported config files
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/experimental.conf

# install doc files omitted by standard install
for f in COPYRIGHT CREDITS INSTALL.rst README.rst VERSION; do
    cp $f $RPM_BUILD_ROOT/%{docdir}
done
cp LICENSE $RPM_BUILD_ROOT/%{docdir}/LICENSE.gpl
cp src/lib/LICENSE $RPM_BUILD_ROOT/%{docdir}/LICENSE.lgpl
cp src/LICENSE.openssl $RPM_BUILD_ROOT/%{docdir}/LICENSE.openssl

# add Red Hat specific documentation
cat >> $RPM_BUILD_ROOT/%{docdir}/REDHAT << EOF

Red Hat, RHEL, Fedora, and CentOS specific information can be found on the
FreeRADIUS Wiki in the Red Hat FAQ.

http://wiki.freeradius.org/guide/Red-Hat-FAQ

Please reference that document.

All documentation is in the freeradius-doc sub-package.

EOF


# Make sure our user/group is present prior to any package or subpackage installation
%pre
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd > /dev/null 2>&1
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -d %{_localstatedir}/lib/radiusd -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%post
%systemd_post radiusd.service
if [ $1 -eq 1 ]; then           # install
  # Initial installation
  if [ ! -e /etc/raddb/certs/server.pem ]; then
    /sbin/runuser -g radiusd -c 'umask 007; /etc/raddb/certs/bootstrap' > /dev/null 2>&1
  fi
fi
exit 0

%preun
%systemd_preun radiusd.service

%postun
%systemd_postun_with_restart radiusd.service
if [ $1 -eq 0 ]; then           # uninstall
  getent passwd radiusd >/dev/null && /usr/sbin/userdel  radiusd > /dev/null 2>&1
  getent group  radiusd >/dev/null && /usr/sbin/groupdel radiusd > /dev/null 2>&1
fi
exit 0

/bin/systemctl try-restart radiusd.service >/dev/null 2>&1 || :


%files
%defattr(-,root,root)

# doc
%license %{docdir}/LICENSE.gpl
%license %{docdir}/LICENSE.lgpl
%license %{docdir}/LICENSE.openssl
%doc %{docdir}/REDHAT

# system
%config(noreplace) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %{_sysconfdir}/logrotate.d/radiusd
%{_unitdir}/radiusd.service
%{_tmpfilesdir}/radiusd.conf
%dir %attr(710,radiusd,radiusd) %{_localstatedir}/run/radiusd
%dir %attr(700,radiusd,radiusd) %{_localstatedir}/run/radiusd/tmp
%dir %attr(755,radiusd,radiusd) %{_localstatedir}/lib/radiusd

# configs (raddb)
%dir %attr(755,root,radiusd) /etc/raddb
%defattr(-,root,radiusd)
/etc/raddb/README.rst
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/panic.gdb

%attr(644,root,radiusd) %config(noreplace) /etc/raddb/dictionary
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/clients.conf

%attr(640,root,radiusd) %config(noreplace) /etc/raddb/templates.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/trigger.conf

# symlink: /etc/raddb/hints -> ./mods-config/preprocess/hints
%config /etc/raddb/hints

# symlink: /etc/raddb/huntgroups -> ./mods-config/preprocess/huntgroups
%config /etc/raddb/huntgroups

%attr(640,root,radiusd) %config(noreplace) /etc/raddb/proxy.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/radiusd.conf

# symlink: /etc/raddb/users -> ./mods-config/files/authorize
%config(noreplace) /etc/raddb/users

# certs
%dir %attr(770,root,radiusd) /etc/raddb/certs
%config(noreplace) /etc/raddb/certs/Makefile
%config(noreplace) /etc/raddb/certs/passwords.mk
/etc/raddb/certs/README
%config(noreplace) /etc/raddb/certs/xpextensions
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/certs/*.cnf
%attr(750,root,radiusd) /etc/raddb/certs/bootstrap

# mods-config
%dir %attr(750,root,radiusd) /etc/raddb/mods-config
/etc/raddb/mods-config/README.rst
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/attr_filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/attr_filter/*
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/files
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/files/*
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/preprocess
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/preprocess/*

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main

# sites-available
%dir %attr(750,root,radiusd) /etc/raddb/sites-available
/etc/raddb/sites-available/README
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/control-socket
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/decoupled-accounting
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/robust-proxy-accounting
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/soh
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/coa
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/example
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/inner-tunnel
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/dhcp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/check-eap-tls
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/status
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/dhcp.relay
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/virtual.example.com
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/originate-coa
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/vmps
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/default
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/proxy-inner-tunnel
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/dynamic-clients
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/copy-acct-to-home-server
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/buffered-sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/tls
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/channel_bindings
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/challenge

# sites-enabled
# symlink: /etc/raddb/sites-enabled/xxx -> ../sites-available/xxx
%dir %attr(750,root,radiusd) /etc/raddb/sites-enabled
%config(missingok) /etc/raddb/sites-enabled/inner-tunnel
%config(missingok) /etc/raddb/sites-enabled/default

# mods-available
%dir %attr(750,root,radiusd) /etc/raddb/mods-available
/etc/raddb/mods-available/README.rst
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/always
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/attr_filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/cache
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/cache_eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/chap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/counter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/cui
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/date
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/detail
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/detail.example.com
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/detail.log
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp_sqlippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/digest
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dynamic_clients
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/echo
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/etc_group
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/exec
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/expiration
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/expr
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/files
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/idn
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/inner-eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/linelog
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/logintime
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/mac2ip
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/mac2vlan
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/mschap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ntlm_auth
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/opendirectory
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/otp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/pam
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/pap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/passwd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/preprocess
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/python
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/radutmp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/realm
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/replicate
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/smbpasswd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/smsotp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/soh
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sometimes
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sqlcounter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sqlippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sradutmp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/unix
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/unpack
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/utf8
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/wimax
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/yubikey

# mods-enabled
# symlink: /etc/raddb/mods-enabled/xxx -> ../mods-available/xxx
%dir %attr(750,root,radiusd) /etc/raddb/mods-enabled
%config(missingok) /etc/raddb/mods-enabled/always
%config(missingok) /etc/raddb/mods-enabled/attr_filter
%config(missingok) /etc/raddb/mods-enabled/cache_eap
%config(missingok) /etc/raddb/mods-enabled/chap
%config(missingok) /etc/raddb/mods-enabled/date
%config(missingok) /etc/raddb/mods-enabled/detail
%config(missingok) /etc/raddb/mods-enabled/detail.log
%config(missingok) /etc/raddb/mods-enabled/digest
%config(missingok) /etc/raddb/mods-enabled/dynamic_clients
%config(missingok) /etc/raddb/mods-enabled/eap
%config(missingok) /etc/raddb/mods-enabled/echo
%config(missingok) /etc/raddb/mods-enabled/exec
%config(missingok) /etc/raddb/mods-enabled/expiration
%config(missingok) /etc/raddb/mods-enabled/expr
%config(missingok) /etc/raddb/mods-enabled/files
%config(missingok) /etc/raddb/mods-enabled/linelog
%config(missingok) /etc/raddb/mods-enabled/logintime
%config(missingok) /etc/raddb/mods-enabled/mschap
%config(missingok) /etc/raddb/mods-enabled/ntlm_auth
%config(missingok) /etc/raddb/mods-enabled/pap
%config(missingok) /etc/raddb/mods-enabled/passwd
%config(missingok) /etc/raddb/mods-enabled/preprocess
%config(missingok) /etc/raddb/mods-enabled/radutmp
%config(missingok) /etc/raddb/mods-enabled/realm
%config(missingok) /etc/raddb/mods-enabled/replicate
%config(missingok) /etc/raddb/mods-enabled/soh
%config(missingok) /etc/raddb/mods-enabled/sradutmp
%config(missingok) /etc/raddb/mods-enabled/unix
%config(missingok) /etc/raddb/mods-enabled/unpack
%config(missingok) /etc/raddb/mods-enabled/utf8

# policy
%dir %attr(750,root,radiusd) /etc/raddb/policy.d
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/accounting
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/canonicalization
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/control
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/cui
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/debug
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/dhcp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/operator-name


# binaries
%defattr(-,root,root)
/usr/sbin/checkrad
/usr/sbin/raddebug
/usr/sbin/radiusd
/usr/sbin/radmin

# dictionaries
%dir %attr(755,root,root) /usr/share/freeradius
/usr/share/freeradius/*

# logs
%dir %attr(700,radiusd,radiusd) /var/log/radius/
%dir %attr(700,radiusd,radiusd) /var/log/radius/radacct/
%ghost %attr(644,radiusd,radiusd) /var/log/radius/radutmp
%ghost %attr(600,radiusd,radiusd) /var/log/radius/radius.log

# libs
%attr(755,root,root) %{_libdir}/freeradius/lib*.so*

# loadable modules
%dir %attr(755,root,root) %{_libdir}/freeradius
%{_libdir}/freeradius/proto_dhcp.so
%{_libdir}/freeradius/proto_vmps.so
%{_libdir}/freeradius/rlm_always.so
%{_libdir}/freeradius/rlm_attr_filter.so
%{_libdir}/freeradius/rlm_cache.so
%{_libdir}/freeradius/rlm_cache_rbtree.so
%{_libdir}/freeradius/rlm_chap.so
%{_libdir}/freeradius/rlm_counter.so
%{_libdir}/freeradius/rlm_cram.so
%{_libdir}/freeradius/rlm_date.so
%{_libdir}/freeradius/rlm_detail.so
%{_libdir}/freeradius/rlm_dhcp.so
%{_libdir}/freeradius/rlm_digest.so
%{_libdir}/freeradius/rlm_dynamic_clients.so
%{_libdir}/freeradius/rlm_eap.so
%{_libdir}/freeradius/rlm_eap_fast.so
%{_libdir}/freeradius/rlm_eap_gtc.so
%{_libdir}/freeradius/rlm_eap_leap.so
%{_libdir}/freeradius/rlm_eap_md5.so
%{_libdir}/freeradius/rlm_eap_mschapv2.so
%{_libdir}/freeradius/rlm_eap_peap.so
%if %{HAVE_EC_CRYPTO}
%{_libdir}/freeradius/rlm_eap_pwd.so
%endif
%{_libdir}/freeradius/rlm_eap_sim.so
%{_libdir}/freeradius/rlm_eap_tls.so
%{_libdir}/freeradius/rlm_eap_ttls.so
%{_libdir}/freeradius/rlm_exec.so
%{_libdir}/freeradius/rlm_expiration.so
%{_libdir}/freeradius/rlm_expr.so
%{_libdir}/freeradius/rlm_files.so
%{_libdir}/freeradius/rlm_ippool.so
%{_libdir}/freeradius/rlm_linelog.so
%{_libdir}/freeradius/rlm_logintime.so
%{_libdir}/freeradius/rlm_mschap.so
%{_libdir}/freeradius/rlm_otp.so
%{_libdir}/freeradius/rlm_pam.so
%{_libdir}/freeradius/rlm_pap.so
%{_libdir}/freeradius/rlm_passwd.so
%{_libdir}/freeradius/rlm_preprocess.so
%{_libdir}/freeradius/rlm_radutmp.so
%{_libdir}/freeradius/rlm_realm.so
%{_libdir}/freeradius/rlm_replicate.so
%{_libdir}/freeradius/rlm_soh.so
%{_libdir}/freeradius/rlm_sometimes.so
%{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sqlcounter.so
%{_libdir}/freeradius/rlm_sqlippool.so
%{_libdir}/freeradius/rlm_sql_null.so
%{_libdir}/freeradius/rlm_unix.so
%{_libdir}/freeradius/rlm_unpack.so
%{_libdir}/freeradius/rlm_utf8.so
%{_libdir}/freeradius/rlm_wimax.so
%{_libdir}/freeradius/rlm_yubikey.so

# main man pages
%doc %{_mandir}/man5/clients.conf.5.gz
%doc %{_mandir}/man5/dictionary.5.gz
%doc %{_mandir}/man5/radiusd.conf.5.gz
%doc %{_mandir}/man5/radrelay.conf.5.gz
%doc %{_mandir}/man5/rlm_always.5.gz
%doc %{_mandir}/man5/rlm_attr_filter.5.gz
%doc %{_mandir}/man5/rlm_chap.5.gz
%doc %{_mandir}/man5/rlm_counter.5.gz
%doc %{_mandir}/man5/rlm_detail.5.gz
%doc %{_mandir}/man5/rlm_digest.5.gz
%doc %{_mandir}/man5/rlm_expr.5.gz
%doc %{_mandir}/man5/rlm_files.5.gz
%doc %{_mandir}/man5/rlm_idn.5.gz
%doc %{_mandir}/man5/rlm_mschap.5.gz
%doc %{_mandir}/man5/rlm_pap.5.gz
%doc %{_mandir}/man5/rlm_passwd.5.gz
%doc %{_mandir}/man5/rlm_realm.5.gz
%doc %{_mandir}/man5/rlm_sql.5.gz
%doc %{_mandir}/man5/rlm_unix.5.gz
%doc %{_mandir}/man5/unlang.5.gz
%doc %{_mandir}/man5/users.5.gz
%doc %{_mandir}/man8/raddebug.8.gz
%doc %{_mandir}/man8/radiusd.8.gz
%doc %{_mandir}/man8/radmin.8.gz
%doc %{_mandir}/man8/radrelay.8.gz

# MIB files
%{_datadir}/snmp/mibs/*RADIUS*.mib

%files doc

%doc %{docdir}/


%files utils
/usr/bin/*

# utils man pages
%doc %{_mandir}/man1/radclient.1.gz
%doc %{_mandir}/man1/radeapclient.1.gz
%doc %{_mandir}/man1/radlast.1.gz
%doc %{_mandir}/man1/radtest.1.gz
%doc %{_mandir}/man1/radwho.1.gz
%doc %{_mandir}/man1/radzap.1.gz
%doc %{_mandir}/man1/rad_counter.1.gz
%doc %{_mandir}/man1/smbencrypt.1.gz
%doc %{_mandir}/man1/dhcpclient.1.gz
%doc %{_mandir}/man5/checkrad.5.gz
%doc %{_mandir}/man8/radcrypt.8.gz
%doc %{_mandir}/man8/radsniff.8.gz
%doc %{_mandir}/man8/radsqlrelay.8.gz
%doc %{_mandir}/man8/rlm_ippool_tool.8.gz

%files devel
/usr/include/freeradius

%files krb5
%{_libdir}/freeradius/rlm_krb5.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/krb5

%files perl
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/perl

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/perl
%attr(640,root,radiusd) /etc/raddb/mods-config/perl/example.pl

%{_libdir}/freeradius/rlm_perl.so

%files python
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/python
/etc/raddb/mods-config/python/example.py*
/etc/raddb/mods-config/python/radiusd.py*
%{_libdir}/freeradius/rlm_python.so

%files mysql
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/noresetcounter.conf

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/mysql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/mysql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mysql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/setup.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/mysql/extras
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/mysql/extras/wimax
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/extras/wimax/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/extras/wimax/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/ndb
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/ndb/setup.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/ndb/schema.sql
/etc/raddb/mods-config/sql/main/ndb/README

%{_libdir}/freeradius/rlm_sql_mysql.so

%files postgresql
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/noresetcounter.conf

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/postgresql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/postgresql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/setup.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/postgresql/extras
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/extras/voip-postpaid.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/extras/cisco_h323_db_schema.sql

%{_libdir}/freeradius/rlm_sql_postgresql.so

%files sqlite
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/noresetcounter.conf

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/schema.sql

%{_libdir}/freeradius/rlm_sql_sqlite.so

%files ldap
%{_libdir}/freeradius/rlm_ldap.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ldap

%files unixODBC
%{_libdir}/freeradius/rlm_sql_unixodbc.so

%files rest
%{_libdir}/freeradius/rlm_rest.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/rest

%files couchbase
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/couchbase
%{_libdir}/freeradius/rlm_couchbase.so

%changelog
* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.15-3
- Backported freeradius-3.0.15-3.fc27
- https://koji.fedoraproject.org/koji/buildinfo?buildID=944999
- Updated to 3.0.17
- Enabled rlm_couchbase
- Removed un-used redis files

