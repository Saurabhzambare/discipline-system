from django.db import migrations, models


def migrate_legacy_armor_slots(apps, schema_editor):
    ArmorPiece = apps.get_model('paths', 'ArmorPiece')
    ArmorPiece.objects.filter(slot='chest').update(slot='chest_plate')
    ArmorPiece.objects.filter(slot='legs').update(slot='shoulder_guards')


def reverse_migrate_legacy_armor_slots(apps, schema_editor):
    ArmorPiece = apps.get_model('paths', 'ArmorPiece')
    ArmorPiece.objects.filter(slot='chest_plate').update(slot='chest')
    ArmorPiece.objects.filter(slot='shoulder_guards').update(slot='legs')


class Migration(migrations.Migration):

    dependencies = [
        ('paths', '0006_delete_accountabilitypartner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armorpiece',
            name='slot',
            field=models.CharField(
                choices=[
                    ('helmet', 'Helmet'),
                    ('chest_plate', 'Chest Plate'),
                    ('gauntlets', 'Gauntlets'),
                    ('shoulder_guards', 'Shoulder Guards'),
                    ('boots', 'Boots'),
                    ('shield', 'Shield'),
                    ('sword', 'Sword'),
                    ('chest', 'Chest (Legacy)'),
                    ('legs', 'Legs (Legacy)'),
                ],
                max_length=20,
            ),
        ),
        migrations.RunPython(migrate_legacy_armor_slots, reverse_migrate_legacy_armor_slots),
    ]
