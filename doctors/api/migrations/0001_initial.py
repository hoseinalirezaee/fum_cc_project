# Generated by Django 3.1.7 on 2021-03-26 15:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_from', models.TimeField()),
                ('time_to', models.TimeField()),
                ('count', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.CharField(default='', max_length=128, verbose_name='User ID')),
                ('username', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='Username')),
                ('first_name', models.CharField(max_length=64, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last Name')),
                ('phone', models.CharField(default='', max_length=16, verbose_name='Phone')),
                ('men', models.CharField(default='', max_length=11, verbose_name='Medical Education Number')),
                ('address', models.TextField(default='', max_length=8192, verbose_name='Address')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(default='', max_length=128, verbose_name='User ID')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', related_query_name='reservations', to='api.appointmenttime')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', related_query_name='reservations', to='api.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(default='', max_length=128, verbose_name='User ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(max_length=4096)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comments', to='api.doctor')),
            ],
        ),
        migrations.AddField(
            model_name='appointmenttime',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_times', related_query_name='appointment_times', to='api.doctor'),
        ),
    ]