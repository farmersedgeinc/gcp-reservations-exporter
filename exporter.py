"""
This module will query (and render as a Prometheus Guage metric) the utilization of GCP machine
reservations.

References:
  https://www.gspann.com/resources/blogs/developing-custom-exporter-for-prometheus-using-python/
  https://github.com/prometheus/client_python
  https://stackoverflow.com/questions/59954984/prometheus-python-exporter-for-json-values

Testing:
1. Set up the GCP Service account locally in `/service-account/gcp_reservations_sa.json`, as
   found in the helm charts.
2. Create your venv:
   python -m virtualenv myenv
   source myenv/bin/activate
   GCP_PROJECT_ID=test-4f727257h6h
   export GCP_PROJECT_ID
   GCP_APPLICATION_CREDENTIALS=/service-account/gcp_reservations_sa.json
   export GCP_APPLICATION_CREDENTIALS
   pip install prometheus_client
   python ./exporter.py
   (run `deactivate` once you are done)
3. Collect locally with `curl http://127.0.0.1:8003`
4. Note that since the service account is now being used, to restore your normal gcloud
   account and functionality you will need to `gcloud auth revoke` and `gcloud auth login` again.
"""
import os
import time
import sys
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

class CustomCollector():
    """
    This class determines the utilization ration of 'reservations in current use' divided
    by 'reservations available'.
    """
    def __init__(self):
        pass

    def collect(self):
        """ Note that google project-id is set before we list the reservations."""
        os.system('gcloud compute reservations list \
            --format="csv(name,specificReservation.count,specificReservation.inUseCount)" \
            | tail -n +2 > /tmp/list.csv')
        csvfile = open('/tmp/list.csv','r')
        for line in csvfile:
            chopline = line.rstrip()
            arr = chopline.split(',')
            reservation_name =  arr[0]
            utilization = float(arr[2]) / float(arr[1])
            gauge = GaugeMetricFamily("gcp_reservations", 'Help text', labels=['reservation'])
            gauge.add_metric([reservation_name],utilization)
            yield gauge
        csvfile.close()

if __name__ == '__main__':
    try:
        activate_service_account_cmd = 'gcloud auth activate-service-account --key-file ' + \
            os.environ['GCP_APPLICATION_CREDENTIALS'] + ' 2>&1'
        os.system(activate_service_account_cmd)
    except KeyError:
        print('Failed to activate GCP Service Account')
        sys.exit(1)

    try:
        set_project_cmd = 'gcloud config set project ' + os.environ['GCP_PROJECT_ID']
        os.system(set_project_cmd)
    except KeyError:
        print('GCP_PROJECT_ID must be defined')
        sys.exit(1)

    print('Start metrics http server on port 8003')
    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(10)

# Cheers!
