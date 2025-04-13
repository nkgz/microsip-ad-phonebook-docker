# MicroSIP Active Directory Address Book

Generates MicroSIP phone address book from Active Directory. Built with Python and Docker for easy deployment.\
[Script](https://www.oldfag.ru/2021/03/microsip-ldap-addressbook.html) is taken as a basis.

## Setup

1. **Clone repository**
    ```bash
    git clone https://github.com/yourname/microsip-ad-book.git
    cd microsip-ad-book
    ```

2. **Configure .env file**
    ```ini
    AD_USER='your_service_account'
    AD_PASSWORD='secure_password'
    AD_SCOPE='DC=domain,DC=local'  # e.g. DC=contoso,DC=com
    AD_DOMAIN='domain.local'
    ```

3. **Build container**
    ```bash
    docker compose build
    ```

4. **Run service**
    ```bash
    docker compose up -d
    # Listens on port 65000 by default
    ```

## MicroSIP Configuration
1. Open **Settings** → **Advanced**
2. Set **Address book URL**:
    ```
    http://your-server-ip:65000/phonebook.xml
    ```
3. Enable **Use address book**