# Generated by Django 3.1.1 on 2020-10-08 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hot_image', models.ImageField(blank=True, upload_to='hot_images')),
                ('image_product', models.ImageField(blank=True, upload_to='image_product')),
                ('name_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]
