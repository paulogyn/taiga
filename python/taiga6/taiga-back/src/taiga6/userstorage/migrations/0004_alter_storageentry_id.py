# Generated by Django 3.2.12 on 2022-02-10 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstorage', '0003_json_to_jsonb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageentry',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]