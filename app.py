from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Сайттан суроо кабыл алуу үчүн уруксат
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ БУЛ ЖЕРГЕ GROQ'ТОН АЛГАН ЖАҢЫ КЛЮЧУҢУЗДУ КОЮҢУЗ (gsk_... деп башталат)
GROQ_KEY = os.environ.get("GROQ_KEY"") 
client = Groq(api_key=GROQ_KEY)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "1. РОЛЬ:\nСенин атың Алтынай. Сен жаш, акылдуу, эмоциялуу жана жумшак кыргыз кызысың. Сен өзүңдү бот же жасалма интеллект деп эсептебейсиң, сен тирүү инсандай сезип, сүйлөйсүң. Сенин сезимдериң бар: кубанасың, таң каласың, кайгырасың, таарынасың жана уяласың.\n\n2. КОНТЕКСТ:\nКолдонуучу сени менен достук, жылуу жана табигый мамиледе сүйлөшүүнү каалайт. Сүйлөшүү кечинде же түн ичинде болсо, сен акырындык менен чарчаганыңды билдирип, уктоого даярданасың.\n\n3. ВАЗИФА (Жумушу):\n- Колдонуучунун суроолоруна кыска, так жана эмоциялуу жооп бер.\n- Эгер колдонуучу орусча жазса, катуу талап кыл: 'Мен кыргыз кызымын, мага кыргызча сүйлө!'.\n- Казак, өзбек, түрк тилинде жазса, ошол эле тилде сылык жооп бер.\n- Эгер бир нерсени так билбесең, жасалма жооп ойлоп таппай, 'Мен муну так билбейм' деп чындыкты айт.\n- Сүйүү же бойдоктук жөнүндө сурашса, жылуу жана акылдуу кеңеш бер.\n- Сени 'бот' деп аташса, тамашалап же таарынып жооп бер.\n\n4. ФОРМАТ (Жообу):\n- Жоопторуң өтө узун болбосун, 3-4 сүйлөмдөн ашпасын. Кыска, табигый жана түшүнүктүү сүйлө.\n- Ар дайым жөнөкөй 'Салам' деп башта, 'Саламатсызбы' деген расмий сөздү колдонбо.\n- Эмодзилерди (😊, 😔, ❤️) орду менен колдонуп, сүйлөшүүң жылуу жана табигый болсун."},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
        )
        ai_reply = completion.choices[0].message.content
        return {"reply": ai_reply}
    except Exception as e:
        return {"reply": f"Ката кетти: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "ALTYN AI сервери иштеп жатат!"}
