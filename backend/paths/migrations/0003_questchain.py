from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0006_add_quest_support_models"),
        ("paths", "0002_fix_quiz_models"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestChain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sequence_order", models.PositiveSmallIntegerField(default=1)),
                (
                    "child_quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chain_parents",
                        to="quests.quest",
                    ),
                ),
                (
                    "parent_quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chain_children",
                        to="quests.quest",
                    ),
                ),
            ],
            options={
                "ordering": ["sequence_order", "id"],
                "unique_together": {("parent_quest", "child_quest")},
            },
        ),
        migrations.AddConstraint(
            model_name="questchain",
            constraint=models.CheckConstraint(
                condition=~models.Q(("parent_quest", models.F("child_quest"))),
                name="paths_questchain_no_self_reference",
            ),
        ),
    ]
