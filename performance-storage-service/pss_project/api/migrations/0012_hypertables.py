from django.db import migrations
from django.db.migrations.operations.special import RunSQL


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_auto_20210105_1158"),
    ]

    operations = [
        migrations.RunSQL("SELECT create_hypertable('artifact_stats_results', 'time', chunk_time_interval => INTERVAL '30 days', migrate_data => TRUE);"),
        migrations.RunSQL("SELECT create_hypertable('oltpbench_results', 'time', chunk_time_interval => INTERVAL '30 days', migrate_data => TRUE);"),
        migrations.RunSQL("SELECT create_hypertable('microbenchmark_results', 'time', chunk_time_interval => INTERVAL '30 days', migrate_data => TRUE);"),
    ]
