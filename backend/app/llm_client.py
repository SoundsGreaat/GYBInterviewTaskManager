from google import genai

client = genai.Client()


def generate_short_description(title: str, description: str, text: str):
    try:
        prompt = (
            f"You are a helpful assistant for a task management app. "
            f"Your task is to generate a concise, clear, and engaging short description "
            f"for a task, suitable for displaying in a mobile or web UI. "
            f"Use a friendly and professional tone. "
            f"Limit the description to a maximum of 100 characters. "
            f"Do not include quotes, punctuation at the end, or extra commentary.\n\n"
            f"Task details:\n"
            f"Title: {title}\n"
            f"Description: {description}\n"
            f"Text: {text}\n\n"
            f"Short Description (max 100 characters, single line):"
        )

        ai_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
    except Exception:
        return None

    return ai_response.text
