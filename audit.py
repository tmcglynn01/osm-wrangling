from CONSTANTS import *
from pprint import pprint
from collections import defaultdict
import xml.etree.cElementTree as ET

# Use defaultdict sets for data validation, esp. streetnames
zip_code_audit = defaultdict(set)
phone_num_audit = defaultdict(set)
address_audit = defaultdict(set)

#********************************************************************#
#     Functions for auditing the OSM data                            #
#********************************************************************#


def audit(file=OSM_FILE):
    """
    	Audits a given OSM file
    	Args:
    		file: a file object for processing
    	Returns:
    		text: audited zip codes, phone nums, and street names
    """
    f = open(file, 'r')
    for event, element in ET.iterparse(f, events=('start',)):
        if (element.tag == 'node') or (element.tag == 'way'):
            for tag in element.iter('tag'):
                if is_zip_code(tag):
                    audit_zip_code(tag.attrib['v'])
                if is_street_name(tag):
                    audit_street_name(tag.attrib['v'])
                if is_phone(tag):
                    audit_phone_num(tag.attrib['v'])
    f.close()
    audit_printer('ZIP CODES', zip_code_audit)
    audit_printer('STREET NAMES', address_audit)
    audit_printer('PHONE NUMBERS', phone_num_audit)


def is_zip_code(element):
    return element.attrib['k'] == 'addr:postcode'


def is_street_name(element):
    return element.attrib['k'] == 'addr:street'


def is_phone(element):
    return (element.attrib['k'] == 'phone') or (element.attrib['k'] == 'contact:phone')


def audit_zip_code(zip_code):
    """
    	Audits a zip code to determine its validity
    	Args:
    		zip_code (string): pre-validated zip code
    	Returns:
    		None: adds to a defaultdict(set) of invalid zip codes
    """
    match = ZIP_CODE_RE.search(zip_code)
    if not match:
        zip_code_audit[zip_code].add(zip_code)


def audit_street_name(street_name):
    """
    	Audits a street name to determine its validity
    	Args:
    		street_name (string): pre-validated street name
    	Returns:
    		None: adds to a defaultdict(set) of invalid street names
    """
    match = STREET_NAME_RE.search(street_name)
    if match:
        street_type = match.group()
        if street_type not in expected_addresses:
            address_audit[street_type].add(street_name)


def audit_phone_num(phone_num):
    """
    	Audits a phone number to determine its validity
    	Args:
    		phone_num (string): pre-validated phone number
    	Returns:
    		None: adds to a defaultdict(set) of invalid phone numbers	
    """
    match = PHONE_NUM_RE.search(phone_num)
    if not match:
        phone_num_audit[phone_num].add(phone_num)


def audit_printer(audit_name, audit_type):
    print('#', '*' * 68, '#')
    print(' ' * 5, 'Auditing: {}'.format(audit_name))
    print('#', '*' * 68, '#')
    pprint(dict(audit_type))
    print('\n\n')
