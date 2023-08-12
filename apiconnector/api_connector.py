__author__ = 'William Souza Alves'
__version__ = '0.1.0'

import json


class ApiConnector:
    
    def get_config_data():
        with open('test/response.json', 'r') as file:
            return json.load(file)
        
    def post_result_data(data: dict):
        with open(f'test/response2.json', 'w') as file:
            json.dump(data, file)