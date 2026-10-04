from langchain_community.utilities import SQLDatabase
from src.config import settings

db = SQLDatabase.from_uri(
    settings.supabase_url,
    sample_rows_in_table_info=2,
)
