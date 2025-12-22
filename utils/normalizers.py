import re

def normalize_article(article: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", article.upper())

def clean_product_name(name: str) -> str:
    return re.sub(r"/\d+/$", "", name).strip()