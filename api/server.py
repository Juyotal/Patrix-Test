from flask import Flask, request, jsonify
import json
from flask_swagger_ui import get_swaggerui_blueprint
import sys
import requests
import xmltodict
from functools import wraps

app = Flask(__name__)

SWAGGER_URL = '/api/'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "F1 API"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def remove_symbols(json_dict):
    updated_dict = {}
    for key, value in json_dict.items():
        if isinstance(value, dict):
            value = remove_symbols(value)
        elif isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict):
                    item = remove_symbols(item)
                new_value.append(item)
            value = new_value
        if key.startswith('@') or key.startswith('#'):
            new_key = key[1:]
            updated_dict[new_key] = value
        else:
            updated_dict[key] = value
    return updated_dict


def xml_to_dict(xml_data):
    try:
        data_dict = xmltodict.parse(xml_data)
    except xmltodict.expat.ExpatError as e:
        error_msg = f"Error parsing XML data: {e}"
        return (jsonify({'error': error_msg}), 400)
    
    data_dict = remove_symbols(data_dict)
    return data_dict


def transform_xml_to_json(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        year = request.view_args.get('year')
        round = request.view_args.get('round')
        if year < 1950 or year > 2023:
            response = {
                'status': 'error',
                'message': f'No data exists for the year {year}'
            }
            return jsonify(response), 404
        if round < 1 or round > 99:
            response = {
                'status': 'error',
                'message': f'Round {round} does not exist for the year {year}'
            }
            return jsonify(response), 404
        api_url = f"http://ergast.com/api/f1/{year}/{round}/results"
        try:
            data = requests.get(api_url).content
        except requests.exceptions.RequestException as e:
            return jsonify(f'API request failed due to {str(e)}'), 500
    
        data_dict = xml_to_dict.parse(data)

        try:
            kwargs["json_data"] = json.dumps(data_dict)
        except xmltodict.expat.ExpatError as e:
            error_msg = f"Error encoding JSON data: {e}"
            return (jsonify({error_msg}), 500)
        
        return func(*args, **kwargs)
    return decorator


@app.route('/api/<int:year>/<int:round>', methods=['GET'])
@transform_xml_to_json
def query_results(year, round, json_data):
    if json.loads(json_data).get("MRData").get("total") == "0":
        response = {
            'status': 'error',
            'message': f'Round {round} does not exist for the year {year}'
        }
        return jsonify(response), 404
    return json_data, 200



if __name__ == '__main__':
    app.run(debug=True, port=5000)