from flask import Flask, render_template, request, jsonify
import wikipedia
import random

app = Flask(__name__)
messages = []

# ======================
# CONFIG
# ======================
GREETINGS = ['hello', 'hi', 'hey', 'good day', 'howdy']
GREETING_RESPONSES = ['Hello!', 'Hi!', 'Good day!', 'Hey there!', 'Greetings!']


# ======================
# AI LOGIC
# ======================
def get_ai_response(user_msg):
    msg_lower = user_msg.lower().strip()

    # 1. Greetings
    if any(word in msg_lower.split() for word in GREETINGS):
        return random.choice(GREETING_RESPONSES)

    # 2. Wikipedia intent detection
    wiki_triggers = ['what is', 'who is', 'tell me about', 'define', 'explain']

    for trigger in wiki_triggers:
        if msg_lower.startswith(trigger):
            search_term = msg_lower.replace(trigger, '').strip()

            if not search_term:
                return "Please tell me what topic you want to search 😊"

            try:
                wikipedia.set_lang('en')
                summary = wikipedia.summary(search_term, sentences=3)
                return make_friendly_answer(summary)


            except wikipedia.exceptions.DisambiguationError as e:
                return (
                    "This topic has multiple meanings. Try one of these:\n"
                    + ", ".join(e.options[:5])
                )

            except wikipedia.exceptions.PageError:
                return f"I couldn't find anything about '{search_term}'. Try another topic."

            except Exception:
                return "Something went wrong while searching Wikipedia."

    # 3. Smart fallback
    return (
        "I'm still learning 🤖\n"
        "You can ask things like:\n"
        "- what is physics\n"
        "- who is Isaac Newton\n"
        "- explain gravity"
    )
def make_friendly_answer(text):
    openings = [
        "Thanks for your question! ",
        "I appreciate you asking 😊 ",
        "Great question! ",
        "Happy to help! "
    ]

    closings = [
        " Let me know if you want to go deeper.",
        " Hope this helps!",
        " Feel free to ask more questions.",
        " I'm here if you need more help."
    ]

    return random.choice(openings) + text + random.choice(closings)


# ======================
# ROUTES
# ======================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    user_msg = request.json['message']
    messages.append({'user': user_msg})

    ai_msg = get_ai_response(user_msg)
    messages.append({'ai': ai_msg})

    return jsonify({'response': ai_msg})


@app.route('/clear', methods=['POST'])
def clear():
    messages.clear()
    return jsonify({'status': 'cleared'})


# ======================
# RUN
# ======================
if __name__ == '__main__':
    app.run(debug=True, port=5500)
