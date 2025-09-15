from django.db import migrations

def copy_profiles_data(apps, schema_editor):
    """
    Copie les données du modèle Profile de l'ancienne application vers la nouvelle.
    """
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')
    User = apps.get_model('auth', 'User')

    # Copier chaque profil existant
    for old_profile in OldProfile.objects.all():
        # On récupère l'utilisateur lié au profil
        try:
            user = User.objects.get(pk=old_profile.user_id)
        except User.DoesNotExist:
            continue
        # Création du nouveau profil
        new_profile = NewProfile.objects.create(
            user=user,
            favorite_city=old_profile.favorite_city
        )
        new_profile.save()

class Migration(migrations.Migration):
    """
    Migration personnalisée pour copier les données Profile.
    """
    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data),
    ]