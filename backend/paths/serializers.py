from rest_framework import serializers

from .quiz_data import PATH_CODES


class SubmitAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    question_number = serializers.IntegerField(min_value=1, max_value=9)
    answer = serializers.ChoiceField(choices=["A", "B", "C", "D", "E"])


class CompleteQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()


class SelectPathSerializer(serializers.Serializer):
    path_code = serializers.ChoiceField(choices=PATH_CODES)


class FitnessWarriorOnboardingSerializer(serializers.Serializer):
    training_split = serializers.ChoiceField(
        choices=["ppl", "full_body", "bro_split", "calisthenics", "cardio_focused", "custom"]
    )
    primary_goal = serializers.ChoiceField(
        choices=["muscle_gain", "fat_loss", "recomp", "general_performance"]
    )
    training_days_per_week = serializers.ChoiceField(choices=[3, 4, 5, 6, 7])
    experience_level = serializers.ChoiceField(
        choices=["beginner", "intermediate", "advanced"]
    )
    split_day_start = serializers.ChoiceField(
        choices=["push", "pull", "legs", "rest", "fresh_start"],
        required=False,
        allow_null=True,
    )


class MindsetSageOnboardingSerializer(serializers.Serializer):
    motivation = serializers.ChoiceField(
        choices=["mental_clarity", "stress_relief", "personal_growth", "discipline_building"]
    )
    daily_time_commitment = serializers.ChoiceField(
        choices=["15_minutes", "30_minutes", "1_hour", "as_much_as_needed"]
    )
    experience_level = serializers.ChoiceField(
        choices=["complete_beginner", "some_experience", "daily_practitioner"]
    )
    archetype = serializers.ChoiceField(
        choices=["stoic", "scholar", "monk", "warrior_sage"]
    )


class HealthAlchemistOnboardingSerializer(serializers.Serializer):
    primary_health_goal = serializers.ChoiceField(
        choices=[
            "optimize_energy",
            "reduce_stress_and_burnout",
            "improve_gut_health",
            "build_better_sleep",
            "full_body_transformation",
        ]
    )
    health_relationship = serializers.ChoiceField(
        choices=[
            "starting_from_scratch",
            "some_good_habits",
            "already_health_conscious",
            "biohack_and_optimize",
        ]
    )
    focus_area = serializers.ChoiceField(
        choices=["nutrition", "sleep", "mental_health", "hydration", "all_of_them"]
    )
    equipment_list = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                "cold_shower",
                "cold_plunge",
                "sauna",
                "fitness_tracker",
                "supplements",
                "none_yet",
            ]
        ),
        allow_empty=True,
    )


class DisciplineKnightOnboardingSerializer(serializers.Serializer):
    routine_level = serializers.ChoiceField(
        choices=[
            "no_routine",
            "partial_routine",
            "routine_but_break_often",
            "solid_routine_level_up",
        ]
    )
    biggest_challenge = serializers.ChoiceField(
        choices=["wake_consistently", "staying_focused", "resisting_distractions", "managing_money", "all_of_them"]
    )
    structure_preference = serializers.ChoiceField(
        choices=["fully_structured", "semi_structured", "flexible"]
    )
    time_commitment = serializers.ChoiceField(
        choices=["30_minutes", "1_hour", "2_hours", "as_much_as_it_takes"]
    )


class DisciplineCodeSerializer(serializers.Serializer):
    rules = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=3,
        max_length=5,
    )


class GrindVisionaryOnboardingSerializer(serializers.Serializer):
    grind_focus = serializers.ChoiceField(
        choices=[
            "coding_and_tech",
            "design_and_creative",
            "writing_and_content",
            "business_and_entrepreneurship",
            "marketing_and_growth",
            "finance_and_investing",
            "other",
        ]
    )
    grind_focus_other = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=80,
    )
    experience_state = serializers.ChoiceField(
        choices=[
            "complete_beginner",
            "some_skills_go_deeper",
            "intermediate_ready_to_ship",
            "advanced_scaling",
        ]
    )
    singular_goal_text = serializers.CharField(max_length=255)
    goal_timeline = serializers.ChoiceField(choices=["3_months", "6_months", "1_year", "2_years"])
    daily_hours = serializers.ChoiceField(choices=["30_minutes", "1_hour", "2_hours", "3_plus_hours"])
    current_output_state = serializers.ChoiceField(
        choices=[
            "consume_more_than_create",
            "create_occasionally",
            "ship_regularly",
            "audience_or_income_already",
        ]
    )


class OnboardingCompleteSerializer(serializers.Serializer):
    path_code = serializers.ChoiceField(choices=PATH_CODES)
