from circuitbreaker import circuit
import requests

@circuit(failure_threshold=3, recovery_timeout=10)
def communicate(method, url, body=None):
    if body is not None:
        response = requests.request(method, url, json=body)
    else:
        response = requests.request(method, url)
    if response.status_code == 200:
        return response.json()


