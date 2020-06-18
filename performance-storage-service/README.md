# Performance Storage Service

This serivce will be used to accept data from the Jenkins pipeline and store it in TimeScaleDB.

### API Documentation
The openapi.yaml file documents all the endpoints of the API


### Related Kubernetes Files
`/deployments/kubernetes/performance/performance-storage-service/*`

`/deployments/kubernetes/namespaces.yml`

`/deployments/playbooks/pss-deployment.yml`

`/deployments/playbooks/create-namespaces.yml`


### Running locally
Make sure you have docker desktop, and ansible installed.

#### Prerequisite
Make sure your docker-desktop kubernetes node is labeled with `env=local`.

To do this run `kubectl label nodes docker-desktop env=local`

#### Execution
```bash
docker build -t cmudb/performance-storage-service:latest .

ansible-playbook -i inventory playbooks/create-namespaces.yml -e "env=local host_override=local"

ansible-playbook -i inventory playbooks/pss-deployment.yml -e "env=local host_override=local"
```
To verify try hitting `http://localhost:31000/health`

To delete the local deployment
```
kubectl delete pods,service,deployment -n performance --all
```
