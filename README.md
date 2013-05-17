openssh-ldap-publickey
======================

Wrapper for OpenSSH to store public keys inside the OpenLDAP entry.

## How it works?

You create entry for user from OpenLdap and add attribut `'sshPublicKey'` with **PublicKey** to this user.
When user try login through the ssh, OpenSSH calls **/usr/bin/openssh-ldap-publickey script** which in its turn makes request to OpenLdap asking for **sshPublicKey** attribute value.

Ldap connection parameters are used by **openssh-ldap-publickey** is taken from **/etc/ldap.conf** file.
Keep in mind that  **'pam_filter'** value from **/etc/ldap.conf** is used by **openssh-ldap-publickey**.

Basically, it looks similar to this scheme    
ssh-client -> ssh-server -> openssh-ldap-publickey -> openldap server -> openldap server is looking for attribute **sshPublicKey** inside user's entry in Base DN
## How to setup step by step?

To implement ldap key authentication support take next steps:
##### OpenLDAP side

1. Setup your system to use ldap authorization
2. Add new ldap schema from */usr/share/doc/openssh-ldap-publickey-{version}/openssh-lpk-openldap.schema* to your ldap server.
3. In case you want take advantage of host based authorization, change your */etc/ldap.conf* adding:
4. Add new object to your user entry - **ldapPublicKey**
`pam_filter |(host=test-server.example.com)(host=\*)`
5. Add next attributes into user entry:    
**Host: test-server.example.com** <- in case of host-based auth    
**sshPublicKey: ssh-rsa some_public_key_here user@hostname** <- put here your public key from ~/.ssh/id_{rsa,dsa}.pub     
**sshPublicKey: ssh-rsa some_ohter_public_key_here user2@hostname2** <- there can be several sshPublicKey entries in event of you want connect from different computers        

##### OpenSSH side:
4. Setup openssh with **AuthorizedKeysCommand** support(openssh-server >= 6.2, Redhat openssh-server >= 5.3)
5. Change **sshd_config**:    
`AuthorizedKeysCommand /usr/bin/openssh-ldap-publickey`    
`AuthorizedKeysCommandRunAs root`    
if you want store key **ONLY** in ldap, change next lines    
`#AuthorizedKeysFile     .ssh/authorized_keys`   
`AuthorizedKeysFile      /dev/null`   


#### Building RPM:
1. Download **misc/openssh-ldap-publickey.spec** to **$rpmbuild/SPECS**
2. Download all source into **$rpmbuild/SOURCE**.
you can do it automatically running:    
`cd $rpmbuild/SPECS && spectool -gf  -C ../SOURCES/ openssh-ldap-publickey.spec`
3. Build package:    
`rpmbuild -bb openssh-ldap-publickey.spec`

#### Requirements:
1. **Perl**
2. Perl module **Net::LDAP**
3. OpenSSH with **AuthorizedKeysCommand** support:   
    * mainstream openssh-server >= 6.2
    * RedHat/CentOS openssh-server >= 5.3

#### Notes:

To make it works with RHEL/CentOS 5.x you have to download and build your own rpm package of openssh-server higher or equal to version 5.3

#### Issues:
1. variable **nss_base_passwd** in **ldap.conf** should be set properly to fully qualified path. Example: **ou=People,dc=test,dc=com** (without prefix **?one** or something)
