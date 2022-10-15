import json
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
config = {}
config = json.load(open(config_path, 'r', encoding='utf8'))

def get_config(key, sub_key):
	if key in config and sub_key in config[key]:
		return config[key][sub_key]
	return None