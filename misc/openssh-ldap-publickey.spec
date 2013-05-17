Summary: Wrapper for OpenSSH to store public keys inside the OpenLDAP entry.
Name: openssh-ldap-publickey
Version: 0.1
Release: 2
License: GPLv3
Group: Applications/Internet
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/bin/openssh-ldap-publickey
Source1: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/misc/openssh-lpk-openldap.schema
Source2: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/README.md
Source3: https://raw.github.com/AndriiGrytsenko/openssh-ldap-publickey/master/misc/openssh-ldap-publickey.spec
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
install -m 0755 %{SOURCE0} %{buildroot}/usr/bin/
install -m 0644 %{SOURCE1} %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 %{SOURCE2} %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 %{SOURCE3} %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}


%clean
rm -rf %{buildroot}

%files
%dir /usr/share/doc/%{name}-%{version}-%{release}
%defattr(-,root,root,-)
/usr/bin/openssh-ldap-publickey
/usr/share/doc/%{name}-%{version}-%{release}/openssh-lpk-openldap.schema
/usr/share/doc/%{name}-%{version}-%{release}/README.md
/usr/share/doc/%{name}-%{version}-%{release}/openssh-ldap-publickey.spec

%changelog
* Thu Mar 14 2013 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.1-2 
- small changes in spec file
- small addition to documentation
* Mon Jun 25 2012 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.1
- Added multikeys feature 
- Added howto 
- Added spec
- Created openssh-ldap-publickey package for version 0.1
