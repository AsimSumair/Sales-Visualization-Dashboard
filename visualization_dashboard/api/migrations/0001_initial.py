from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_year', models.IntegerField(blank=True, null=True)),
                ('intensity', models.IntegerField(blank=True, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('topic', models.CharField(blank=True, max_length=255, null=True)),
                ('insight', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('start_year', models.IntegerField(blank=True, null=True)),
                ('impact', models.CharField(blank=True, max_length=255, null=True)),
                ('added', models.CharField(blank=True, max_length=255, null=True)),
                ('published', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('relevance', models.IntegerField(blank=True, null=True)),
                ('pestle', models.CharField(blank=True, max_length=255, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('likelihood', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
