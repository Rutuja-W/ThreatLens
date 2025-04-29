import openai
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import Elasticsearch
import time

openai.api_key = "use your api key"

# Elasticsearch setup HTTP Version
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=('yourusername', 'yourpassword'),  # Add your credentials here
    verify_certs=True,  # Disable certificate verification for testing; enable in production
    ca_certs="location/of/your/cert"
)


ORIGINAL_INDEX_NAME = "rss-feed"  # The original index name
NEW_INDEX_NAME = "rss-security-summary"   # The new index for storing summaries

# Create a new index if it doesn't already exist
def create_new_index():
    mapping = {
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword"},
                "url": {"type": "text"},
                "title": {"type": "text"},
                "original_content": {"type": "text"},
                "short_summary": {"type": "text"},
                "long_summary": {"type": "text"},
                "cve": {"type": "text"},
                "category": {"type": "text"},
                "@timestamp": {"type": "date"}
            }
        }
    }
    if not es.indices.exists(index=NEW_INDEX_NAME):
        es.indices.create(index=NEW_INDEX_NAME, body=mapping)
        print(f"Created new index: {NEW_INDEX_NAME}")
    else:
        print(f"Index {NEW_INDEX_NAME} already exists.")

# Load URLs from Elasticsearch that don't already have the "short_summary" or "long_summary" field
def load_urls_from_elastic():
    urls = []
    titles = []
    doc_ids = []
    try:
        # Query to fetch documents that do not already have summaries in the original index
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"exists": {"field": "link"}}  # Ensure the document has a "link" field
                    ],
                    "must_not": [
                        {"exists": {"field": "short_summary"}},  # Exclude documents with "short_summary"
                        {"exists": {"field": "long_summary"}}   # Exclude documents with "long_summary"
                    ]
                }
            },
            "size": 500  # Limit the number of documents fetched at a time
        }

        # Fetch documents from Elasticsearch
        results = es.search(index=ORIGINAL_INDEX_NAME, body=query)
        
        for hit in results['hits']['hits']:
            doc_id = hit["_id"]
            title = hit["_source"].get("title", "Untitled")
            link_field = hit["_source"].get("link")
            url = link_field if isinstance(link_field, str) and link_field.startswith("http") else None

            # Ensure valid URL
            if not url:
                print(f"Invalid or missing URL: {link_field}")
                continue

            # Check if this doc_id exists in NEW_INDEX_NAME with both summaries
            new_index_query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"doc_id": doc_id}},  # Match by doc_id
                            {"exists": {"field": "short_summary"}},
                            {"exists": {"field": "long_summary"}}
                        ]
                    }
                }
            }

            new_index_results = es.search(index=NEW_INDEX_NAME, body=new_index_query, size=1)
            if new_index_results["hits"]["total"]["value"] > 0:
                print(f"Skipping already summarized article in NEW_INDEX_NAME: {title}")
                continue

            # Add valid data to the lists
            urls.append(url)
            titles.append(title)
            doc_ids.append(doc_id)

            # Add the new "doc_id" field to the original index
            update_doc = {"doc": {"doc_id": doc_id}}
            es.update(index=ORIGINAL_INDEX_NAME, id=doc_id, body=update_doc)

    except Exception as e:
        print(f"Error loading URLs from Elasticsearch: {e}")
    
    return urls, titles, doc_ids


def fetch_article_content(url):
    """Fetch the article content from the URL."""
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            article_text = "\n".join([p.get_text() for p in paragraphs])
            return article_text
        else:
            print(f"Failed to retrieve article. Status code: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"An error occurred while fetching {url}: {e}")
        return None

async def summarize_article(session, title, article_content, max_tokens=5000):
    """Summarize the article in both short and long formats with relevant category and CVEs."""
    if not article_content:
        print(f"Skipping summarization for {title} due to missing content.")
        return None, None, None, None
    
    prompt = (
        f"[Persona] You are a knowledgeable assistant who provides concise summaries and categorizes content.\n\n"
        f"[Context] The article is titled '{title}'. The goal is to create summaries for different audiences and provide relevant category and any mentioned CVEs for categorization.\n\n"
        f"[Task] Provide the following information about the article:\n"
        f"    - Short Summary: 200 words aimed at a non-technical person.\n"
        f"    - Long Summary: 500 words aimed at a technical person.\n"
        f"    - CVE: A list of CVEs mentioned in the article. If no CVE is mentioned, return 'None'.\n"
#       f"    - Keywords: A list of relevant keywords or phrases that categorize the main topics of the article.\n\n"
        f"    - Category: Category the risk may impact which industry, from the following list (Energy, Technology, Healthcare, Finance, Consumer Goods, Education, Transportation, Media, Government, Hospitality), you can choose more than one but all the category should be in the list I provided.\n\n"
        f"[Format] Ensure each section is in plain text with no extra symbols.\n\n"
        f"Here is the content:\n{article_content}"
    )

    try:
        response = await session.post(
            'https://api.openai.com/v1/chat/completions',
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            },
            headers={"Authorization": f"Bearer {openai.api_key}"}
        )
        data = await response.json()
        summaries = data['choices'][0]['message']['content']

        # Parsing labeled sections
        short_summary = summaries.split("Short Summary:")[1].split("Long Summary:")[0].strip()
        long_summary = summaries.split("Long Summary:")[1].split("CVE:")[0].strip()
        cve = summaries.split("CVE:")[1].split("Category:")[0].strip()
        category = summaries.split("Category:")[1].strip().split(", ")

        return short_summary, long_summary, cve, category
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None, None, None, None

def store_in_new_index(doc_id, url, title, original_content, short_summary, long_summary, cve, category):
    """Store the summarized data in a new Elasticsearch index."""
    doc = {
        "doc_id": doc_id,
        "link": url,
        "title": title,
        "original_content": original_content,
        "short_summary": short_summary,
        "long_summary": long_summary,
        "cve": cve,
        "category": category,  # Store as a list
        "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

    try:
        es.index(index=NEW_INDEX_NAME, document=doc)
        print(f"Saved summarized article '{title}' to the new index '{NEW_INDEX_NAME}'.")
    except Exception as e:
        print(f"Error storing data in the new index: {e}")


async def main():
    # Ensure the new index exists
    # create_new_index()

    async with aiohttp.ClientSession() as session:
        # Fetch URLs, titles, and document IDs from Elasticsearch
        urls, titles, doc_ids = load_urls_from_elastic()
        
        # Fetch articles in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            fetch_tasks = [loop.run_in_executor(executor, fetch_article_content, url) for url in urls]
            articles_content = await asyncio.gather(*fetch_tasks)

        # Summarize and store each article individually
        for url, title, content, doc_id in zip(urls, titles, articles_content, doc_ids):
            print("summarizing")
            if content:  # Only proceed if content was successfully fetched
                short_summary, long_summary, cve, category = await summarize_article(session, title, content)
                if short_summary and long_summary:
                    print("storing")
                    store_in_new_index(doc_id, url, title, content, short_summary, long_summary, cve, category)

if __name__ == "__main__":
    asyncio.run(main())
