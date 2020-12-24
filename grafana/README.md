# Grafana

Grafana will be used by NoisePage to query, visualize, and understand the metrics that stored in TimeScaleDB

### Related Deployment Files
`/deployments/kubernetes/performance/grafana/*`

`/deployments/kubernetes/namespaces.yml`

`/deployments/playbooks/grafana-deployment.yml`

`/deployments/playbooks/create-namespaces.yml`



### Running locally
Make sure you have docker desktop, and ansible installed.

#### Prerequisite
Make sure your docker-desktop kubernetes node is labeled with `env=local`.

To do this run `kubectl label nodes docker-desktop env=local`

#### Execution
```bash
ansible-playbook -i inventory playbooks/create-namespaces.yml -e "env=local host_override=local"

ansible-playbook -i inventory playbooks/grafana-deployment.yml -e "env=local host_override=local"
```
To verify try opening a browser to `http://localhost:32000/`

To delete the local deployment
```
kubectl delete pods,service,deployment -n performance --all
```

### Create a dashboard
Check the document here: https://grafana.com/docs/grafana/latest/getting-started/getting-started/#step-3-create-a-dashboard

Be sure to **store** the dashboard JSON Model into the folder: [noisepage-stats/grafana/dashboards/](https://github.com/cmu-db/noisepage-stats/tree/master/grafana/dashboards)
