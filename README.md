# 🛡️ ThreatLens: AI-Driven Cyber Threat Intelligence Summarization
**Automated Summarization of Cybersecurity News for Threat Intelligence Monitoring**

---

## 📌 Project Overview

In today's cybersecurity landscape, the rapid growth of online information poses significant challenges for organizations trying to stay ahead of emerging threats. ThreatLens is developed as an AI-driven cyber threat intelligence platform designed to automate the process of gathering, analyzing, and summarizing cybersecurity news articles from a wide range of trusted sources. By leveraging natural language processing techniques, ThreatLens transforms lengthy and often overwhelming news content into concise, actionable summaries that enable security teams to monitor threats more efficiently. The system collects data through APIs and RSS feeds, processes the text to extract key insights, and structures the outputs for seamless integration into threat dashboards or security information systems. Through its lightweight, modular design, ThreatLens aims to reduce analyst workload, improve decision-making speed, and lay a foundation for future integration of advanced summarization models and expanded data source coverage.

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
- Expansion of data sources to include CVE alerts, dark web monitoring, security advisories, and vendor-specific threat feeds
---

## 👩‍💻 Contributors

- **Gayathri Rayudu** 
- **Rutuja Wani** 
- **Gavin** 
- **Gary** 

---
