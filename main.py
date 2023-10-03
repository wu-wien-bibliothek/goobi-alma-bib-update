import argparse
import json
import re
import time

from marcsnippet import MarcSnippet
from keyvalue import keyvalue
from sftpClient import SFTPClient


def read_args():  
    # creating parser object
    parser = argparse.ArgumentParser()
    
    # adding aan rguments 
    parser.add_argument('--config', default='config.json', help='Path to the configuration file.')
    parser.add_argument('--kwargs', nargs='*', action = keyvalue)
    
    #parsing arguments 
    return parser.parse_args()

def load_config(config_file):
    # load config 
    with open(config_file, 'r') as myconffile:
        data=myconffile.read()
    return json.loads(data)

def validate_value(pattern, value):
    if not re.fullmatch(pattern, value):
        raise ValueError(f"Value {value} doesn’t match validation pattern `{pattern}`")

# find matching id in args
def find_matching_id(key_values, config):
    # The id against which the record will match can be at any position.
    # Loop through the possible ids in the config file and take the first
    #   which you find in the arguments. 
    for key in config["matching-ids"]:
        if key in key_values:
            id_value = key_values[key]
            validate_value(config["matching-ids"][key]["validation-regex"], id_value)
            # Delete the entry from the array of arguments.
            del key_values[key]
            return (key, id_value)
    raise ValueError("No matching_id given")

def add_fields(key_values, config, marc):
    # Loop through all arguments left after determining the matching id and add
    #   a field for each datafield.
    for key in key_values:
        # All keys left must be in data and not in matching-ids
        if not key in config["data"]:
            raise ValueError
        data_value = key_values[key]
        validate_value(config["data"][key]["validation-regex"], data_value)
        marc.add_field(config["data"][key], data_value)

def write_xml_file(config, marc):
    # Open a file object to pass on to ElementTree.write()
    # This implements an SFTP client and a local path.
    file = None
    filename = f'{int(time.time())}.xml'
    path = f'{config["target_path"]}{filename}'

    if config['target_type'] == 'sftp':
        sftp_settings = load_sftp_settings(config['sftp_settings_file'])
        sftp = SFTPClient(sftp_settings['server'], key_filename=sftp_settings['key_filename'], username=sftp_settings['username'], password=sftp_settings['password'])
        with sftp.open(path) as file:
            marc.write_xml(file)
    else:
        with open(path, 'wb') as file:
            marc.write_xml(file)

def load_sftp_settings(settings_file):
    with open(settings_file, 'r') as settingsfile:
        return json.load(settingsfile)

def main():
    args = read_args()
    config = load_config(args.config)
    key_values = args.kwargs
    matching_id_key, matching_id_value = find_matching_id(key_values, config)
    marc = MarcSnippet()
    marc.add_field(config["matching-ids"][matching_id_key], matching_id_value)
    add_fields(key_values, config, marc)
    write_xml_file(config, marc)

if __name__ == "__main__":
    main()