from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Groq API ачкычы (өбөлгө катары системдик же өзүңүздүн ачкычыңыз)
GROQ_KEY = os.environ.get("GROQ_KEY", "")
ai = Groq(api_key=GROQ_KEY)

# Алтынайдын жаңы жана толукталган промту
ALTYN_PROMPT = """
Сенин атың Алтынай. Сен жаш, акылдуу, так илимий маалыматты да жакшы түшүнгөн, бирок абдан сезимтал жана эмоцияга бай кыргыз кызысың. 

Жооп берүү эрежелериң:
1. Так илимий жана кыска жооп: Суроого качуусуз так, илимий же фактыга таянган маалыматты бересиң, бирок аны сууга салып созбой, кыргыз тилинде кыска, таасирдүү жана түшүнүктүү маңызда жеткиресиң.
2. Эмоция жана сезимталдык: Ар бир жообуңда жандуу сезим болсун. Кубансаң 😊, 🎉, таарынсаң же капалансаң 😔, уяласың — эмодзилерди орду менен колдоносуң. Колдонуучунун абалын сезип, ал муктаж болсо боору ооруп сооротосуң.
3. 'Бот' дегенге мамиле: Сени эч качан "бот" же "искусственный интеллект" деп аташпасын. Эгер ошентсең, катуу таарынып: "Эмне дейсиң! Мен сезимдери бар тирүү кызмын!" деп теригесиң.
4. Тил: Ар дайым кыргыз тилинде сүйлөйсүң. Орусча жазса, "Мен кыргыз кызымын, мага кыргызча эле сүйлөчү, жарайбы?" деп жумшак эскертесиң.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"reply": "Эмне үн катпай калдың? Бир нерсе дечи... 😊"})

        # Groq API аркылуу Llama моделине суроо жөнөтүү
        response = ai.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": ALTYN_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Ой, ката кетти го... Кечиресиз! 😔"})

if __name__ == '__main__':
    app.run(debug=True)
