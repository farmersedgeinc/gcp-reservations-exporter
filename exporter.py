import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
### import requests
import json

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        # response = requests.get('https://api.test.com/v1/data', auth= ('abc@gg.com', 'xxrty'))
        # Start with this, then try the json output of the `gcloud compute reservations list --format="json"`
        d1 = {
            "garage": [
                {
                "vehicle": "jeep",
                "value": "1.0"
                },
                {
                "vehicle": "chevrolet",
                "value": "0.75"
                },
                {
                "vehicle": "honda",
                "value": "0.50"
                },
                {
                "vehicle": "plymouth",
                "value": "0.25"
                }
            ]
        }
        list_of_metrics = d1["garage"]
        for key in list_of_metrics:
           g = GaugeMetricFamily("michelcars", 'Help text', labels=['michelspecificcar'])
           g.add_metric([str(key['vehicle'])], key['value'])
           yield g

if __name__ == '__main__':
    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(10)
