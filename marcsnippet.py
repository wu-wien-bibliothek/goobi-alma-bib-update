import lxml.etree as ET

class MarcSnippet:
    def __init__(self):
        self.collection = ET.Element('collection')
        self.record = ET.SubElement(self.collection, 'record')
        
    def add_field(self, config, data):
        """
        Add a field (controlfield or datafield) to the record.
        
        Args:
            config (dict): Field configuration with keys 'controlfield', 'datafield', 'ind1', 'ind2', 'subfields', and 'target-subfield'.
            data (str): The data to be added to the field.
        """
        if 'controlfield' in config:
            controlfield = ET.SubElement(self.record, 'controlfield', tag=config['controlfield'])
            controlfield.text = data
        else:
            datafield = ET.SubElement(self.record, 'datafield', tag=config['datafield'], ind1=config['ind1'], ind2=config['ind2'])
            for subfield in config['subfields']:
                subfieldElement = ET.SubElement(datafield, 'subfield', code=subfield[0])
                if subfield[0] == config['target_subfield']:
                    subfieldElement.text = subfield[1].format(data=data)
                else:
                    subfieldElement.text = subfield[1]

    def write_xml(self, path):
        """
        Write the XML record to a file.

        Args:
            path (file): Filelike object to the output XML file.
        """
        tree = ET.ElementTree(self.record)
        tree.write(path, encoding='utf-8', xml_declaration=True, pretty_print=True)