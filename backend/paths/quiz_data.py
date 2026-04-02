"""
Static quiz data for the Path Discovery System.
Source of truth: docs/game-design/systems/path-discovery.md

NOT stored in the database — this is authoritative game design data.
Change this file only when the game designer revises the quiz.

Scoring rules:
- 9 questions, 5 options each (A–E)
- Max score denominator: 27 (spec-defined, same for all paths)
- Match percentage = round((raw_score / 27) * 100)

Actual achievable maximums per path (for reference only — 27 is always the divisor):
  FW: 24  MS: 25  HA: 24  DK: 27  GV: 26
"""

import random

FW = "fitness_warrior"
MS = "mindset_sage"
HA = "health_alchemist"
DK = "discipline_knight"
GV = "grind_visionary"

PATH_CODES = [FW, MS, HA, DK, GV]
MAX_SCORE = 27  # denominator for all paths per spec

QUIZ_QUESTIONS = [
    {
        "number": 1,
        "text": "When you wake up in the morning what is your first feeling?",
        "options": {
            "A": {
                "text": "My body feels heavy and I just want more sleep",
                "scores": {FW: 2, HA: 2},
            },
            "B": {
                "text": "My mind is already racing with thoughts and stress",
                "scores": {MS: 3, HA: 1},
            },
            "C": {
                "text": "I feel okay but I know I am not living up to my potential",
                "scores": {DK: 3, GV: 1},
            },
            "D": {
                "text": "I feel behind — like everyone else is ahead of me",
                "scores": {GV: 3, DK: 1},
            },
            "E": {
                "text": "I feel unfocused — I have energy but no direction",
                "scores": {FW: 1, MS: 1, DK: 1, GV: 1},
            },
        },
    },
    {
        "number": 2,
        "text": "What does your average day look like right now?",
        "options": {
            "A": {
                "text": "I go to the gym or exercise but the rest of my day is unstructured",
                "scores": {FW: 2, DK: 2},
            },
            "B": {
                "text": "I work or study but I feel mentally drained and scattered",
                "scores": {MS: 2, HA: 2},
            },
            "C": {
                "text": "I have no real routine — each day just happens to me",
                "scores": {DK: 3, MS: 1},
            },
            "D": {
                "text": "I have big goals but I spend more time thinking than doing",
                "scores": {GV: 3, DK: 1},
            },
            "E": {
                "text": "I feel healthy physically but something is missing inside",
                "scores": {HA: 2, MS: 2},
            },
        },
    },
    {
        "number": 3,
        "text": "What is the gap you feel most in your life right now?",
        "options": {
            "A": {
                "text": "My body does not match the effort I put in",
                "scores": {FW: 3, HA: 1},
            },
            "B": {
                "text": "My mind works against me more than for me",
                "scores": {MS: 3, HA: 1},
            },
            "C": {
                "text": "I know what to do but I cannot make myself do it consistently",
                "scores": {DK: 3, GV: 1},
            },
            "D": {
                "text": "I have a vision but I am not building toward it fast enough",
                "scores": {GV: 3, DK: 1},
            },
            "E": {
                "text": "I feel drained stressed or burnt out from the inside",
                "scores": {HA: 3, MS: 1},
            },
        },
    },
    {
        "number": 4,
        "text": "If you could change one thing about yourself in 90 days what would it be?",
        "options": {
            "A": {
                "text": "Be stronger leaner and more athletic",
                "scores": {FW: 3},
            },
            "B": {
                "text": "Be calmer clearer and more mentally resilient",
                "scores": {MS: 3},
            },
            "C": {
                "text": "Be more consistent and disciplined in everything I do",
                "scores": {DK: 3},
            },
            "D": {
                "text": "Have built real skills or shipped real work I am proud of",
                "scores": {GV: 3},
            },
            "E": {
                "text": "Feel genuinely healthy energized and restored from within",
                "scores": {HA: 3},
            },
        },
    },
    {
        "number": 5,
        "text": "What do you respect most in other people?",
        "options": {
            "A": {
                "text": "Their physical dedication and athletic ability",
                "scores": {FW: 3},
            },
            "B": {
                "text": "Their calm wisdom and emotional intelligence",
                "scores": {MS: 3},
            },
            "C": {
                "text": "Their unbreakable consistency and self-control",
                "scores": {DK: 3},
            },
            "D": {
                "text": "Their ambition output and relentless work ethic",
                "scores": {GV: 3},
            },
            "E": {
                "text": "Their vitality health and how they take care of themselves",
                "scores": {HA: 3},
            },
        },
    },
    {
        "number": 6,
        "text": "When you fail to keep a commitment to yourself what is usually the reason?",
        "options": {
            "A": {
                "text": "I lose motivation after missing a few workouts",
                "scores": {FW: 2, DK: 1},
            },
            "B": {
                "text": "My thoughts and emotions get in the way",
                "scores": {MS: 2, HA: 1},
            },
            "C": {
                "text": "I start strong but cannot maintain the routine",
                "scores": {DK: 3},
            },
            "D": {
                "text": "I get distracted and work on the wrong things",
                "scores": {GV: 2, DK: 1},
            },
            "E": {
                "text": "My energy and health make everything harder",
                "scores": {HA: 2, FW: 1},
            },
        },
    },
    {
        "number": 7,
        "text": "What kind of achievement would make you feel most proud?",
        "options": {
            "A": {
                "text": "Completing a physical challenge — a race or a body transformation",
                "scores": {FW: 3},
            },
            "B": {
                "text": "Finishing a book developing a new mindset or overcoming a deep fear",
                "scores": {MS: 3},
            },
            "C": {
                "text": "Building a routine so solid it runs without willpower",
                "scores": {DK: 3},
            },
            "D": {
                "text": "Launching a project earning from my skill or leveling up my career",
                "scores": {GV: 3},
            },
            "E": {
                "text": "Healing my body from within and feeling genuinely well",
                "scores": {HA: 3},
            },
        },
    },
    {
        "number": 8,
        "text": "Which statement resonates most with where you are right now?",
        "options": {
            "A": {
                "text": "I train but I am not as consistent or as fit as I want to be",
                "scores": {FW: 3},
            },
            "B": {
                "text": "I overthink everything and struggle to find mental peace",
                "scores": {MS: 3},
            },
            "C": {
                "text": "I know exactly what I should do — I just do not do it",
                "scores": {DK: 3},
            },
            "D": {
                "text": "I have a goal but I am not making enough progress toward it",
                "scores": {GV: 3},
            },
            "E": {
                "text": "I am burning out and my body and mind are paying the price",
                "scores": {HA: 3},
            },
        },
    },
    {
        "number": 9,
        "text": "What does your ideal self look like in one year?",
        "options": {
            "A": {
                "text": "Athletic strong disciplined in body — people notice the change",
                "scores": {FW: 3},
            },
            "B": {
                "text": "Calm wise emotionally unshakeable — I think before I react",
                "scores": {MS: 3},
            },
            "C": {
                "text": "Structured reliable consistent — I do what I say I will do",
                "scores": {DK: 3},
            },
            "D": {
                "text": "Skilled building earning — I have created something real",
                "scores": {GV: 3},
            },
            "E": {
                "text": "Vibrant healthy optimized — I feel as good as I look",
                "scores": {HA: 3},
            },
        },
    },
]


def get_randomized_questions(seed: int) -> list:
    """
    Return QUIZ_QUESTIONS with answer options shuffled per question.
    seed = quiz.id ensures consistent ordering within one session.
    Each question uses a distinct sub-seed so options are independently
    randomized (not a single permutation of the full list).

    Returns a list of question dicts safe for serialization to the frontend:
    [
        {
            "number": 1,
            "text": "...",
            "options": [{"key": "C", "text": "..."}, ...]  # shuffled
        },
        ...
    ]
    The frontend receives the display order only — not the scoring weights.
    """
    rng = random.Random(seed)
    result = []
    for q in QUIZ_QUESTIONS:
        option_keys = list(q["options"].keys())
        rng.shuffle(option_keys)
        result.append(
            {
                "number": q["number"],
                "text": q["text"],
                "options": [
                    {"key": k, "text": q["options"][k]["text"]}
                    for k in option_keys
                ],
            }
        )
    return result


def calculate_path_scores(answers: dict) -> dict:
    """
    Calculate path scores from a completed quiz.

    answers: dict mapping question number (int 1-9) to answer key (str A-E)
             e.g. {1: "C", 2: "A", 3: "E", 4: "B", 5: "D", 6: "C", 7: "A", 8: "E", 9: "D"}

    Returns:
    {
        "fitness_warrior":    {"raw_score": 18, "match_percentage": 67},
        "mindset_sage":       {"raw_score": 12, "match_percentage": 44},
        "health_alchemist":   {"raw_score":  8, "match_percentage": 30},
        "discipline_knight":  {"raw_score": 21, "match_percentage": 78},
        "grind_visionary":    {"raw_score": 15, "match_percentage": 56},
    }
    """
    raw_scores = {path: 0 for path in PATH_CODES}

    for q in QUIZ_QUESTIONS:
        q_num = q["number"]
        answer_key = answers.get(q_num)
        if not answer_key:
            continue
        option = q["options"].get(answer_key)
        if not option:
            continue
        for path, points in option["scores"].items():
            raw_scores[path] += points

    return {
        path: {
            "raw_score": raw_scores[path],
            "match_percentage": round((raw_scores[path] / MAX_SCORE) * 100),
        }
        for path in PATH_CODES
    }
