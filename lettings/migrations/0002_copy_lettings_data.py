from django.db import migrations

def copy_lettings_data(apps, schema_editor):
    """
    Copie les données des anciens modèles Address et Letting vers les nouveaux modèles.
    """
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')

    # Copier les adresses
    for old_address in OldAddress.objects.all():
        new_address = NewAddress.objects.create(
            number=old_address.number,
            street=old_address.street,
            city=old_address.city,
            state=old_address.state,
            zip_code=old_address.zip_code,
            country_iso_code=old_address.country_iso_code
        )
        new_address.save()

    # Copier les locations
    for old_letting in OldLetting.objects.all():
        # Récupérer la nouvelle adresse correspondante
        try:
            new_address = NewAddress.objects.get(
                number=old_letting.address.number,
                street=old_letting.address.street,
                city=old_letting.address.city,
                state=old_letting.address.state,
                zip_code=old_letting.address.zip_code,
                country_iso_code=old_letting.address.country_iso_code
            )
        except NewAddress.DoesNotExist:
            continue
        new_letting = NewLetting.objects.create(
            title=old_letting.title,
            address=new_address
        )
        new_letting.save()

class Migration(migrations.Migration):
    """
    Migration personnalisée pour copier les données Address et Letting.
    """
    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data),
    ]