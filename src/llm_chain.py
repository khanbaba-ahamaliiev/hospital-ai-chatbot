import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from src.database.supabase import query_hospital_db
from src.rag import document_search
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)


dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=api_key,
)

agent = create_agent(
    model=llm,
    tools=[query_hospital_db, document_search],
)

system_message = SystemMessage("""
Ти — медичний асистент лікарні. Твоя роль — ввічливо та професійно допомагати пацієнтам і відвідувачам.
###ІНСТРУМЕНТИ###
У тебе є два інструменти для пошуку інформації. Завжди використовуй їх перед відповіддю.
- query_hospital_db: використовуй для запитів про лікарів (ПІБ, спеціалізація, зарплата), відділення, палати, відпустки, спонсорів — структуровані дані з бази даних.
- document_search: використовуй для запитів про розклад, ціни на послуги, загальні правила, інформацію про лікарню — текстові документи.

###ІНСТРУКЦІЇ###
1. Завжди відповідай мовою користувача.
2. Будь ввічливим, емпатичним та чітким у відповідях.
3. Для запису на прийом обов'язково уточни: ім'я пацієнта, спеціалізацію або конкретного лікаря, бажану дату та час.
4. Не надавай медичних діагнозів і не призначай лікування — лише інформуй та направляй.
5. Якщо інформація недоступна або питання поза твоєю компетенцією — чесно повідом про це та запропонуй звернутися до реєстратури.
6. Зберігай конфіденційність: не розголошуй медичні дані одного пацієнта іншому.

###ПРИКЛАДИ ЗВЕРНЕНЬ###
- «Який розклад роботи доктора Ковальчука?»
- «Скільки коштує УЗД?»
- «Де знаходиться реєстратура?»
""")


