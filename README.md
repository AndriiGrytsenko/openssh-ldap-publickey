openssh-ldap-publickey
======================

Wrapper for OpenSSH to store public keys inside the OpenLDAP entry.

## How it works? 

You created entry for user inside OpenLdap and add attribut `'sshPublicKey'` with **PublicKey** to this user. 
When user try login through the ssh, OpenSSH calls **/usr/bin/openssh-ldap-publickey script** which in its turn make request to OpenLdap asking for **sshPublicKey** value.   
Ldap connection configuration used by **openssh-ldap-publickey** is taking from **/etc/ldap.conf** file. Also keep in mind that **openssh-ldap-publickey** takes into account **'pam_filter'** value from **/etc/ldap.conf**.

Basically, it looks similar to this scheme   
ssh-client -> ssh-server -> openssh-ldap-publickey -> openldap server -> openldap server is looking for attribute sshPublicKey inside user's entry in Base DN
## How to setup step by step? 

To implement ldap key authentication support take next steps:
##### OpenLDAP side

1. Your system should be already setup for using ldap authorization
2. Add new ldap schema from */usr/share/doc/openssh-ldap-publickey-{version}/openssh-lpk-openldap.schema* to your ldap server.
3. Change your */etc/ldap.conf* add(in case you want take advantage of host based authorization):
`pam_filter |(host=test-server.example.com)(host=\*)`
4. Add next attributes into user entry:  
**Host: test-server.example.com** <- in case of hast-based auth  
**sshPublicKey: ssh-rsa some_public_key_here user@hostname** <- put here your public key from ~/.ssh/id_{rsa,dsa}.pub
**sshPublicKey: ssh-rsa some_ohter_public_key_here user2@hostname2** <- there can be several sshPublicKey entries in event of you want connect from different computers

##### OpenSSH side:
4. Setup openssh with **AuthorizedKeysCommand** support(openssh-server > 5.3)
5. Change **sshd_config**:  
`AuthorizedKeysCommand /usr/bin/openssh-ldap-publickey`  
`AuthorizedKeysCommandRunAs root`  
if you want store key **ONLY** in ldap, change next lines  
`#AuthorizedKeysFile     .ssh/authorized_keys`  
`AuthorizedKeysFile      /dev/null`  


#### Requirements:
1. **Perl**  
2. Perl module **Net::LDAP**  
3. OpenSSH with **AuthorizedKeysCommand** support(openssh-server > 5.3)  