#!/usr/bin/env python3

import warnings
warnings.simplefilter("ignore")

import paramiko
import configparser
import argparse
import sys
import getpass
import warnings
import re

REMOTE_CONFIG_PATH = "/data/xochitl.conf"

def read_html_file(html_path):
    """Reads the contents of the HTML file we are inserting into the conf file."""
    try:
        with open(html_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        sys.exit(1)

def ssh_connect(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    password = getpass.getpass("Enter SSH password: ").strip()
    
    try:
        client.connect(host, username="root", password=password, look_for_keys=False, allow_agent=False)
        return client
    except paramiko.AuthenticationException:
        print("SSH password authentication failed.")
        sys.exit(1)
    except Exception as e:
        print(f"SSH connection failed: {e}")
        sys.exit(1)

def modify_xochitl_config(client, html_content, reset=False):
    """Fetches, modifies, and uploads the xochitl.conf file while preserving structure."""
    try:
        sftp = client.open_sftp()
        remote_file = sftp.open(REMOTE_CONFIG_PATH, "r")
        config_data = remote_file.read().decode("utf-8")
        remote_file.close()

        if reset:
            print("Resetting IdleContact and IdleName to blank values...")
            config_data = re.sub(r'(?<=\n)IdleContact=.*', 'IdleContact=""', config_data)
            config_data = re.sub(r'(?<=\n)IdleName=.*', 'IdleName=""', config_data)
        else:
            # uncomment to replace IdleName as well
            single_line_html = html_content.replace("\n", "").replace('"', '\\"')
            config_data = re.sub(r'(?<=\n)IdleContact=.*', f'IdleContact="{single_line_html}"', config_data)
            # config_data = re.sub(r'(?<=\n)IdleName=.*', f'IdleName="{single_line_html}"', config_data)

        temp_file = "/tmp/xochitl.conf"
        remote_temp_file = sftp.open(temp_file, "w")
        remote_temp_file.write(config_data)
        remote_temp_file.close()

        client.exec_command(f"mv {temp_file} {REMOTE_CONFIG_PATH}")

        print("xochitl.conf successfully updated.")

        print("Restarting xochitl service...")
        client.exec_command("systemctl restart xochitl")

        print("xochitl service restarted successfully.")

    except Exception as e:
        print(f"Error modifying xochitl.conf: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Update xochitl.conf on reMarkable tablet.")
    parser.add_argument("-i", "--ip", help="IP address of reMarkable tablet")
    parser.add_argument("-f", "--file", help="Path to the HTML file to insert")
    parser.add_argument("--reset", action="store_true", help="Reset IdleContact and IdleName to blank values")
    args = parser.parse_args()

    host = args.ip if args.ip else input("Enter the reMarkable's IP address: ")

    if not args.reset and not args.file:
        print("Error: You must provide an HTML file with -f or use --reset to clear values.")
        sys.exit(1)

    html_content = read_html_file(args.file) if args.file else ""

    client = ssh_connect(host)

    modify_xochitl_config(client, html_content, reset=args.reset)

    client.close()

if __name__ == "__main__":
    main()