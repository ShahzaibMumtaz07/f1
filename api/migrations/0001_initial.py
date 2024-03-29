# Generated by Django 3.1.3 on 2023-03-19 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circuits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.TextField()),
                ('name', models.TextField()),
                ('location', models.TextField()),
                ('country', models.TextField()),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('alt', models.IntegerField(blank=True, null=True)),
                ('url', models.TextField()),
            ],
            options={
                'db_table': 'circuits',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Constructors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constructor_ref', models.TextField()),
                ('name', models.TextField()),
                ('nationality', models.TextField()),
                ('country', models.TextField(blank=True, null=True)),
                ('url', models.TextField()),
            ],
            options={
                'db_table': 'constructors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Drivers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_ref', models.TextField()),
                ('number', models.TextField(blank=True, null=True)),
                ('code', models.TextField(blank=True, null=True)),
                ('forename', models.TextField()),
                ('surname', models.TextField()),
                ('dob', models.DateField()),
                ('nationality', models.TextField()),
                ('country', models.TextField(blank=True, null=True)),
                ('url', models.TextField()),
            ],
            options={
                'db_table': 'drivers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Races',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('name', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TextField(blank=True, null=True)),
                ('url', models.TextField()),
                ('circuit', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.circuits')),
            ],
            options={
                'db_table': 'races',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.TextField()),
                ('url', models.TextField()),
            ],
            options={
                'db_table': 'seasons',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField()),
            ],
            options={
                'db_table': 'status',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SprintResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(blank=True, null=True)),
                ('grid', models.IntegerField()),
                ('position', models.IntegerField(blank=True, null=True)),
                ('position_text', models.TextField(blank=True, null=True)),
                ('position_order', models.IntegerField()),
                ('points', models.FloatField()),
                ('laps', models.IntegerField()),
                ('time', models.TextField(blank=True, null=True)),
                ('milliseconds', models.TextField(blank=True, null=True)),
                ('fastest_lap', models.IntegerField(blank=True, null=True)),
                ('fastest_lap_time', models.TextField(blank=True, null=True)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.constructors')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.status')),
            ],
            options={
                'db_table': 'sprint_results',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(blank=True, null=True)),
                ('grid', models.IntegerField()),
                ('position', models.IntegerField(blank=True, null=True)),
                ('position_text', models.TextField(blank=True, null=True)),
                ('position_order', models.IntegerField()),
                ('points', models.FloatField()),
                ('laps', models.IntegerField()),
                ('time', models.TextField(blank=True, null=True)),
                ('milliseconds', models.TextField(blank=True, null=True)),
                ('fastest_lap', models.IntegerField(blank=True, null=True)),
                ('fastest_lap_time', models.TextField(blank=True, null=True)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('fastest_lap_speed', models.TextField(blank=True, null=True)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.constructors')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.status')),
            ],
            options={
                'db_table': 'results',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='races',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.seasons'),
        ),
        migrations.CreateModel(
            name='Qualifying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('position', models.IntegerField()),
                ('q1', models.TextField(blank=True, null=True)),
                ('q2', models.TextField(blank=True, null=True)),
                ('q3', models.TextField(blank=True, null=True)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.constructors')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
            ],
            options={
                'db_table': 'qualifying',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PitStops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop', models.IntegerField()),
                ('lap', models.IntegerField()),
                ('time', models.TextField()),
                ('duration', models.TextField()),
                ('milliseconds', models.BigIntegerField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
            ],
            options={
                'db_table': 'pit_stops',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LapTimes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lap', models.IntegerField()),
                ('position', models.IntegerField()),
                ('time', models.TextField()),
                ('milliseconds', models.BigIntegerField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
            ],
            options={
                'db_table': 'lap_times',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DriverStandings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField()),
                ('position', models.BigIntegerField()),
                ('position_text', models.TextField()),
                ('wins', models.BigIntegerField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
            ],
            options={
                'db_table': 'driver_standings',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ConstructorStandings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField()),
                ('position', models.IntegerField()),
                ('position_text', models.TextField()),
                ('wins', models.IntegerField()),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.constructors')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
            ],
            options={
                'db_table': 'constructor_standings',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ConstructorResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField()),
                ('status', models.TextField(blank=True, null=True)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.constructors')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
            ],
            options={
                'db_table': 'constructor_results',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CombinedResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(blank=True, null=True)),
                ('grid', models.IntegerField()),
                ('position', models.IntegerField(blank=True, null=True)),
                ('position_text', models.TextField(blank=True, null=True)),
                ('position_order', models.IntegerField()),
                ('points', models.FloatField()),
                ('laps', models.IntegerField()),
                ('time', models.TextField(blank=True, null=True)),
                ('milliseconds', models.TextField(blank=True, null=True)),
                ('fastest_lap', models.IntegerField(blank=True, null=True)),
                ('fastest_lap_time', models.TextField(blank=True, null=True)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('fastest_lap_speed', models.TextField(blank=True, null=True)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.constructors')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.drivers')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.races')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.status')),
            ],
            options={
                'db_table': 'combined_results',
                'managed': True,
            },
        ),
    ]
