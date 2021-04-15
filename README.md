# GCP Reservations Exporter

This exporter will query the Google Cloud Platform machine reservations and export the results into Prometheus.

The Prometheus gauge will be called `gcp_reservation_utilization` and is the ratio of reservation "inUseCount"
divided by "count" of the total machines reserved.  An alert will be generated for reservations where the utilization
is less than 10%.

**Cheers!**
