"""
This module will query (and render as a Prometheus Guage metric) the utilization of GCP machine
reservations.

References:
  https://www.gspann.com/resources/blogs/developing-custom-exporter-for-prometheus-using-python/
  https://github.com/prometheus/client_python
  https://stackoverflow.com/questions/59954984/prometheus-python-exporter-for-json-values

Testing:
  Create your venv, and collect locally with `curl http://127.0.0.1:8003`
"""
import os
import time
import sys
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
# References:
# https://www.gspann.com/resources/blogs/developing-custom-exporter-for-prometheus-using-python/
# https://github.com/prometheus/client_python
# https://stackoverflow.com/questions/59954984/prometheus-python-exporter-for-json-values

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
