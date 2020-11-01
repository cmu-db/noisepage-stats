from pss_project.settings.utils import get_environ_value

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
GITHUB_APP_IDENTIFIER = 86997
ALLOWED_EVENTS = ['pull_request', 'status']
CI_STATUS_CONTEXT = 'continuous-integration/jenkins/pr-merge'
WEBHOOK_SECRET = get_environ_value('WEBHOOK_SECRET')
GITHUB_WEBHOOK_HASH_HEADER = 'HTTP_X_HUB_SIGNATURE_256'
GITHUB_PRIVATE_KEY = get_environ_value('GITHUB_PRIVATE_KEY')
PERFORMANCE_COP_CHECK_NAME = 'performance-cop'

#Github NoisePage Client
REPO_OWNER = 'cmu-mse-cmudb' #TODO: change these after a test
REPO_NAME = 'terrier' #TODO: change these after a test
GITHUB_BASE_URL = 'https://api.github.com/'