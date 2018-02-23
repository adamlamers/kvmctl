import os
import json
import sys

class Configuration(object):

    DEFAULTS = {
            'KVM_URI': ''
            }

    def __init__(self, path):
        self.path = os.path.expanduser(path)

    @property
    def data(self):
        try:
            with open(self.path, 'r') as f:
                data = json.loads(f.read())
                if not data:
                    return Configuration.DEFAULTS
                return data
        except ValueError as e:
            print("Error loading configuration: {}".format(e))
            sys.exit(1)
        except FileNotFoundError:
            return Configuration.DEFAULTS

    def save(self, data):
        try:
            with open(self.path, 'w') as f:
                f.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            os.makedirs(os.path.dirname(self.path))
            self.save(data)

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, val):
        data = self.data
        data[key] = val

        self.save(data)
