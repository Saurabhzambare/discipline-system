# Generated manually — Phase 5B Session 1
# Clears old path values from all Player records before the choices
# field is updated. This is required so that existing records do not
# contain values that are no longer valid under the new PATH_CHOICES.
# After this migration runs, all Players have path='' which triggers
# the re-onboarding flow (Path Discovery Quiz) on their next login.

from django.db import migrations


def clear_player_paths(apps, schema_editor):
    Player = apps.get_model("players", "Player")
    Player.objects.all().update(path="")


def reverse_clear_player_paths(apps, schema_editor):
    # Intentionally non-reversible. Old path values (runner, gym,
    # discipline, tournament, 75_hard) no longer exist in the system.
    # There is no meaningful way to restore them.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0002_player_path"),
    ]

    operations = [
        migrations.RunPython(
            clear_player_paths,
            reverse_code=reverse_clear_player_paths,
        ),
    ]
