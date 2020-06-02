import re

# I/O files
OSM_FILE = 'Madison.osm'
NODE_FILE = 'node.csv'
NODE_TAG_FILE = 'node_tag.csv'
WAY_FILE = 'way.csv'
WAY_TAG_FILE = 'way_tag.csv'
WAY_NODE_FILE = 'way_node.csv'

# Header values for output CSV files
NODE_HEAD = ['id', 'lat', 'lon', 'version']
NODE_TAG_HEAD = ['id', 'key', 'value', 'type']
WAY_HEAD = ['id', 'version']
WAY_TAG_HEAD = ['id', 'key', 'value', 'type']
WAY_NODE_HEAD = ['id', 'node_id']

# Regular expressions for validating zips, phones, etc.
PROBLEM_CHARACTERS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
ZIP_CODE_RE = re.compile(r'^(\d{5})[- ]?(\d{4})?$')
PHONE_NUM_RE = re.compile(r'^[+]?(1)?[- \.]?[( ]?(\d{3})[ )]?[- \.]?(\d{3})[- \.?]?(\d{4})$')
PHONE_REPLACEMENT_RE = '\\2\\3\\4'
STREET_NAME_RE = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# List of acceptable address names for validation
expected_addresses = ['Avenue', 'Bend', 'Boulevard', 'Broadway',
                      'Circle', 'Close', 'Commons', 'Court',
                      'Crestway', 'Cross', 'Drive', 'Highway',
                      'Lane', 'Lawn', 'Main', 'Mews', 'Parkway',
                      'Pass', 'Place', 'Plaza', 'Ridge', 'Road',
                      'Row', 'Square', 'Street', 'Terrace', 'Trace',
                      'Trail', 'Way']