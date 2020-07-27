import pytest
import jsonpickle

from urllib.parse import quote_plus

from ..common import save_words_list_classification, assert_issues_count_is_zero
from ..configuration import ENDPOINT_PATH
from ...common import token_header, claims


@pytest.mark.xfail(raises=ValueError)
def test_designation_existence_request_response(client, jwt, app):
    words_list_classification = [{'word': 'ARMSTRONG', 'classification': 'DIST'},
                                 {'word': 'ARMSTRONG', 'classification': 'DESC'},
                                 {'word': 'PLUMBING', 'classification': 'DIST'},
                                 {'word': 'PLUMBING', 'classification': 'DESC'}]
    save_words_list_classification(words_list_classification)
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    test_params = [
        {
            'name': 'ARMSTRONG PLUMBING LTD.',
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'CHG'
        },
        {
            'name': 'ARMSTRONG PLUMBING LTD.',
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'DBA'
        },
        {
            'name': 'ARMSTRONG PLUMBING LTD.',
            'location': 'BC',
            'entity_type': 'CR',
            'request_action': 'NEW'
        }
    ]

    for entry in test_params:
        query = '&'.join("{!s}={}".format(k, quote_plus(v)) for (k, v) in entry.items())
        path = ENDPOINT_PATH + '?' + query
        print('\n' + 'request: ' + path + '\n')
        response = client.get(path, headers=headers)
        payload = jsonpickle.decode(response.data)
        print("Assert that the payload contains issues")
        if isinstance(payload.get('issues'), list):
            assert_issues_count_is_zero(payload.get('issues'))
