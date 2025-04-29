# 🛡️ ThreatLens: AI-Driven Cyber Threat Intelligence Summarization
**Automated Summarization of Cybersecurity News for Threat Intelligence Monitoring**

---

## 📌 Project Overview

ThreatLens addresses the need for efficient cyber threat monitoring by aggregating cybersecurity news from trusted sources and summarizing them using AI.  
The project aims to streamline information overload faced by security analysts by providing concise, actionable intelligence.  
Collected articles are automatically summarized and prepared for visualization in dashboard environments.

---

## 🛠️ Key Features

- Real-time news aggregation from APIs and RSS feeds
- Lightweight AI-based summarization pipeline
- Customizable news source and topic mappings
- Structured output for dashboard integration (NDJSON)
- Modular design for scalability and easy extension

---

## 📚 Data Sources

- **NewsAPI:** For cybersecurity-related headlines from trusted news outlets
- **Custom RSS Feeds:** Handpicked cybersecurity blogs, news sites, and advisory sources

---

## 🧩 System Components

- **Collection Module:** Fetches articles from NewsAPI and RSS feeds
- **Summarization Module:** Processes text articles to generate concise summaries using NLP methods
- **Export Module:** Converts summaries into dashboard-ready formats

---

## 🗂️ Directory Structure

ThreatLens/  
├── code/  
│   ├── Summarizer.py  
│   ├── newsapi.conf  
│   ├── rss-feed.conf  
│   ├── mapping.json  
│   ├── newsapi-feed-mappings.json  
│   ├── dashboard.ndjson  
├── docs/  
│   ├── R&D Report.pdf  
│   ├── Final presentation.pdf  
│   └── Poster (Coming Soon)  
├── .gitignore  
└── README.md  

---

## ⚙️ Setup Instructions

- Clone the repository:  
  `git clone https://github.com/your-username/threatlens.git`  
  `cd threatlens/code`

- Install required dependencies:  
  `pip install requests newspaper3k nltk`

- Configure API keys and feeds:  
  - Insert NewsAPI credentials into `newsapi.conf`
  - Edit `rss-feed.conf` for custom RSS sources

- Run the summarization script:  
  `python Summarizer.py`

- Summarized articles will be stored in structured files for further use.

---

## 🔬 Methodology

- Collect cybersecurity news articles using configured APIs and feeds
- Preprocess and clean article content to remove irrelevant noise
- Apply NLP-based extractive summarization techniques
- Structure and export the summarized outputs in NDJSON format for dashboard integration

---

## 📈 Key Outcomes

| Aspect                 | Description |
|-------------------------|-------------|
| Sources Supported       | NewsAPI, RSS feeds |
| Summarization Technique | Extractive summarization (NLP-based) |
| Output Format           | NDJSON for dashboard compatibility |

---

## 🚀 Future Work

- Integration of transformer-based abstractive summarizers (e.g., BART, T5)
- Development of a real-time updating dashboard interface
- Expansion of data sources to include CVE alerts, dark web monitoring, and threat advisories

---

## 👩‍💻 Contributors

- **Gayathri Rayudu** – Summarization system development, evaluation, documentation  
- **[Other Team Member Name]** – Feed collection integration, testing  
- **[Other Team Member Name]** – Dashboard data export design  
- **[Other Team Member Name]** – Reporting and presentation development  

---
