Summary: Wrapper for OpenSSH to store public keys inside the OpenLDAP entry.
Name: openssh-ldap-publickey
Version: 0.4
Release: 1
License: GPLv3
Group: Applications/Internet
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/bin/openssh-ldap-publickey
Source1: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/misc/openssh-lpk-openldap.schema
Source2: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/README.md
Source3: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/misc/openssh-ldap-publickey.spec
Source4: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/man/openssh-ldap-publickey.8
BuildArch: noarch

Requires: perl-LDAP
Requires: openssh-server >= 5.3

%description
Wrapper for ssh. To store keys inside ldap.

#%prep
#%setup -q

#%build

%install
rm -rf %{buildroot}

install -d -m 0755 %{buildroot}/usr/bin/
install -d -m 0755 %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -d -m 0755 %{buildroot}/%_mandir/man8/
install -m 0755 %{SOURCE0} %{buildroot}/usr/bin/
install -m 0644 %{SOURCE1} %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 %{SOURCE2} %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 %{SOURCE3} %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 %{SOURCE4} %{buildroot}/%_mandir/man8/
gzip %{buildroot}/%_mandir/man8/openssh-ldap-publickey.8

%clean
rm -rf %{buildroot}

%files
%dir /usr/share/doc/%{name}-%{version}-%{release}
%defattr(-,root,root,-)
/usr/bin/openssh-ldap-publickey
%doc /usr/share/doc/%{name}-%{version}-%{release}/openssh-lpk-openldap.schema
/usr/share/doc/%{name}-%{version}-%{release}/README.md
/usr/share/doc/%{name}-%{version}-%{release}/openssh-ldap-publickey.spec
%_mandir/man8/openssh-ldap-publickey.8.gz

%changelog
* Sat Aug 17 2013 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.4-1
- refactoring and changed configuration variable name ( openssh_ldap_debug -> openssh_ldap_loglevel )
* Fri Aug 16 2013 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.3-1
- added auth support
- added new pam_filter check
- updated documentation
* Mon May 20 2013 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.2-1
- security fix in ldap filter
- added debug mode
- added connection timeout parameter
- defined default nss_base_passwd if not set
- updated documentation
- added man page
* Thu Mar 14 2013 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.1-2 
- small changes in spec file
- small addition to documentation
* Mon Jun 25 2012 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.1
- Added multikeys feature 
- Added howto 
- Added spec
- Created openssh-ldap-publickey package for version 0.1
