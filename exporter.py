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
        # reslist = subprocess.Popen(['gcloud', 'compute', 'reservations', 'list', '--format="json"'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # reslist = subprocess.Popen(['gcloud compute reservations list --format="json"'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #stdout,stderr = reslist.communicate()
        #print(stdout)
        cmd = 'gcloud compute reservations list --format="json"'
        os.system(cmd)
        
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
           print('metrics')
           gauge = GaugeMetricFamily("michelcars", 'Help text', labels=['michelspecificcar'])
           gauge.add_metric([str(key['vehicle'])], float(key['value']))
           yield gauge

if __name__ == '__main__':
    try:
        print('hello');
        gcloud_project_id = os.environ['GCP_PROJECT_ID']
    except KeyError:
        print('GCP_PROJECT_ID must be defined')
        sys.exit(1)
    
    print('start http server')
    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    print('registry')
    while True:
        time.sleep(10)
