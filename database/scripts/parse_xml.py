import xml.etree.ElementTree as ET

def parse_kanjivg_xml(kanjivg_xml_path):
    # Parse the XML file
    tree = ET.parse(kanjivg_xml_path)
    root = tree.getroot()
    
    # Define the namespace
    namespace = {'kvg': 'http://kanjivg.tagaini.net'}

    kanji_mapping = {}

    # Iterate through <kanji> elements
    for character in root.findall(".//kanji", namespace):
        # Find the primary <g> element directly under <kanji>

        g_elem = character.find("./g", namespace)
        
        if g_elem is not None:
            kanji_char = g_elem.get('{http://kanjivg.tagaini.net}element', None)
            if kanji_char:
                # Extract the SVG ID from the kanji id attribute, which looks like "kvg:kanji_0f9b2"
                kanji_id = character.get('id')  # e.g. "kvg:kanji_0f9b2"
                # Remove "kvg:kanji_" to get the base ID ("0f9b2")
                svg_id = kanji_id.replace('kvg:kanji_', '')

                svg_file = f"{svg_id}.svg"
                kanji_mapping[kanji_char] = svg_file

    return kanji_mapping