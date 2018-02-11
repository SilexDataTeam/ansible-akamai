# ansible-akamai
Ansible Module for working with Akamai OPEN APIIs

# Prerequisites
- Edgegrid-Python (install with `pip install edgegrid python`), works with Python 2.7+

# Install
Drop `akamai.py` into `./library` in any Ansible playbook, then invoke it like any standard module

# Variables
Akamai OPEN credentials are required to use this module.  A reference to get the credentials can be found here - https://developer.akamai.com/introduction/Prov_Creds.html

You may either list the credentials for every task or assign each value to the correct environment variable, following the pattern below (all envfironment variables may either be defined for the session or listed in a script file):
```
Host = AKAMAI_HOST
Access token = AKAMAI_ACCESS_TOKEN
Client token = AKAMAI_CLIENT_TOKEN
Client secret = AKAMAI_CLIENT_SECRET
```
