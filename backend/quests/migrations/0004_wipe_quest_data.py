from django.db import migrations


def wipe_all_quests(apps, schema_editor):
    """
    Delete all Quest records. CASCADE handles PlayerDailyQuestAssignment
    and QuestCompletion automatically. Player EXP/level/streak are
    unaffected (stored on Player model).
    """
    Quest = apps.get_model("quests", "Quest")
    Quest.objects.all().delete()


def reverse_wipe_all_quests(apps, schema_editor):
    # Quest data cannot be restored — seed data will be re-loaded via fixtures
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0003_playerdailyquestassignment_quests_play_player__5ea607_idx"),
        ("players", "0004_update_player_model"),
    ]

    operations = [
        migrations.RunPython(wipe_all_quests, reverse_code=reverse_wipe_all_quests),
    ]
