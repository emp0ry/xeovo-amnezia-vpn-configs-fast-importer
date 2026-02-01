import configparser
import json
import os
import tkinter as tk
from tkinter import filedialog

def parse_conf_file(conf_path):
    # Initialize config parser
    config = configparser.ConfigParser()
    config.read(conf_path)
    
    # Dictionary to store parsed data
    parsed_data = {}
    
    # Parse Interface section
    if 'Interface' in config:
        interface = config['Interface']
        parsed_data['Address'] = interface.get('Address', '')
        parsed_data['PrivateKey'] = interface.get('PrivateKey', '')
        parsed_data['DNS'] = interface.get('DNS', '')
        parsed_data['Jc'] = interface.get('Jc', '')
        parsed_data['Jmin'] = interface.get('Jmin', '')
        parsed_data['Jmax'] = interface.get('Jmax', '')
        parsed_data['S1'] = interface.get('S1', '')
        parsed_data['S2'] = interface.get('S2', '')
        parsed_data['H1'] = interface.get('H1', '')
        parsed_data['H2'] = interface.get('H2', '')
        parsed_data['H3'] = interface.get('H3', '')
        parsed_data['H4'] = interface.get('H4', '')
    
    # Parse Peer section
    if 'Peer' in config:
        peer = config['Peer']
        parsed_data['PublicKey'] = peer.get('PublicKey', '')
        parsed_data['AllowedIPs'] = peer.get('AllowedIPs', '')
        parsed_data['Endpoint'] = peer.get('Endpoint', '')
    
    return parsed_data

def open_explorer():
    # Initialize tkinter root
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Open file dialog to select .conf file
    conf_path = filedialog.askopenfilename(
        title="Select .conf file",
        filetypes=[("Configuration files", "*.conf"), ("All files", "*.*")]
    )
    
    # Destroy the root window
    root.destroy()
    
    return conf_path

def create_amnezia_backup(conf_data, output_path, conf_path):
    # Define all server locations
    locations = {
        'al': 'Albania, Tirana',
        'au': 'Australia, Sydney',
        'br': 'Brazil, São Paulo',
        'ca': 'Canada, Montreal',
        'ch': 'Switzerland, Zurich',
        'de': 'Germany, Falkenstein',
        'fi': 'Finland, Helsinki',
        'fr': 'France, Paris',
        'jp': 'Japan, Tokyo',
        'lu': 'Luxembourg, Roost',
        'lv': 'Latvia, Riga',
        'nl': 'Netherlands, Amsterdam',
        'no': 'Norway, Sandefjord',
        'pl': 'Poland, Warsaw',
        'ro': 'Romania, Iasi',
        'se': 'Sweden, Stockholm',
        'sg': 'Singapore, Singapore',
        'ua': 'Ukraine, Kyiv',
        'uk': 'United Kingdom, London',
        'us-lv': 'United States, Las Vegas',
        'us-mia': 'United States, Miami',
        'us-nyc': 'United States, New York',
        'random': 'Random'
    }

    # Read the original .conf file content
    with open(conf_path, 'r') as f:
        conf_content = f.read()

    # Create servers list
    servers_list = []
    for code, description in locations.items():
        host_name = f"{code}.gw.xeovo.com"
        port = conf_data['Endpoint'].split(':')[1] if ':' in conf_data['Endpoint'] else "51820"
        
        # Update the Endpoint in the conf_content for this server
        updated_conf_content = conf_content.replace(
            conf_data['Endpoint'],
            f"{host_name}:{port}"
        ) if conf_data['Endpoint'] in conf_content else conf_content
        
        # Create last_config for each server
        last_config = {
            "H1": conf_data['H1'],
            "H2": conf_data['H2'],
            "H3": conf_data['H3'],
            "H4": conf_data['H4'],
            "Jc": conf_data['Jc'],
            "Jmax": conf_data['Jmax'],
            "Jmin": conf_data['Jmin'],
            "S1": conf_data['S1'],
            "S2": conf_data['S2'],
            "allowed_ips": conf_data['AllowedIPs'].split(', '),
            "client_ip": conf_data['Address'],
            "client_priv_key": conf_data['PrivateKey'],
            "config": updated_conf_content.replace('\n', '\\n'),
            "hostName": host_name,
            "mtu": "1376",
            "port": int(port),
            "server_pub_key": conf_data['PublicKey']
        }

        server_entry = {
            "containers": [
                {
                    "awg": {
                        "isThirdPartyConfig": True,
                        "last_config": json.dumps(last_config, indent=4).replace('\n', '\n' + ' ' * 4),
                        "port": port,
                        "transport_proto": "udp"
                    },
                    "container": "amnezia-awg"
                }
            ],
            "defaultContainer": "amnezia-awg",
            "description": description,
            "hostName": host_name
        }
        servers_list.append(server_entry)

    # Convert servers_list to a JSON string with proper formatting
    servers_list_str = json.dumps(servers_list, indent=4).replace('\n', '\n')

    # Create the AmneziaVPN.backup structure
    backup_data = {
        "Conf/appLanguage": None,
        "Conf/appsRouteMode": 2,
        "Conf/encrypted": "true",
        "Conf/routeMode": 1,
        "Conf/sitesSplitTunnelingEnabled": False,
        "Servers/defaultServerIndex": 0,
        "Servers/serversList": servers_list_str
    }

    # Write to AmneziaVPN.backup file
    with open(output_path, 'w') as f:
        json.dump(backup_data, f, indent=4)

def main():
    # Open file explorer to select file
    global conf_path
    conf_path = open_explorer()
    
    if not conf_path:
        print("No file selected")
        return
    
    if not os.path.exists(conf_path):
        print(f"Error: File {conf_path} does not exist")
        return
    
    # Parse the conf file
    data = parse_conf_file(conf_path)
    
    # Print parsed data
    print("\nParsed Configuration Data:")
    print("-" * 50)
    for key, value in data.items():
        print(f"{key}: {value}")
    
    # Create AmneziaVPN.backup file
    output_path = "AmneziaVPN.backup"
    create_amnezia_backup(data, output_path, conf_path)
    print(f"\nAmneziaVPN.backup file created at: {output_path}")

if __name__ == "__main__":
    main()

# Build example:
# pyinstaller --icon=icon.ico --distpath ./ --workpath ./build --clean -F --noconsole -n "XeovoAmneziaVPNImporter" --add-data "icon.ico;." --upx-dir=upx main.py
