# Performance Storage Service

This serivce will be used to accept data from the Jenkins pipeline and store it in TimeScaleDB.

### API Documentation
The openapi.yaml file documents all the endpoints of the API


### Related Kubernetes Files
`/kubernetes/performance/performance-storage-service/*`

`/kubernetes/performance/service.yml`


### Running locally
Make sure you have docker desktop, and ansible installed.

Run
```bash
kubectl apply -f ../kubernetes/namespaces.yml

docker build -t cmudb/performance-storage-service:latest .

ansible-playbook -i inventory playbooks/pss-deployment.yml -e "env=local container_name=cmudb/performanc
e-storage-service"
```
To verify try hitting `http://localhost:30001/health`

To delete the local deployment
```
kubectl delete pods,service,deployment -n performance --all
```
