# Generated by Django 4.1.3 on 2022-11-07 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Gearbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('version', models.CharField(max_length=100)),
                ('horsepower', models.IntegerField()),
                ('doors', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('body_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bodytype')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.brand')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.color')),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.fuel')),
                ('gearbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gearbox')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.url')),
            ],
        ),
    ]