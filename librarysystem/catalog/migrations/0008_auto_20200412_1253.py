# Generated by Django 3.0.3 on 2020-04-12 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20200404_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(help_text='Enter a brief review of the book', max_length=1000, verbose_name='Review')),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='review',
            field=models.ForeignKey(help_text='Enter a brief review of the book', max_length=1000, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Review'),
        ),
    ]