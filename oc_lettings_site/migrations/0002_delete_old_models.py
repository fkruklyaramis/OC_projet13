from django.db import migrations

class Migration(migrations.Migration):
    """
    Migration pour supprimer les anciens modèles Address, Letting et Profile.
    """
    dependencies = [
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Letting',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]