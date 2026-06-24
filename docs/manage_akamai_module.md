# manage_akamai Module

Ansible Module for working with Akamai OPEN APIs

## Prerequisites

- Python 2.7.10+ (NOTE:  This is higher then Ansible, which can run on Python 2.6 - 2.7.9)
- Edgegrid-Python (install with `pip install edgegrid-python`), works with Python 2.7.10+

## Install

- Install the collection from Ansible Galaxy:

  ```shell
  ansible-galaxy collection install silexdata.akamai
  ```

- Or install directly from the source repository:

  ```shell
  ansible-galaxy collection install git+https://github.com/SilexDataTeam/silexdata.akamai.git
  ```

- Once installed, invoke the module by its fully qualified collection name, `silexdata.akamai.manage_akamai`

## Credentials

- Akamai OPEN credentials are required to use this module.  A reference to get the credentials can be found here - [Get Credentials](https://developer.akamai.com/introduction/Prov_Creds.htm)

- The currently supported method for storing credentials is via an `.edgerc` file, the recommended location to store the file is in the home directory

## Variables

- `section` - Section of `.edgerc` file
- `endpoint` - API endpoint to hit
- `method` - GET or POST, similar to HTTPie and the Akamai CLI
- `body` - The request body that needs to used only for POST method
  - "productId": "prd_Alta",
  - "propertyName": "my.new.property.com",
- `headers` - The request headers that needs to used only for POST method
  - "Content-Type": "application/json"d
  - "PAPI-Use-Prefixes": "true"

## Acknowledgements

- The Akamai Technologies [api-kickstart](https://github.com/akamai/api-kickstart) repository where many other Akamai API examples are available!
- The Akamai API Catalog: <https://developer.akamai.com/api/>
- Jacob Hudson (@jacob-hudson) for the initial work on the library.
