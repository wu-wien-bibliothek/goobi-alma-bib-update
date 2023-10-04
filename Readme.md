# goobi-alma-bib-update

Script for a Goobi script step that writes an xml file containing a MARC snippet to an FTP server in order to update Alma MARC files via import profiles. The snippet contains one field with an identifier against which Alma can perform the matching and any number of data fields which shall be merged.

## Dependencies

lxml, paramiko 

```
pip3 install lxml paramiko
```

## Configuration

This script requires a json file for general configuration and a separate json file for sftp settings.

### config.json

```json
{
    "target_type": "sftp",   
    "target_path": "/files/sandbox/import/goobi/",
    "sftp_settings_file": "/Users/gduffner/alma_sftp.json",
    "matching_ids": {
        "mms_id": {
            "controlfield": "001",
            "validation_regex": "^9\\d+3337$"
        },
        "other_id": {
            "datafield": "035",
            "ind1": " ",
            "ind2": " ",
            "target_subfield": "a",
            "subfields": [
                ["a", "(AT-OBV){data}"]
            ],
            "validation_regex": "AC\\d{8}"
        }
    },
    "data": {
        "doi": {
            "datafield": "024",
            "ind1": "7",
            "ind2": " ",
            "target_subfield": "a",
            "subfields": [
                ["a", "{data}"],
                ["2", "doi"]
            ],
            "validation_regex": "^10.\\d{4,}/.+$"
        },
        "repro-776": {
            "datafield": "776",
            "ind1": "0",
            "ind2": "8",
            "target_subfield": "o",
            "subfields": [
                ["i", "Elektronische Reproduktion"],
                ["d", "Wien : Wirtschaftsuniversität Wien"],
                ["o", "{data}"]
            ],
            "validation_regex": "^10.\\d{4,}/.+$"
        },
        "repro-doi-url": {
            "datafield": "856",
            "ind1": "4",
            "ind2": "1",
            "target_subfield": "u",
            "subfields": [
                ["u", "https://doi.org/{data}"],
                ["x", "Resolving-System"],
                ["z", "kostenfrei"],
                ["3", "Volltext"],
                ["7", "0"]
            ],
            "validation_regex": "^10.\\d{4,}/.+$"
        }
    }
}

```

#### Parameters:

| Element       | Description                              |
|---------------|------------------------------------------|
| `target_type` | `sftp` or `local` for a local file path. |
| `target_path` | Either a local path or a path on the sftp server. |
| `sftp_settings_file` | Path to the sftp settings file. |
| `matching_ids` | Dictionary with possible fields for identifier matching. The field definitions here and in the `data` dictionary follow the same pattern. |
| `data` | Definitions for data fields which can be merged in Alma. |
| _field key_ | A key that identifies the field and is given as the key in the arguments list in the Goobi script step. |
| `controlfield` or `datafield` | MARC field type, the value contains the field tag. |
| `ind1`, `ind2` | MARC indicator values |
| `target_subfield` | Defines which subfield will contain the data value given in the arguments list in the script step. |
| `subfields` | List of subfields that shall be written |
| `['x', 'Resolving-System']` | Each subfield is a list of a subfield code and the contents. |
| `['u', 'https://doi.org/{data}']` | The subfield that shall receive the data value needs to contain `{data}` in the second list item. There may be content around it. |
| `validation_regex` | Contains a regex against which the validity of the given value can be checked. At least `.+` should be given. |

### alma_sftp.json

```json
{
  "server": "ftp.example.org",
  "username": "almauser",
  "password": "password",
  "key_filename": null
}
```

## Calling the script

```
python3 /path/to/goobi-alma-bib-update/main.py --kwargs ac_nr={meta.CatalogIDDigital} doi={meta.DOI}
```