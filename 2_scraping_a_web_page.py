#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

2_app.py
========
Este script é responsável por realizar o crawl (scraping) 
de uma página web e salvar os resultados em arquivos 
JSON, Markdown e CSV.

Run:
uv run 2_app.py
"""
import asyncio
import json
import csv
import os
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/" #"https://www.nbcnews.com/business",
        )
        #print(result.markdown)
        # Criar a pasta "data" se não existir:
        os.makedirs("./data", exist_ok=True)

        # 1. Salvar em arquivo JSON:
        with open("./data/resultado_crawl.json", "w", encoding="utf-8") as f:
            json.dump({
                "markdown": result.markdown.raw_markdown,
                "links": result.links,
                "metadata": result.metadata if hasattr(result, "metadata") else {},
                "media": result.media if hasattr(result, "media") else {} # media --> contém elementos como imagens, vídeos, áudio e tabelas.
            }, f, ensure_ascii=False, indent=4)
        
        # 2. Salvar apenas o conteúdo Markdown em arquivo de texto:
        with open("./data/resultado_crawl.md", "w", encoding="utf-8") as f:
            f.write(result.markdown.raw_markdown)
        
        # 3. Salvar links em CSV (exemplo):
        if hasattr(result, "links") and "internal" in result.links:
            with open("./data/resultado_crawl_links_internos.csv", "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["URL", "Texto", "Título"])
                for link in result.links["internal"]:
                    writer.writerow([
                        link.get("href", ""),
                        link.get("text", ""),
                        link.get("title", "")
                    ])



if __name__ == "__main__":
    asyncio.run(main())
