# Generated by Django 2.1.9 on 2019-07-16 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eetlijst', '0013_dinner_cost_time'),
    ]

    def test_user_entries(apps, schema_editor):
        UserDinner = apps.get_model('eetlijst', 'UserDinner')
        Dinner = apps.get_model('eetlijst', 'Dinner')
        for user_dinner in UserDinner.objects.all():
            try:
                dinner = Dinner.objects.get(date=user_dinner.dinner_date)
                user_dinner.dinner = dinner
                user_dinner.save()
            except Exception as e:
                raise LookupError("Couldnt get a date for this userdinner entry.", str(e))

    operations = [
        migrations.AlterField(
            model_name='dinner',
            name='eta_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userdinner',
            name='dinner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eetlijst.Dinner', null=True),
        ),
    ]
