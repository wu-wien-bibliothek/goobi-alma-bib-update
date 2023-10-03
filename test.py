import marcsnippet
import lxml.etree as ET
import unittest
import main as scrmain
import re


#print(ET.tostring(marc.record))
class TestMainscript(unittest.TestCase):
    def testValidation(self):
        config = {"controlfield": "009",
            "validation-regex": "^AC\\d{8}"}
        data = "AC12345678" 
        data1 = "AC123456789" 
        with self.assertRaises(AssertionError):
            scrmain.validate_value(config["validation-regex"], data1)
        self.assertIsNone(scrmain.validate_value(config["validation-regex"], data))

class TestMarcSnippetMethods(unittest.TestCase):
    def setUp(self):
        self.marc = marcsnippet.MarcSnippet()

    def testBasicRecord(self):
        self.assertEqual(ET.tostring(self.marc.record), b'<record/>')

    def testControlfield(self):
        config = {"controlfield": "009",
            "validation-regex": "^AC\\d{8}"}
        data = "AC12345678"
        self.marc.add_field(config, data)
        self.assertEqual(ET.tostring(self.marc.record), b'<record><controlfield tag="009">AC12345678</controlfield></record>')

    def testDatafield(self):
        config = {
            "datafield": "856",
            "ind1": "4",
            "ind2": "0",
            "target-subfield": "u",
            "subfields": [
                ["u", "data"],
                ["x", "Resolving-System"],
                ["3", "Volltext"]
            ],
            "validation-regex": "^10.\d{4,}/.+$",
            "prefix": "https://doi.org/"
        }
        data = "https://doi.org/10.33456/rm.AC12345678"
        self.marc.add_field(config, data)
        self.assertEqual(ET.tostring(self.marc.record), b'<record><datafield tag="856" ind1="4" ind2="0"><subfield tag="u">https://doi.org/10.33456/rm.AC12345678</subfield><subfield tag="x">Resolving-System</subfield><subfield tag="3">Volltext</subfield></datafield></record>')

    def testCombinedFields(self):
        config009 = {"controlfield": "009",
            "validation-regex": "^AC\\d{8}"}
        data009 = "AC12345678"
        self.marc.add_field(config009, data009)
        config035 = {
            "datafield": "035",
            "ind1": " ",
            "ind2": " ",
            "target-subfield": "a",
            "subfields": [
                ["a", "data"]
            ],
            "validation-regex": "AC\d{8}",
            "prefix": "(AT-OBV)"
        }
        data035 = "(AT-OBV)AC12345678"
        self.marc.add_field(config035, data035)
        config = {
            "datafield": "856",
            "ind1": "4",
            "ind2": "0",
            "target-subfield": "u",
            "subfields": [
                ["u", "data"],
                ["x", "Resolving-System"],
                ["3", "Volltext"]
            ],
            "validation-regex": "^10.\d{4,}/.+$",
            "prefix": "https://doi.org/"
        }
        data = "https://doi.org/10.33456/rm.AC12345678"
        self.marc.add_field(config, data)
        self.assertEqual(ET.tostring(self.marc.record), b'<record><controlfield tag="009">AC12345678</controlfield><datafield tag="035" ind1=" " ind2=" "><subfield tag="a">(AT-OBV)AC12345678</subfield></datafield><datafield tag="856" ind1="4" ind2="0"><subfield tag="u">https://doi.org/10.33456/rm.AC12345678</subfield><subfield tag="x">Resolving-System</subfield><subfield tag="3">Volltext</subfield></datafield></record>')

    def testValidation(self):
        config = {"validation-regex": "^10.\d{4,}/.+$"}
        pattern = config["validation-regex"]
        value = "10.33456/rm.AC12345678"
        pat = re.compile(pattern)
        #assert re.fullmatch(pat, value)
        self.assertTrue(re.fullmatch(pat, value))

if __name__ == '__main__':
    unittest.main()