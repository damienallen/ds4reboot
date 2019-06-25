# Generated by Django 2.1.9 on 2019-06-11 22:33

from django.db import migrations, models

from thesau.models import Report


class Migration(migrations.Migration):
    dependencies = [
        ('thesau', '0012_auto_20170228_1709'),
    ]

    def convert_to_media(apps, schema_editor):
        MyModel = apps.get_model('thesau', 'Report')
        for report in MyModel.objects.all():
            report.report_file.name = report.report_path.replace('static/', '')
            report.save()

    def convert_to_static(apps, schema_editor):
        MyModel = apps.get_model('thesau', 'Report')
        for report in MyModel.objects.all():
            report.report_file.name = report.report_path.replace('/hr_reports', 'static/hr_reports')
            report.save()


    operations = [
        migrations.AddField(
            model_name='report',
            name='report_file',
            field=models.FileField(default='media', upload_to='hr_reports/'),
            preserve_default=False,
        ),
        migrations.RunPython(convert_to_media,reverse_code=convert_to_static),
        migrations.RemoveField(
            model_name='report',
            name='report_path',
        ),
    ]