import os
import time
import subprocess
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
        mylog = subprocess.run(['gcloud compute reservations list --format="json"'], stdout=subproces.PIPE)
        mylog.stdout.decode('utf-8')
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
           gauge = GaugeMetricFamily("michelcars", 'Help text', labels=['michelspecificcar'])
           gauge.add_metric([str(key['vehicle'])], float(key['value']))
           yield gauge

if __name__ == '__main__':
    try:
        gcloud_project_id = os.environ['GCP_PROJECT_ID']
    except KeyError:
        print('GCP_PROJECT_ID must be defined')
        sys.exit(1)

    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(10)
