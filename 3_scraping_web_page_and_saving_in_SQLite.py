#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

3_scraping_web_page_and_saving_in_SQLite.py
===========================================
Este script é responsável por realizar o crawl (scraping) 
de uma página web e salvar os resultados em SQLite.

Run:
uv run 3_scraping_web_page_and_saving_in_SQLite.py
"""
import asyncio
import sqlite3
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/"  #"https://www.nbcnews.com/business",
        )
        
        # Salvar em SQLite:
        conn = sqlite3.connect("./data/crawl_resultados.db")
        cursor = conn.cursor()
        
        # Criar tabela se não existir:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY,
            url TEXT,
            title TEXT,
            content TEXT,
            data_crawl TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Inserir resultado:
        title = result.metadata.get("title", "") if hasattr(result, "metadata") else ""
        cursor.execute(
            "INSERT INTO resultados (url, title, content) VALUES (?, ?, ?)",
            ("https://openai.com/api/pricing/", title, result.markdown.raw_markdown)
        )
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    asyncio.run(main())

