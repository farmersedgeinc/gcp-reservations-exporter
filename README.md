# GCP Reservations Exporter

This exporter will query the Google Cloud Platform machine reservations and export the results into Prometheus.

The Prometheus gauge will be called `gcp_reservation_utilization` and is the ratio of reservation "inUseCount"
divided by "count" of the total machines reserved.  An alert will be generated for reservations where the utilization
is less than 10%.

## Exporter

This exporter will basically issue a `gcloud compute reservations list` call (via `Gcp_reservations` service account) to
gather utilization numbers for each reservation, and then format these into a Prometheus gauge called `gcp_reservations_utilization`
where the label is the machine reservation name, and the value is a float of `reservation inUseCount` divided by `reservation count`.

## Notes

Currently the `gcp-quota-exporter` does collect the `gcloud_reservations_quota_usage` and `gcloud_reservations_quota_ratio` metrics
by GCP Project.  This however only shows how many reservations you have in a project, and how close you are to filling the
quota of how many reservations you are allowed per project.  This does NOT give you any utilzation details of said reservations.

**Cheers!**
