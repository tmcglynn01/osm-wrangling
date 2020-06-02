from audit import *


zip_map = {'5': ''}
street_map = {
    'Ave': 'Avenue', 'Ave.': 'Avenue', 'Avenues': 'Avenue',
    'Blvd': 'Boulevard',
    'Cir': 'Circle', 'Ct': 'Court',
    'Dr': 'Drive', 'Dr.': 'Drive',
    'Hamilton': 'Hamilton Street',
    'Johnson': 'Johnson Street',
    'Ln': 'Lane','Ln.': 'Lane',
    'Mall': 'Mall Road',
    'Pkwy': 'Parkway',
    'Rd': 'Road', 'Rd.': 'Road', 'road': 'Road',
    'St': 'Street', 'St.': 'Street', 'street': 'Street',
    'Stoughton': 'Stoughton Road',
    'Williamson': 'Williamson Street'}
phone_map = {'(608) 257-9700\u200b': '6082579700', 'no': ''}

#********************************************************************#
#     Functions for navigating the XML tree                          #
#********************************************************************#


def get_element(file=OSM_FILE, tags=('node', 'way', 'relation')):
    """Yield the element if it matches a specific tag type"""
    context = ET.iterparse(file, events=('start', 'end'))
    _, root = next(context)
    for event, element in context:
        if (event == 'end') and (element.tag in tags):
            yield element
            root.clear()


def shape_element(element):
    """Return the node or way as a dictionary from raw XML data"""
    node_attributes, way_attributes = {}, {}
    way_nodes_list, tags_list = [], []

    if element.tag == 'node':
        node_attributes = shape_element_attributes(element, NODE_HEAD)
        node_id = node_attributes['id']
        tags = shape_element_tags(element, node_id)
        return {'node': node_attributes, 'node_tag': tags}
    elif element.tag == 'way':
        way_attributes = shape_element_attributes(element, WAY_HEAD)
        way_id = way_attributes['id']
        tags = shape_element_tags(element, way_id)
        way_nodes = shape_way_node(element, way_id)
        return {'way': way_attributes, 'way_tag': tags, 'way_node': way_nodes}


def shape_element_attributes(element, header):
    """Convert raw XML to a dictionary node or way"""
    attributes = {}
    for field in header:
        attributes[field] = element.attrib[field]
    return attributes


def shape_element_tags(element, id_):
    """Shape the raw XML tags"""
    tags = []
    element_tags = element.findall('tag')
    if element_tags:
        for element_tag in element_tags:
            key, value = element_tag.get('k'), element_tag.get('v')
            if not re.search(PROBLEM_CHARACTERS, key):
                tag = {'id': id_}
                # First check to see if there is a colon in the string
                # If there is, split the string into type and key
                if ':' in key:
                    tag['type'], tag['key'] = key.split(':', 1)
                else:
                    tag['type'], tag['key'] = '', key

                # Next, address the tag values
                if key == 'addr:street':
                    tag['value'] = update_street_name(value)
                elif (key == 'phone') or (key == 'contact:phone'):
                    tag['value'] = update_phone_num(value)
                elif key == 'addr:postcode':
                    tag['value'] = update_zip_code(value)
                else:
                    tag['value'] = value

                tags.append(tag)
    return tags


def shape_way_node(element, way_id):
    """Convert raw XML into way_nodes dictionary"""
    way_nodes = []
    way_node_tags = element.findall('nd')
    for tag in way_node_tags:
        w_node = {'id': way_id, 'node_id': tag.get('ref')}
        way_nodes.append(w_node)
    return way_nodes


#********************************************************************#
#     Functions for updating the OSM data                            #
#********************************************************************#


def update_zip_code(zip_code, mapping=zip_map):
    '''Updates zip code format if it is found in the mapping'''
    if zip_code in mapping:
        replacement = mapping[zip_code]
        zip_code.replace(zip_code, replacement)
    return zip_code


def update_street_name(street_name, mapping=street_map):
    '''Updates street name format if it is found in the mapping'''
    street_type = street_name.split(' ')[-1]
    if street_type in mapping:
        replacement = mapping[street_type]
        street_name.replace(street_type, replacement)
    return street_name


def update_phone_num(phone_num, mapping=phone_map):
    """Updates phone number format if it is found in the mapping"""
    if phone_num in mapping:
        phone_num = mapping[phone_num]
        return phone_num
    else:
        return re.sub(PHONE_NUM_RE, PHONE_REPLACEMENT_RE, phone_num)

