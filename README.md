# 🤖 Weather Agent – AI-powered Autonomous Weather Assistant

**Live AI Agent using Google Gemini API**  
An autonomous AI agent that reasons, plans, and executes actions to fetch real-time weather data for any city using a structured workflow: `START → PLAN → TOOL → OBSERVE → OUTPUT`.

---

## Features
- Agentic workflow: Structured steps ensure reliable reasoning and tool usage.
- Live weather info: Fetches current weather from [wttr.in](https://wttr.in).
- Modular design: Easily add new tools or APIs to extend the agent.
- Error handling: Robustly manages API failures and rate limits.
- Structured outputs: JSON-based responses for reliable parsing and automation.

---

## Tech Stack
- Python 3.12+
- OpenAI SDK / Google Gemini 2.5 Flash
- Requests, dotenv
- JSON-based structured outputs

---

## Installation
```bash
git clone <your-repo-link>
cd weather-agent
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
````

Create a `.env` file with:

```
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

```bash
python agent.py
```

Example:

```
⛅ WEATHER AGENT
> What is the weather in London?
🤖 The current weather conditions in London are: ☀️ +18°C
```

---

## Demo

### Preview (10 sec)

[![Watch Preview](https://res.cloudinary.com/dt686xyud/video/upload/v1759859347/weather_agent_cropped-ezgif.com-video-speed_vjvdrd.gif)](https://res.cloudinary.com/dt686xyud/video/upload/v1759857219/weather_agent_pr2qio.webm)

> 💡 Click the preview above to watch the full 1-minute demo on Cloudinary.

### Full Video

Or directly watch the full 1-minute demo hosted on Cloudinary:

[▶ Watch Full 1-Minute Demo](https://res.cloudinary.com/dt686xyud/video/upload/v1759857219/weather_agent_pr2qio.webm)

---
