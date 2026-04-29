import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id_notification', models.AutoField(primary_key=True, serialize=False)),
                ('messsage', models.CharField(blank=True, default='', max_length=255)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('lu', models.BooleanField(default=False)),
            ],
        ),
    ]
