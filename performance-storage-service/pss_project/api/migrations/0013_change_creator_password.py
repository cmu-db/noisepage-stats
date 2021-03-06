from django.db import migrations
from django.contrib.auth.models import User
from pss_project.settings.utils import get_environ_value

def update_password(apps,schema_editor):
    try:
        user = User.objects.get(username=get_environ_value('PSS_CREATOR_USER'))
        user.set_password(get_environ_value('PSS_CREATOR_PASSWORD'))
        user.save()
    except:
        msg = 'Migration error: update user password failed'
        print(msg)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_hypertables'),
    ]

    operations = [
        migrations.RunPython(update_password),
    ]
