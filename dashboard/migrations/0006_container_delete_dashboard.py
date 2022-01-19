# Generated by Django 4.0.1 on 2022-01-19 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_dashboard_ctnname_alter_dashboard_ctnport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctnName', models.CharField(max_length=50, null=True)),
                ('ctnStatus', models.BooleanField()),
                ('ctnPort', models.CharField(max_length=10, null=True)),
                ('ctnIP', models.TextField(max_length=50, null=True)),
                ('ctnToken', models.TextField(null=True)),
                ('ctnId', models.TextField(null=True)),
                ('clientName', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Dashboard',
        ),
    ]