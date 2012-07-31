Summary: Wrapper for ssh. To store keys inside ldap.
Name: openssh-ldap-publickey
Version: 0.1
Release: 1
License: GPLv3
Group: Misc
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: %{name}-%{version}-%{release}.tar.gz

Requires: perl-LDAP

%description
Wrapper for ssh. To store keys inside ldap.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

install -d -m 0755 %{buildroot}/usr/bin/
install -d -m 0755 %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0755 ssh-ldap-auth %{buildroot}/usr/bin/
install -m 0644 openssh-lpk-openldap.schema %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 HOWTO %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}
install -m 0644 openssh-ldap-publickey.spec %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}


%clean
rm -rf %{buildroot}

%files
%dir /usr/share/doc/%{name}-%{version}-%{release}
%defattr(-,root,root,-)
/usr/bin/ssh-ldap-auth
/usr/share/doc/%{name}-%{version}-%{release}/openssh-lpk-openldap.schema
/usr/share/doc/%{name}-%{version}-%{release}/HOWTO
/usr/share/doc/%{name}-%{version}-%{release}/openssh-ldap-publickey.spec

%changelog
* Mon Jun 25 2012 Andrii Grytsenko <andrii.grytsenko@gmail.com> 0.1
- Added multikeys feature 
- Added howto 
- Added spec
- Created openssh-ldap-publickey package for version 0.1

