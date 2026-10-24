import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundry', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amount',
            new_name='amount_paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='reference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
