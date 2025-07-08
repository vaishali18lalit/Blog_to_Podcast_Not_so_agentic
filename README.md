# 📰 ➡️ 🎙️ Blog to Podcast: Agent vs Sequential Flow

This project explores two different implementations of a "Blog to Podcast" application:

- ✅ **Simple Sequential Flow** (`app.py`) — Uses direct API calls to scrape, summarize, and convert a blog post into a podcast.
- 🧠 **Agent-Based Flow** (`blog_to_podcast_agent.py`) — Uses an agent (via LangChain or similar orchestration) to perform the same steps using tools.

The core idea: **Should we really use an agent for this task? Or is a simple, sequential approach good enough?**

---

## 💡 Objective

This repo is not just about building a cool tool — it's about **evaluating trade-offs**:

| Aspect        | Sequential (`app.py`) | Agent-Based (`blog_to_podcast_agent.py`) |
|---------------|------------------------|-------------------------------------------|
| Simplicity    | ✅ Straightforward      | ❌ More complex setup                      |
| Flexibility   | ❌ Fixed flow           | ✅ Modular, step-by-step reasoning         |
| Performance   | ✅ Fast                 | ⚠️ Slightly slower                         |
| Cost          | ✅ Minimal API usage    | ⚠️ More tokens used                        |
| Usefulness    | ✅ For fixed workflows  | ✅ For dynamic or evolving tasks           |

---

## 🔧 Features

- 🔍 **Blog Scraping** using [Firecrawl API](https://www.firecrawl.dev/)
- 🧠 **Summarization** via OpenAI GPT-4 (within 2000 characters)
- 🎙️ **Podcast Audio Generation** via [ElevenLabs](https://www.elevenlabs.io/)
- 📤 **Streamlit UI** for easy testing and comparison
- 🔑 **Secure API Key Input** via sidebar

---

## 🔑 Requirements

- Python 3.8+
- API Keys for:
  - [OpenAI](https://platform.openai.com/account/api-keys)
  - [Firecrawl](https://www.firecrawl.dev/)
  - [ElevenLabs](https://www.elevenlabs.io/)

---

## 🚀 Setup

1. **Clone the repository**:


git clone https://github.com/vaishali18lalit/Blog_to_Podcast_Not_so_agentic.git
cd Blog_to_Podcast_Not_so_agentic

2. **Install Dependencies**

   pip install -r requirements.txt

3. **How to Run**

   *Simple Sequential Flow*

   streamlit run app.py

   *Agno Agentic Flow*

   streamlit run blog_to_podcast_agent.py


## How it works 

Enter your API keys in the sidebar

Paste the blog URL

Click "🎙️ Generate Podcast"

The app will:

✅ Scrape blog content (via Firecrawl)

✅ Summarize it (via GPT-4)

✅ Convert it to audio (via ElevenLabs)

✅ Let you listen to or download the podcast








