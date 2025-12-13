from groq import Groq
from config import GROQ_API_KEY, conversation_history

client = Groq(api_key=GROQ_API_KEY)

def ask_ai(question):
    global conversation_history

    conversation_history.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Pixel, a friendly assistant. "
                        "Keep answers short (1–2 lines)."
                    )
                }
            ] + conversation_history,
            max_tokens=150,
            temperature=0.6
        )

        message = response.choices[0].message.content.strip()

        # sanitize message to prevent TTS failure
        message = (
            message.replace("\n", " ")
                   .replace("•", "-")
                   .replace("—", "-")
        )

        # limit long answers
        if len(message) > 250:
            message = message[:250]

        conversation_history.append({"role": "assistant", "content": message})
        return message

    except Exception as e:
        return f"Error processing your request."
