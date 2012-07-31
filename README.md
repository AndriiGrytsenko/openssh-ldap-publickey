openssh-ldap-publickey
======================

Wrapper for OpenSSH to store public keys inside the OpenLDAP entry.

## How it works? 

You created entry for user inside OpenLdap and apply attribut `'sshPublicKey'` with **PublicKey** to this user. 
When user try login into the system OpenSSH run **/usr/bin/openssh-ldap-publickey script** which in its turn make request to OpenLdap asking for **sshPublicKey** value.
**openssh-ldap-publickey** script take ldap configuration from **/etc/ldap.conf** INCLUDING **'pam_filter'** value and takes it into account.

## How to setup step by step? 

To install ldap key authentication support take next steps:
##### OpenLDAP side

1. Add new ldap schema from */usr/share/doc/openssh-ldap-publickey-{version}/openssh-lpk-openldap.schema* to your ldap server.
2. Change your ldap.conf add(in case you want take advantage of host based authorization):
`pam_filter |(host=test-server.example.com)(host=\*)`
3. Add next attributes into user entry:  
**Host: test-server.example.com**  
**sshPublicKey: ssh-rsa some_long_long_key user@hostname**

##### OpenSSH side:
4. Setup openssh with **AuthorizedKeysCommand** support(openssh-server > 5.3)
5. Change **sshd_config**:  
`AuthorizedKeysCommand /usr/bin/openssh-ldap-publickey`  
`AuthorizedKeysCommandRunAs root`  
if you want store key **ONLY** in ldap change next lines  
`#AuthorizedKeysFile     .ssh/authorized_keys`  
`AuthorizedKeysFile      /dev/null`  

##### Requirements
1. Perl  
2. Perl module Net::LDAP  