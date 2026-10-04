from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompt(name: str) -> str:
    """
    Завантажує текст промпта за назвою файлу.

    :param name: назва файлу (наприклад, 'system' або 'system.txt')
    :return: вміст файлу промпта як рядок
    """
    file_name = name if name.endswith(".txt") else f"{name}.txt"
    prompt_file = PROMPTS_DIR / file_name

    if not prompt_file.exists():
        raise FileNotFoundError(f"Файл промпта не знайдено: {prompt_file}")

    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read().strip()
