# Generated by Django 3.0.3 on 2020-03-29 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200329_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Publisher'),
        ),
    ]