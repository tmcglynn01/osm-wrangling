from csv import DictWriter as dw
from process_map import *


# ********************************************************************#
#     Main Function                                                  #
# ********************************************************************#


def process_map(file=OSM_FILE):
    """Iteratively process each XML element and write to csv(s)"""
    with open(NODE_FILE, 'w', encoding='utf-8') as node_file, \
            open(NODE_TAG_FILE, 'w', encoding='utf-8') as node_tag_file, \
            open(WAY_FILE, 'w', encoding='utf-8') as way_file, \
            open(WAY_TAG_FILE, 'w', encoding='utf-8') as way_tag_file, \
            open(WAY_NODE_FILE, 'w', encoding='utf-8') as way_node_file:

        # Use dictwriter for each of the csv file writers
        node_writer = dw(node_file, NODE_HEAD)
        node_tag_writer = dw(node_tag_file, NODE_TAG_HEAD)
        way_writer = dw(way_file, WAY_HEAD)
        way_tag_writer = dw(way_tag_file, WAY_TAG_HEAD)
        way_node_writer = dw(way_node_file, WAY_NODE_HEAD)

        # Write the headers for each of the csv files
        node_writer.writeheader()
        node_tag_writer.writeheader()
        way_writer.writeheader()
        way_tag_writer.writeheader()
        way_node_writer.writeheader()

        # Determine if node/way, then write XML data to file
        for element in get_element(file, tags=('node', 'way')):
            elem = shape_element(element)
            if elem:
                if element.tag == 'node':
                    node_writer.writerow(elem['node'])
                    node_tag_writer.writerows(elem['node_tag'])
                elif element.tag == 'way':
                    way_writer.writerow(elem['way'])
                    way_node_writer.writerows(elem['way_node'])
                    way_tag_writer.writerows(elem['way_tag'])


if __name__ == '__main__':
    audit()
    process_map()
