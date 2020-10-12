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
