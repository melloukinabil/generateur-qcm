from groq import Groq
from config import GROQ_API_KEY
import json
import re


def _build_prompt(text: str, num_questions: int, difficulty: str) -> str:
    """Construit le prompt pour la génération de QCM."""
    return f"""À partir du texte suivant, génère exactement {num_questions} questions à choix multiples (QCM)
de niveau {difficulty}.

Pour chaque question :
- Propose 4 options (A, B, C, D)
- Indique la bonne réponse
- Ajoute une brève explication

Format souhaité pour chaque question :
**Question X :** [question]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
✅ Réponse correcte : [lettre]
💡 Explication : [explication courte]

---

Texte source :
{text}
"""


def _build_structured_prompt(text: str, num_questions: int, difficulty: str) -> str:
    """Construit le prompt pour obtenir un JSON structuré."""
    return f"""À partir du texte suivant, génère exactement {num_questions} questions à choix multiples (QCM) de niveau {difficulty}.

IMPORTANT : Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après. Le format doit être exactement :
[
  {{
    "question": "La question ici",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "correct": "A",
    "explanation": "Explication courte"
  }}
]

Texte source :
{text}
"""


def _generate_with_groq(prompt: str) -> str:
    """Génération via Groq (gratuit avec limites)."""
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Tu es un expert en création de QCM pédagogiques. Tu génères des questions claires, précises et pertinentes basées sur le contenu fourni.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
    )
    return response.choices[0].message.content


def generate_qcm(text: str, num_questions: int = 5, difficulty: str = "moyen") -> str:
    """Génère des QCM en texte brut."""
    prompt = _build_prompt(text, num_questions, difficulty)
    return _generate_with_groq(prompt)


def generate_qcm_structured(text: str, num_questions: int = 5, difficulty: str = "moyen") -> list:
    """Génère des QCM sous forme de liste de dictionnaires."""
    prompt = _build_structured_prompt(text, num_questions, difficulty)
    response = _generate_with_groq(prompt)

    # Essayer d'extraire le JSON de la réponse
    try:
        # Chercher un tableau JSON dans la réponse
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            questions = json.loads(json_match.group())
        else:
            questions = json.loads(response)
        return questions
    except json.JSONDecodeError:
        # Fallback : réessayer avec un prompt plus strict
        raise ValueError("L'IA n'a pas retourné un format valide. Veuillez réessayer.")
