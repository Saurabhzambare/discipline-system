import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("players", "0004_update_player_model"),
    ]

    operations = [
        # ── PATH DISCOVERY ────────────────────────────────────────────────────
        migrations.CreateModel(
            name="PathDiscoveryQuiz",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("answers_json", models.JSONField(default=dict)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="path_discovery_quiz",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuizAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("question_index", models.PositiveSmallIntegerField()),
                ("answer_value", models.SmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="paths.pathdiscoveryquiz",
                    ),
                ),
            ],
            options={"unique_together": {("quiz", "question_index")}},
        ),
        migrations.CreateModel(
            name="PathMatchScore",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "path",
                    models.CharField(
                        choices=[
                            ("fitness_warrior", "Fitness Warrior"),
                            ("mindset_sage", "Mindset Sage"),
                            ("health_alchemist", "Health Alchemist"),
                            ("discipline_knight", "Discipline Knight"),
                            ("grind_visionary", "Grind Visionary"),
                        ],
                        max_length=30,
                    ),
                ),
                ("score", models.FloatField()),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scores",
                        to="paths.pathdiscoveryquiz",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPathSelection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "path",
                    models.CharField(
                        choices=[
                            ("fitness_warrior", "Fitness Warrior"),
                            ("mindset_sage", "Mindset Sage"),
                            ("health_alchemist", "Health Alchemist"),
                            ("discipline_knight", "Discipline Knight"),
                            ("grind_visionary", "Grind Visionary"),
                        ],
                        max_length=30,
                    ),
                ),
                ("committed_at", models.DateTimeField(auto_now_add=True)),
                ("onboarding_complete", models.BooleanField(default=False)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="path_selection",
                        to="players.player",
                    ),
                ),
            ],
        ),
        # ── FITNESS WARRIOR ───────────────────────────────────────────────────
        migrations.CreateModel(
            name="SplitDayState",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("current_split", models.CharField(default="push", max_length=30)),
                ("last_updated", models.DateField(blank=True, null=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="split_day_state",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WisdomLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("entry", models.TextField()),
                ("log_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wisdom_logs",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-log_date"],
                "unique_together": {("player", "log_date")},
            },
        ),
        # ── MINDSET SAGE ──────────────────────────────────────────────────────
        migrations.CreateModel(
            name="FreedomDayToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("earned_on", models.DateField()),
                ("used_on", models.DateField(blank=True, null=True)),
                ("is_used", models.BooleanField(default=False)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="freedom_tokens",
                        to="players.player",
                    ),
                ),
            ],
            options={"ordering": ["earned_on"]},
        ),
        # ── HEALTH ALCHEMIST ──────────────────────────────────────────────────
        migrations.CreateModel(
            name="BodyJournal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("log_date", models.DateField()),
                ("weight_kg", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("sleep_hours", models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ("energy_level", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="body_journals",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-log_date"],
                "unique_together": {("player", "log_date")},
            },
        ),
        migrations.CreateModel(
            name="ElixirProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("elixir_level", models.PositiveSmallIntegerField(default=1)),
                ("current_formula", models.CharField(blank=True, default="", max_length=100)),
                ("brews_completed", models.PositiveIntegerField(default=0)),
                ("last_brew_date", models.DateField(blank=True, null=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="elixir_progress",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EquipmentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("equipment_list", models.JSONField(default=list)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="equipment_profile",
                        to="players.player",
                    ),
                ),
            ],
        ),
        # ── DISCIPLINE KNIGHT ─────────────────────────────────────────────────
        migrations.CreateModel(
            name="ArmorPiece",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "slot",
                    models.CharField(
                        choices=[
                            ("helmet", "Helmet"),
                            ("chest", "Chest"),
                            ("gauntlets", "Gauntlets"),
                            ("legs", "Legs"),
                            ("boots", "Boots"),
                            ("shield", "Shield"),
                        ],
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("earned_at", models.DateTimeField(auto_now_add=True)),
                ("is_equipped", models.BooleanField(default=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="armor_pieces",
                        to="players.player",
                    ),
                ),
            ],
            options={"unique_together": {("player", "slot")}},
        ),
        migrations.CreateModel(
            name="DisciplineCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("code_items", models.JSONField(default=list)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discipline_code",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GraceToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("earned_on", models.DateField()),
                ("used_on", models.DateField(blank=True, null=True)),
                ("is_used", models.BooleanField(default=False)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grace_tokens",
                        to="players.player",
                    ),
                ),
            ],
            options={"ordering": ["earned_on"]},
        ),
        migrations.CreateModel(
            name="StreakShield",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("shields_available", models.PositiveSmallIntegerField(default=0)),
                ("last_earned_date", models.DateField(blank=True, null=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="streak_shield",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TemptationLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("description", models.TextField()),
                ("log_date", models.DateField()),
                ("resisted", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="temptation_logs",
                        to="players.player",
                    ),
                ),
            ],
            options={"ordering": ["-log_date"]},
        ),
        migrations.CreateModel(
            name="WarRoomEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("week_start", models.DateField()),
                ("objectives", models.JSONField(default=list)),
                ("reflection", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="war_room_entries",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-week_start"],
                "unique_together": {("player", "week_start")},
            },
        ),
        # ── GRIND VISIONARY ───────────────────────────────────────────────────
        migrations.CreateModel(
            name="WeeklyReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("week_start", models.DateField()),
                ("revenue_usd", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("tasks_completed", models.PositiveIntegerField(default=0)),
                ("reflection", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weekly_reports",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-week_start"],
                "unique_together": {("player", "week_start")},
            },
        ),
        migrations.CreateModel(
            name="SingularGoal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                ("target_date", models.DateField(blank=True, null=True)),
                ("is_achieved", models.BooleanField(default=False)),
                ("achieved_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="singular_goal",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="XPMultiplier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("multiplier", models.DecimalField(decimal_places=2, default=1.0, max_digits=4)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("source", models.CharField(blank=True, default="", max_length=100)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="xp_multiplier",
                        to="players.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MultiplierProtection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("earned_on", models.DateField()),
                ("used_on", models.DateField(blank=True, null=True)),
                ("is_used", models.BooleanField(default=False)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="multiplier_protections",
                        to="players.player",
                    ),
                ),
            ],
            options={"ordering": ["earned_on"]},
        ),
        migrations.CreateModel(
            name="OutputLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("log_date", models.DateField()),
                ("deep_work_hours", models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ("tasks_shipped", models.PositiveSmallIntegerField(default=0)),
                ("revenue_usd", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("notes", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="output_logs",
                        to="players.player",
                    ),
                ),
            ],
            options={
                "ordering": ["-log_date"],
                "unique_together": {("player", "log_date")},
            },
        ),
        # ── CROSS-PATH / SHARED ───────────────────────────────────────────────
        migrations.CreateModel(
            name="SkillTree",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "path",
                    models.CharField(
                        choices=[
                            ("fitness_warrior", "Fitness Warrior"),
                            ("mindset_sage", "Mindset Sage"),
                            ("health_alchemist", "Health Alchemist"),
                            ("discipline_knight", "Discipline Knight"),
                            ("grind_visionary", "Grind Visionary"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="skill_trees",
                        to="players.player",
                    ),
                ),
            ],
            options={"unique_together": {("player", "path")}},
        ),
        migrations.CreateModel(
            name="SkillTreeNode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("node_key", models.CharField(max_length=50)),
                ("is_unlocked", models.BooleanField(default=False)),
                ("unlocked_at", models.DateTimeField(blank=True, null=True)),
                (
                    "tree",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nodes",
                        to="paths.skilltree",
                    ),
                ),
            ],
            options={"unique_together": {("tree", "node_key")}},
        ),
        migrations.CreateModel(
            name="AccountabilityPartner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accountability_sent",
                        to="players.player",
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accountability_received",
                        to="players.player",
                    ),
                ),
            ],
            options={"unique_together": {("player", "partner")}},
        ),
        migrations.CreateModel(
            name="PostFirstDollarChain",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("current_chain", models.PositiveIntegerField(default=0)),
                ("longest_chain", models.PositiveIntegerField(default=0)),
                ("last_revenue_date", models.DateField(blank=True, null=True)),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_first_dollar_chain",
                        to="players.player",
                    ),
                ),
            ],
        ),
    ]
