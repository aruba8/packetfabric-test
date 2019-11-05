import requests
from faker import Faker

from util import generate_url

fake = Faker()
endpoint = '/contacts'


def test_create_contact():
    contact_first_name = fake.first_name()
    contact_last_name = fake.last_name()
    contact_email = fake.email()
    contact_phone = fake.msisdn()
    contact_address1 = fake.address()
    contact_city = fake.city()
    contact_state = fake.state()
    contact_country = fake.country_code(representation="alpha-3")
    contact_postal = fake.postalcode()
    url = generate_url(endpoint)
    params = {
        'contact_first_name': contact_first_name,
        'contact_last_name': contact_last_name,
        'contact_email': contact_email,
        'contact_phone': contact_phone,
        'contact_address1': contact_address1,
        'contact_city': contact_city,
        'contact_state': contact_state,
        'contact_country': contact_country,
        'contact_postal': contact_postal
    }
    resp = requests.post(url, json=params, verify=False)
    resp_json = resp.json()
    # should return 200 according to docs?
    assert resp.status_code == 201
    assert resp_json['contact_first_name'] == contact_first_name
    assert resp_json['contact_last_name'] == contact_last_name
    assert resp_json['contact_email'] == contact_email
    assert resp_json['contact_phone'] == contact_phone
    assert resp_json['contact_address1'] == contact_address1
    assert resp_json['contact_city'] == contact_city
    assert resp_json['contact_state'] == contact_state
    assert resp_json['contact_country'] == contact_country
    assert resp_json['contact_postal'] == contact_postal
