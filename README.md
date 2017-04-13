openssh-ldap-publickey
======================

Wrapper for OpenSSH to store public keys inside the OpenLDAP entry.

## How does it work?

You create entry for user from OpenLdap and add attribut `'sshPublicKey'` with **PublicKey** to this user.
When user try login through the ssh, OpenSSH calls **/usr/bin/openssh-ldap-publickey script** which in its turn makes request to OpenLdap asking for **sshPublicKey** attribute value.

Ldap connection parameters are used by **openssh-ldap-publickey** is taken from **/etc/ldap.conf, /etc/pam_ldap.conf or /etc/libnss-ldap.conf** file.
Keep in mind that  **'pam_filter'** value from **/etc/ldap.conf, /etc/pam_ldap.conf or /etc/libnss-ldap.conf** is used by **openssh-ldap-publickey**.

Basically, it looks similar to this scheme   
ssh-client -> ssh-server -> openssh-ldap-publickey -> openldap server -> openldap server is looking for attribute **sshPublicKey** inside user's entry in Base DN
## How to setup step by step?

To implement ldap key authentication support take next steps:
##### OpenLDAP side

1. Setup your system to use ldap authorization
2. Add new ldap schema from */usr/share/doc/openssh-ldap-publickey-{version}/openssh-lpk-openldap.schema* to your ldap server.
3. In case you want take advantage of host based authorization, change your */etc/ldap.conf, /etc/pam_ldap.conf or /etc/libnss-ldap.conf* adding:   
    + Add new object to your user entry - **ldapPublicKey**    
    `pam_filter |(host=test-server.example.com)(host=\*)`
    + Add next attributes into user entry:
    **Host: test-server.example.com** <- in case of host-based auth     
    **sshPublicKey: ssh-rsa some_public_key_here user@hostname** <- put here your public key from ~/.ssh/id_{rsa,dsa}.pub     
    **sshPublicKey: ssh-rsa some_ohter_public_key_here user2@hostname2** <- there can be several sshPublicKey entries in event of you want connect from different computers

##### OpenSSH side:
1. Setup openssh with **AuthorizedKeysCommand** support(openssh-server >= 6.2, Redhat openssh-server >= 5.3)
2. Change **sshd_config**:     
`AuthorizedKeysCommand /usr/bin/openssh-ldap-publickey`     
`AuthorizedKeysCommandRunAs nobody`     
if you want store key **ONLY** in ldap, change next lines     
`#AuthorizedKeysFile     .ssh/authorized_keys`      
`AuthorizedKeysFile      /dev/null`


#### Building RPM:
1. Download **misc/openssh-ldap-publickey.spec** to **$rpmbuild/SPECS**
2. Download all source into **$rpmbuild/SOURCE**. You can do it automatically running:     
`cd $rpmbuild/SPECS && spectool -gf  -C ../SOURCES/ openssh-ldap-publickey.spec`
3. Build package:      
`rpmbuild -bb openssh-ldap-publickey.spec`     

#### Requirements:
1. **Perl**
2. Perl module **Net::LDAP**
3. OpenSSH with **AuthorizedKeysCommand** support:
    * mainstream openssh-server >= 6.2
    * RedHat/CentOS openssh-server >= 5.3

#### Requirements (Debian / Ubuntu):
1. Debian 8+ (or 7+ with backports) / Ubuntu 14.04+
2. `apt-get install libnet-ldap-perl`

### Configuration:

All configuration is read from **/etc/ldap.conf, /etc/pam_ldap.conf or /etc/libnss-ldap.conf** and currently script uses only those parameters:


**uri** - uri to ldap     
**pam_filter** - ldap search filter(*Optional*)     
**base** - ldap base dir      
**nss_base_passwd** - User DN. If not set - "ou=People" + **base**.     
**timeout** - ldap connection timeout. Default 10.         
**binddn** - bind dn(*Optional*)      
**bindpw** - bind dn password(*Optional*)      
**openssh_ldap_loglevel** - log level. By default the logging is turn off.       
**openssh_ldap_logfile** - logfile using only when debug is on. Default */tmp/openssh-ldap-publickey.log*.      

For more information about this params refer to ldap.conf man page.

#### Auth support:
To enable auth set **binddn** and **bindpw** in ldap.conf

#### Logging:
In order to enable logging you have to setup **openssh_ldap_loglevel** and **openssh_ldap_logfile** variables.

## Known issues
1. Script fails with error 255    
    **Symptoms**:   
    * return code is 255    
    * In logs:       
    ```sshd[36009]: error: AuthorizedKeysCommand /etc/ssh/openssh-ldap-publickey returned status 225``
    * When running from console:       
    ```No such object at /usr/bin/openssh-ldap-publickey line 77.```      


    **Cause**:      
    Variable **nss_base_passwd** in **ldap.conf** is empty or doesn't set explicitly to users DN.     

    **Solution**:     
    Set **nss_base_passwd** explicitly to users DN.     
    Example: **ou=People,dc=test,dc=com** (without prefix **?one** or something)     


## Where to download RPM package?      
You can find RPM packages [here](http://andriigrytsenko.net/repo/openssh-ldap-publickey/)

### AuthorizedKeysCommand support and CentOS/RHEL 5.x
Check [this page](http://andriigrytsenko.net/2013/05/authorizedkeyscommand-support-and-centosrhel-5-x/) to see how to configure AuthorizedKeysCommand in CentOS/RHEL 5.x.
