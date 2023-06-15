import subprocess
from config import SERIAL, S3_ENDPOINT
import requests
from importlib import __import__


class Component:
    def __init__(self, config):
        try:
            print(config['library'])
            lib = __import__(config['library'] + '_instance')
        except Exception as e:
            print(e)
            whl = requests.get(S3_ENDPOINT + config['library'] + '.whl', allow_redirects=True)
            lib_name = whl.url.split('/')[-1]
            open('libs/' + lib_name, 'wb').write(whl.content)
            self.__install_package('libs/' + lib_name)

    @staticmethod
    def __install_package(package_name):
        try:
            # Use the pip command to install the package
            subprocess.check_call(['pip', 'install', package_name])
            print(f"Successfully installed {package_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package_name}: {e}")
            exit(0)
