from langchain_core.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from src.database.supabase import db
from src.config import settings


_toolkit_llm = ChatGoogleGenerativeAI(
    model=settings.model.name,
    temperature=0,
    api_key=settings.gemini_api_key,
)

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=_toolkit_llm,
)

sql_tools = toolkit.get_tools()
sql_context = toolkit.get_context()


@tool
def query_hospital_db(query: str) -> str:
    """
    Виконує SQL-запит до бази даних лікарні та повертає результат.

    Використовуй цей інструмент після hospital_db_context, коли користувач запитує про:
    - лікарів (ПІБ, зарплата, спеціалізація)
    - відпустки лікарів
    - відділення та палати
    - спонсорів та пожертвування

    :param query: коректний PostgreSQL-запит.
    :return: рядок з результатом запиту; якщо результат порожній,
             повертається відповідне повідомлення; у разі помилки - текст помилки.
    """
    try:
        result = db.run(query)
        if not result:
            return "Запит виконано успішно, але результат порожній."
        return result
    except Exception as e:
        return f"Помилка при виконанні запиту: {e}"


@tool
def hospital_db_context(_: str = "") -> str:
    """
    Повертає контекст SQL-схеми лікарні з SQLDatabaseToolkit.

    Використовуй цей інструмент:
    - при першому зверненні до БД у поточному діалозі;
    - перед побудовою складних SQL-запитів;
    - коли структура БД невідома або потрібно перевірити таблиці та поля.

    :param: службовий параметр (не використовується), залишений для сумісності з інтерфейсом tool.
    :return: рядок із контекстом БД (SQL dialect, Available tables, Table info)
             або повідомлення про помилку, якщо контекст отримати не вдалося.
    """
    try:
        dialect = sql_context.get("dialect", "postgresql")
        table_names = sql_context.get("table_names", "")
        table_info = sql_context.get("table_info", "")
        return (
            f"SQL dialect: {dialect}\n"
            f"Available tables: {table_names}\n"
            f"Table info:\n{table_info}"
        )
    except Exception as e:
        return f"Помилка при отриманні контексту БД: {e}"

