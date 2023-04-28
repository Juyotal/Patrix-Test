import json

def test_request(api):
    response = api.test_client().get('/api/2021/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data.get("MRData").get("RaceTable").get("season") == "2021"
    assert data.get("MRData").get("RaceTable").get("round") == "1"
    

def test_request_with_date_out_of_range(api):
    response = api.test_client().get('/api/1949/1')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {
            'status': 'error',
            'message': f'No data exists for the year 1949'
        }


def test_request_with_round_out_of_range(api):
    response = api.test_client().get('/api/2021/100')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {
            'status': 'error',
            'message': f'Round 100 does not exist for the year 2021'
        }