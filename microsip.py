#!/usr/bin/python3
# coding=UTF-8

import os

# Contacts file path
contacts_file = '/data/nginx/contacts.xml'
# Active Directory search root
scope = os.environ['AD_SCOPE']
# LDAP filter for user accounts with phone numbers
ldapfilter = '(&(telephoneNumber=*)(objectClass=user))'
# Active Directory domain
domain = os.environ['AD_DOMAIN']
# LDAP connection port
port = '389'
# AD authentication credentials
ldapbind = os.environ['AD_USER']
ldappassword = os.environ['AD_PASSWORD']

# -------------------------------

import ldap, time
from xml.dom import minidom
import xml.etree.cElementTree as ET

while True:
    # Establish LDAP connection
    ad = ldap.initialize('ldap://'+domain+':'+port)
    ad.protocol_version = ldap.VERSION3
    ad.set_option(ldap.OPT_REFERRALS, 0)
    ad.simple_bind_s(ldapbind+'@'+domain, ldappassword)

    # Retrieve user list from AD
    res = []
    try:
        res = ad.search_s(scope, ldap.SCOPE_SUBTREE, ldapfilter, ['displayName','telephoneNumber'])
        # Create XML root with refresh interval
        root = ET.Element('contacts', refresh='0')
        # Populate contact list
        for rec in res:
            if "displayName" in rec[1]:
                name = rec[1]['displayName'][0].decode('utf-8')
                number = rec[1]['telephoneNumber'][0].decode('utf-8')

                # Check for existing number
                existing_contact = root.find(".//contact[@number='" + number + "']")
                if existing_contact is not None:
                    existing_name = existing_contact.get('name')
                    # Append name if less than 3 entries
                    if len(existing_name.split(', ')) < 3:
                        existing_contact.set('name', existing_name + ', ' + name)
                else:
                    # Validate 4-digit numeric format
                    if len(number) == 4 and number.isdigit():
                        ET.SubElement(root, 'contact', name=name, number=number, presence='0')

        # Sort and write XML
        root[:] = sorted(root, key=lambda child: (child.tag, child.get('name')), reverse=True)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(contacts_file, 'wb') as xml_file:
            xml_file.write(xmlstr.encode('utf-8'))
    # Error handling
    except ldap.LDAPError as error_message:
        print(error_message)
    finally:
        ad.unbind_s()
    # Wait 3 hours before next update
    time.sleep(10800)