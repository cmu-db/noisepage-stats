from datetime import datetime
from pss_project.settings.utils import get_environ_value

service_start_time = datetime.now()

# Query mode validation
SIMPLE_MODE = 'simple'
EXTENDED_MODE = 'extended'
QUERY_MODE_CHOICES = [
    (SIMPLE_MODE, 'simple'),
    (EXTENDED_MODE, 'extended'),
]

# WAL device validation
RAM_DISK = 'RAM disk'
HDD = 'HDD'
SATA_SSD = 'SATA SSD'
NVME_SSD = 'NVMe SSD'
NONE = 'None'
WAL_DEVICE_CHOICES = [
    (RAM_DISK, 'RAM disk'),
    (HDD, 'HDD'),
    (SATA_SSD, 'SATA SSD'),
    (NVME_SSD, 'NVMe SSD'),
    (NONE, 'None')
]

# Microbenchmark status validation
PASS = 'PASS'
FAIL = 'FAIL'
MICROBENCHMARK_STATUS_CHOICES = [
    (PASS, 'PASS'),
    (FAIL, 'FAIL')
]

# Github Integration
GITHUB_APP_ID = 86997
ALLOWED_EVENTS = ['pull_request', 'status']
# The status context that is sent when the Jenkins pipeline finishes
CI_STATUS_CONTEXT = 'continuous-integration/jenkins/pr-merge'
GITHUB_APP_WEBHOOK_SECRET = get_environ_value('GITHUB_APP_WEBHOOK_SECRET')
GITHUB_APP_PRIVATE_KEY = get_environ_value('GITHUB_APP_PRIVATE_KEY')

GITHUB_WEBHOOK_HASH_HEADER = 'HTTP_X_HUB_SIGNATURE_256'
GITHUB_EVENT_HEADER = 'HTTP_X_GITHUB_EVENT'

# Github NoisePage Client
REPO_OWNER = 'cmu-db'
REPO_NAME = 'noisepage'
GITHUB_BASE_URL = 'https://api.github.com/'

MASTER_BRANCH_NAME = 'origin/master'
