# Deployment
This folder contains all 

## Tech stack
- [Docker](https://docs.docker.com/): for the containerization
- [Kubernetes](https://kubernetes.io/docs/home/): container orchestraction platform
- [Ansible](https://docs.ansible.com/ansible/latest/index.html): remote deployment executor
- [OpenResty](https://openresty.org/en/): for the web proxy

## File structures
- `kubernetes/`: config files for kubernetes
  - `monitoring/`: monitoring namespace, which monitor the testing infrastructur itself
    - `blackbox_exporter/`: for generic HTTP service prometheus exporter
    - `grafana/`: for grafana monitoring dashboards
    - `postgres_exporter/`: for PostgreSQL database prometheus exporter
    - `prometheus/`: for prometheus TSDB of the testing infrastructure
  - `performance`: testing infrastructure services
    - `grafana/`: for grafana monitoring dashboards of the testing data
    - `openapi/`: for the OpenAPI documentation of the Django API
    - `performance-storage-service/`: the Django API web service which collect and validate testing results
    - `timescaledb`: the TimeScale DB for storing the testing results
  - `namespaces.yml`: defines the namespaces for the kubernetes cluster
- `playbooks/`: contains all the [ansible playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html), which are the invocation points for all the deployment tasks
- `roles/`: contains all the [ansible roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html), which are used directly by the [ansible playbooks](https://github.com/cmu-db/noisepage-stats/tree/master/deployments/playbooks) above
- `scripts/`: contains shell scripts which are used during the deployments
- `ansible.cfg`: the project-wide [configuration of ansible](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings)
- `inventory`: the [INI style configuration](https://docs.ansible.com/ansible/2.9_ja/plugins/inventory/ini.html) of the ansible hosts and vars
- `Jenkinsfile`: the configuration of Jenkins pipeline, which defines the CD processes

## Quick guide to deployments

### How to add a namespace [optional]
-  Normally, you do **NOT** need to do it, because all the testing infrastructure services should be under `performance` and all the monitoring services of the testing infrastructure should be under `monitoring`.
- If you really need to add a new namespace for the kubernetes
  - Declare the namespace of your service in the `namespaces.yml`
  - Trigger the CD by pushing your code changes to the GitHub. The Jenkins should pick up the change and run the following command to execute the change.
  ```bash
  ansible-playbook -i inventory playbooks/create-namespaces.yml
  ```

### To deploy a service for testing infrastructure
- Create a service in `kubernetes/performance/`. In that folder
  - [optional] Create config files if necessary, which may include
    - `config-map.yml`: for file-based service configuration
    - `persistent-volume.yml`: for Kubernetes persistent volume declaration
    - `persistent-volume-claim.yml`: for Kubernetes persistent volume claim
  - Create a deployment config file
    - Create a `deployment.yml` if it is a stateless service
    - Create a `statefulset.yml` if it is a stateful service
  - Create a service config file, which serves as the proxy of the service
    - Use `NodePort` by default
- Create an ansible playbook in `playbooks/` as the invocation point of the deployment of your service
- [optional] Add your service public port as a new [NGINX location in OpenResty config](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) if your service has a public HTTP endpoint
- [optional] Add ansible roles to `roles/` for any additional roles created for your service
- [optional] Add any ansible vars to `inventory` that are specific to your service deployment


