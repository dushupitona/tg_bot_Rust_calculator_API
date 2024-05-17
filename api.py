import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

def get_valid_objects():
    try:
        response = requests.get('http://localhost:8000/api/objects/')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None
        

def get_valid_tools():
    try:
        response = requests.get('http://localhost:8000/api/tools/')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None


def calculate(data):
    object_id = [_.get('id') for _ in get_valid_objects() if _['obj_name'].lower() == data['chosen_object']][0]
    tool_id = [_.get('id') for _ in get_valid_tools() if _['tool_name'].lower() == data['chosen_tool']][0]
    quantity = data['chosen_quan']
    req_data = {
        'obj_id': object_id,
        'tool_id': tool_id,
        'value': quantity
    }

    try:
        response = requests.post('http://localhost:8000/api/calculate/', json=req_data)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None
    


