"""
Fix path discovery models identified during Session 2:

1. PathDiscoveryQuiz: OneToOneField → ForeignKey (multiple quizzes per player
   required for retake support — previous records must never be deleted)
2. PathDiscoveryQuiz: add `completed` BooleanField, `retake_count` IntegerField;
   remove `answers_json` (answers stored in QuizAnswer rows instead)
3. PathMatchScore: `score` FloatField → separate `raw_score` + `match_percentage`
   IntegerFields to match spec
4. QuizAnswer: rename `question_index` → `question_number` (1-based per spec);
   change `answer_value` SmallIntegerField → `answer_key` CharField (A/B/C/D/E)
5. UserPathSelection: add `multi_paths_active` JSONField and
   `multi_path_unlock_day` IntegerField
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("paths", "0001_initial"),
    ]

    operations = [
        # ── PathDiscoveryQuiz ─────────────────────────────────────────────────
        # Remove answers_json (answers now live in QuizAnswer rows)
        migrations.RemoveField(
            model_name="pathdiscoveryquiz",
            name="answers_json",
        ),
        # OneToOneField → ForeignKey to allow multiple quizzes per player
        migrations.AlterField(
            model_name="pathdiscoveryquiz",
            name="player",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="path_discovery_quizzes",
                to="players.player",
            ),
        ),
        # Add completed boolean
        migrations.AddField(
            model_name="pathdiscoveryquiz",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        # Add retake_count
        migrations.AddField(
            model_name="pathdiscoveryquiz",
            name="retake_count",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        # Add ordering
        migrations.AlterModelOptions(
            name="pathdiscoveryquiz",
            options={"ordering": ["-created_at"]},
        ),

        # ── QuizAnswer ────────────────────────────────────────────────────────
        # Rename question_index → question_number (1-based, matches spec)
        migrations.RenameField(
            model_name="quizanswer",
            old_name="question_index",
            new_name="question_number",
        ),
        # Replace answer_value SmallIntegerField with answer_key CharField(1)
        migrations.RemoveField(
            model_name="quizanswer",
            name="answer_value",
        ),
        migrations.AddField(
            model_name="quizanswer",
            name="answer_key",
            field=models.CharField(default="A", max_length=1),
            preserve_default=False,
        ),

        # ── PathMatchScore ────────────────────────────────────────────────────
        # Remove old FloatField `score`, add split raw_score + match_percentage
        migrations.RemoveField(
            model_name="pathmatchscore",
            name="score",
        ),
        migrations.AddField(
            model_name="pathmatchscore",
            name="raw_score",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="pathmatchscore",
            name="match_percentage",
            field=models.PositiveSmallIntegerField(default=0),
        ),

        # ── UserPathSelection ─────────────────────────────────────────────────
        migrations.AddField(
            model_name="userpathselection",
            name="multi_paths_active",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="userpathselection",
            name="multi_path_unlock_day",
            field=models.PositiveSmallIntegerField(default=30),
        ),
    ]
