# Generated by Django 5.1.3 on 2024-11-22 09:59

import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalIncome',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, help_text='Amount of income in the currency unit', max_digits=10)),
                ('date', models.DateField(blank=True, editable=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical income',
                'verbose_name_plural': 'historical Incomes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, help_text='Amount of income in the currency unit', max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Incomes',
                'ordering': ['-date'],
            },
        ),
    ]
