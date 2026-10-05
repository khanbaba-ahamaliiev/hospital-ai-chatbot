import os
import json
from datetime import datetime

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
import docx2txt
import re
from uuid import uuid4

from src.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

embedding = GoogleGenerativeAIEmbeddings(
    model=settings.pinecone.embedding_model,
    api_key=settings.gemini_api_key,
)

index_name = settings.pinecone.index_name

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=settings.pinecone.dimension,
        metric=settings.pinecone.metric,
        spec=ServerlessSpec(
            cloud=settings.pinecone.cloud,
            region=settings.pinecone.region,
        ),
    )

index = pc.Index(index_name)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embedding
)


def _load_pdf(path: str) -> list[Document]:
    """
    General.pdf — технічна документація з розділами по сторінках.
    Розбиваємо по сторінках: кожна сторінка = окремий смисловий блок.
    Додатково очищаємо зайві пробіли (PDF витягує текст з пробілами між словами).
    """

    loader = PyPDFLoader(path)
    pages = loader.load()

    ingested_at = datetime.now().isoformat()
    documents = []
    for page in pages:
        clean_text = re.sub(r' +', ' ', page.page_content).strip()
        if len(clean_text) < settings.pinecone.min_pdf_chunk_chars:
            continue
        page.page_content = clean_text
        page_num = page.metadata.get("page", 0) + 1
        page.metadata["file_name"] = "General.pdf"
        page.metadata["section_title"] = f"Сторінка {page_num}"
        page.metadata["ingested_at"] = ingested_at
        documents.append(page)

    return documents


def _load_docx(path: str) -> list[Document]:
    """
    For wokers.docx — HR-документ з чіткими розділами (1.1, 2.1 тощо).
    Розбиваємо по нумерованих заголовках — кожен розділ = окремий чанк.
    """

    text = docx2txt.process(path)

    pattern = r'(?=\n\d+\.(?:\d+\.?)* )'
    sections = re.split(pattern, text)

    ingested_at = datetime.now().isoformat()
    documents = []
    for section in sections:
        section = section.strip()
        if len(section) < settings.pinecone.min_docx_chunk_chars:
            continue
        section_title = section.split('\n')[0].strip()
        documents.append(Document(
            page_content=section,
            metadata={
                "file_name": "For wokers.docx",
                "section_title": section_title,
                "ingested_at": ingested_at,
            }
        ))

    return documents


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ingest_documents():
    documents = []
    documents.extend(_load_pdf(os.path.join(BASE_DIR, "data", "General.pdf")))
    documents.extend(_load_docx(os.path.join(BASE_DIR, "data", "For wokers.docx")))

    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)

    mapping = {
        uid: {
            "file_name": doc.metadata.get("file_name", ""),
            "section_title": doc.metadata.get("section_title", ""),
            "ingested_at": doc.metadata.get("ingested_at", ""),
        }
        for uid, doc in zip(uuids, documents)
    }
    mapping_path = os.path.join(BASE_DIR, "data", "pinecone_mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"Завантажено {len(documents)} чанків у Pinecone")
    print(f"Мапу ID збережено у {mapping_path}")


if __name__ == "__main__":
    ingest_documents()