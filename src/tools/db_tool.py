from langchain_core.tools import tool
from src.database.supabase import db


@tool
def query_hospital_db(query: str) -> str:
    """
    Виконує SQL-запит до бази даних лікарні та повертає результат.
    Використовуй цей інструмент, коли користувач запитує про:
    - лікарів (ПІБ, зарплата, спеціалізація)
    - відпустки лікарів
    - відділення та палати
    - спонсорів та пожертвування
    Аргумент:
        query: коректний PostgreSQL-запит
    Повертає:
        Рядок з результатом запиту або повідомлення про помилку.
    """
    try:
        result = db.run(query)
        if not result:
            return "Запит виконано успішно, але результат порожній."
        return result
    except Exception as e:
        return f"Помилка при виконанні запиту: {e}"