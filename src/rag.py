from src.database.pinecone_db import vector_store
from langchain_core.tools import tool


@tool
def document_search(query: str) -> str:
    """
    Шукає інформацію у базі знань лікарні.

    База даних містить: розклад роботи лікарів, перелік послуг та ціни,
    інформацію про відділення, правила для працівників та загальну інформацію про лікарню.

    Використовуй цей інструмент, коли потрібно знайти конкретну інформацію
    про лікарню, лікарів, послуги або внутрішні правила.

    :param query: запит для пошуку (наприклад: "розклад кардіолога", "ціна УЗД")
    :return: текст з релевантними уривками з документів лікарні
    """
    docs = vector_store.similarity_search(query, k=3)
    if not docs:
        return "Інформацію за вашим запитом не знайдено в базі знань."

    results = []
    for doc in docs:
        results.append(doc.page_content)

    return "\n\n".join(results)