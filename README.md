# 🏥 Hospital Chatbot — Медичний ШІ-асистент

Чат-бот для лікарні на основі **RAG (Retrieval-Augmented Generation)** та агентного підходу. Використовує Google Gemini для генерації відповідей, Pinecone як векторну базу знань і Supabase як структуровану базу даних.

---

## ✨ Можливості

- 💬 **Мультимовний чат** — відповідає мовою користувача (українська, англійська тощо)
- 🔍 **Пошук по документах** (RAG) — знаходить інформацію у PDF та DOCX файлах лікарні: розклад, ціни, правила
- 🗄️ **Запити до структурованої БД** — лікарі, відділення, палати, відпустки, спонсори (Supabase / PostgreSQL)
- 🤖 **Агентний підхід** — LLM сам вирішує який інструмент використати для відповіді
- 🏥 **Система промптів** — бот дотримується медичної етики, не ставить діагнозів, зберігає конфіденційність

---

## 🏗️ Архітектура

```
hospital-chatbot/
├── app.py                      # Streamlit UI — головна точка входу
├── requirements.txt            # Залежності проекту
├── .env                        # Змінні середовища (API ключі)
├── data/
│   ├── General.pdf             # Загальна інформація про лікарню (послуги, ціни, розклад)
│   ├── For wokers.docx         # HR-документ для персоналу (внутрішні правила)
│   └── pinecone_mapping.json   # Мапа UUID → метадані чанків у Pinecone
└── src/
    ├── llm_chain.py            # LLM, агент та системний промпт
    ├── rag.py                  # Інструмент document_search (LangChain tool)
    └── database/
        ├── pinecone_db.py      # Векторна БД: ініціалізація, завантаження документів
        └── supabase.py         # SQL БД: інструмент query_hospital_db (LangChain tool)
```

### Схема роботи

```
Користувач → Streamlit UI → LangChain Agent (Gemini)
                                    ↓
                     ┌─────────────────────────────┐
                     │    Вибір інструменту         │
                     └──────────┬──────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                                   ▼
    document_search                    query_hospital_db
    (Pinecone Vector DB)               (Supabase PostgreSQL)
    ┌──────────────────┐               ┌──────────────────┐
    │ General.pdf      │               │ Лікарі           │
    │ For wokers.docx  │               │ Відділення       │
    └──────────────────┘               │ Палати           │
                                       │ Відпустки        │
                                       │ Спонсори         │
                                       └──────────────────┘
```

---

## 🛠️ Технічний стек

| Компонент          | Технологія                              |
|--------------------|-----------------------------------------|
| UI                 | Streamlit                               |
| LLM                | Google Gemini (gemini-3.5-flash-lite)   |
| Embeddings         | Google Gemini (gemini-embedding-001)    |
| Агентний фреймворк | LangChain Agents                        |
| Векторна БД        | Pinecone (Serverless, AWS us-east-1)    |
| Реляційна БД       | Supabase (PostgreSQL)                   |
| Завантаження PDF   | PyPDFLoader (LangChain Community)       |
| Завантаження DOCX  | docx2txt                                |

---

## ⚙️ Встановлення та запуск

### 1. Клонуйте репозиторій

```bash
git clone <repo-url>
cd hospital-chatbot
```

### 2. Створіть та активуйте віртуальне середовище

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Встановіть залежності

```bash
pip install -r requirements.txt
```

### 4. Налаштуйте змінні середовища

Створіть файл `.env` у корені проекту:

```env
GEMINI_API_KEY=your_google_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
SUPABASE_URL=postgresql://user:password@host:port/dbname
```

| Змінна             | Де отримати                                                |
|--------------------|------------------------------------------------------------|
| `GEMINI_API_KEY`   | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `PINECONE_API_KEY` | [Pinecone Console](https://app.pinecone.io)                |
| `SUPABASE_URL`     | Supabase → Project Settings → Database → Connection string |

### 5. Завантажте документи у Pinecone (перший запуск)

```bash
python -m src.database.pinecone_db
```

Скрипт:
- Завантажить `data/General.pdf` (розбивка по сторінках)
- Завантажить `data/For wokers.docx` (розбивка по нумерованих розділах)
- Створить індекс у Pinecone (якщо не існує)
- Збереже мапу `data/pinecone_mapping.json`

### 6. Запустіть застосунок

```bash
streamlit run app.py
```

Додаток відкриється за адресою: **http://localhost:8501**

---

## 📂 Структура бази знань

### Векторна БД (Pinecone)

Індекс `hospital-chatbot`:
- **Вимірність**: 3072 (Gemini embedding-001)
- **Метрика**: cosine similarity
- **Провайдер**: AWS us-east-1 (Serverless)

Стратегія чанкінгу:
- `General.pdf` → 1 сторінка = 1 чанк
- `For wokers.docx` → 1 нумерований розділ = 1 чанк (мін. 80 символів)

### Реляційна БД (Supabase)

Таблиці, доступні через `query_hospital_db`:
- **Лікарі** — ПІБ, спеціалізація, зарплата
- **Відділення** — назви, інформація
- **Палати** — розподіл по відділеннях
- **Відпустки** — дати відпусток лікарів
- **Спонсори** — пожертвування

---

## 💡 Приклади запитів

```
«Який розклад роботи доктора Ковальчука?»
«Скільки коштує УЗД?»
«Де знаходиться реєстратура?»
«Які лікарі є в кардіологічному відділенні?»
«Які правила відвідування пацієнтів?»
```

---

## 🔒 Безпека та обмеження

- Бот **не ставить медичних діагнозів** і не призначає лікування
- **Не розголошує** медичні дані одного пацієнта іншому
- При відсутності інформації — чесно повідомляє та направляє до реєстратури
- Всі API-ключі зберігаються у `.env` (не комітяться до репозиторію)

---

## 📦 Залежності

```
streamlit
langchain-core
langchain-google-genai
langchain-pinecone
langchain-community
pinecone
docx2txt
pypdf
python-dotenv
psycopg2-binary
```

> **Примітка:** `requirements.txt` містить лише основні залежності. Повний список встановлюється автоматично через pip.
