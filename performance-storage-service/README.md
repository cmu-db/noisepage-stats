# Performance Storage Service

[![Test Build Status][test_build_badge_url]][test_build_url]
[![Staging Build Status][staging_build_badge_url]][staging_build_url]
[![Test Build Status][master_build_badge_url]][master_build_url]

This serivce will be used to accept data from the Jenkins pipeline and store it in TimeScaleDB.

## API Documentation
The openapi.yaml file documents all the endpoints of the API


## Related Kubernetes Files
`/deployments/kubernetes/performance/performance-storage-service/*`

`/deployments/kubernetes/namespaces.yml`

`/deployments/playbooks/pss-deployment.yml`

`/deployments/playbooks/create-namespaces.yml`


## Running Locally

### Running Locally - Django runserver

```bash
source env/bin/activate

# install requirements
pip install -r requirements.txt

# download docker container if you don't already have it
# docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12

# start timescale docker container
docker start timescaledb

python manage.py runserver

docker stop timescaledb
```

### Running locally - Kubernetes
Make sure you have docker desktop, and ansible installed.

#### Prerequisite
Make sure your docker-desktop kubernetes node is labeled with `env=local`.

To do this run `kubectl label nodes docker-desktop env=local`

#### Execution
```bash
docker build -t cmudb/performance-storage-service:latest .

ansible-playbook -i inventory playbooks/create-namespaces.yml -e "env=local host_override=local"

ansible-playbook -i inventory playbooks/pss-deployment.yml -e "env=local host_override=local pss_db_user=postgres pss_db_password=password"
```
To verify try hitting `http://localhost:31000/performance-results/health`

To delete the local deployment
```
kubectl delete pods,service,deployment -n performance --all
```

## Contributing
### Testing
To run tests, generate coverage report, and generate static analysis reports run:
```bash
python manage.py jenkins --enable-coverage --coverage-rcfile=.coveragerc
```

### Code Quality
Before committing be sure to review and resolve issues in `/reports/pep8.report`. For simple fixes you can autofix by running:
`autopep8 pss_project --recursive --in-place`. If you just want to autofix a single file run: `autopep8 pss_project/<path-to-file> --in-place` 


<!-- Reference Links -->
[test_build_badge_url]: http://jenkins.db.cs.cmu.edu:8080/buildStatus/icon?job=testing-team%2Fnoisepage-test-performance-storage-service%2Ftest
[test_build_url]: http://jenkins.db.cs.cmu.edu:8080/job/testing-team/job/noisepage-test-performance-storage-service/job/test/

[staging_build_badge_url]: http://jenkins.db.cs.cmu.edu:8080/buildStatus/icon?job=testing-team%2Fnoisepage-test-performance-storage-service%2Fstaging
[staging_build_url]: http://jenkins.db.cs.cmu.edu:8080/job/testing-team/job/noisepage-test-performance-storage-service/job/staging/

[master_build_badge_url]: http://jenkins.db.cs.cmu.edu:8080/buildStatus/icon?job=testing-team%2Fnoisepage-test-performance-storage-service%2Fmaster
[master_build_url]: http://jenkins.db.cs.cmu.edu:8080/job/testing-team/job/noisepage-test-performance-storage-service/job/master/

