# G.R.A.C.E — AI Productivity Enforcer

> An AI-powered desktop system that monitors your focus, enforces productivity, and adapts to your behavioral patterns in real time.

---

## What it does

G.R.A.C.E is not a chatbot. It's a persistent AI system that runs on your desktop and actively enforces focus using computer vision, behavioral analysis, and system-level controls.

- **Watches your screen and webcam** — detects what apps are open and whether you're actually looking at them
- **Tracks your mood and intent** — a dynamic irritation engine that escalates responses based on your behavior
- **Enforces focus** — throttles distracting processes (Discord, Spotify, Chrome), dims your screen, and locks your UI when you slack
- **Remembers everything** — vector-embedded memory stored in Supabase; recalls past context using semantic similarity
- **Learns your patterns** — heuristic engine builds hourly CPU baselines and predicts when you're likely to lose focus
- **Talks to you** — real-time voice responses via Microsoft Edge TTS
- **Works on your phone too** — Telegram bot + Flask server lets you send commands and receive alerts remotely
- **Writes code files to disk** — any code block in a response is automatically extracted and saved

---

## Tech stack

| Layer | Technology |
|---|---|
| AI Model | Google Gemini (multimodal — text + screen + camera) |
| Memory | Supabase (PostgreSQL + pgvector for semantic search) |
| Voice | Microsoft Edge TTS + SpeechRecognition + PyGame |
| Vision | OpenCV (face detection, eye tracking) |
| Embeddings | SentenceTransformers `all-MiniLM-L6-v2` |
| Notifications | Telegram Bot API |
| System Control | psutil, PyAutoGUI, pycaw, screen-brightness-control |
| HUD | Tkinter (animated sci-fi overlay) |
| Mobile Bridge | Flask (local REST endpoint) |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                  GraceSystem                │
│                                             │
│  MoodEngine ──► NeuralGovernor             │
│  NeuralMemory ──► SemanticRouter           │
│  ProactiveEngine ──► TemporalPredictor     │
│  HeuristicVault ──► PatternEvolver         │
│  ArchitectEnforcement ──► ResourceThrottler│
│  CameraSensors ──► OcularTracker           │
│  CodeFileWriter ──► disk                   │
│                                             │
│  Gemini AI ◄──► all modules                │
│  Supabase  ◄──► Memory + Mood persistence  │
└─────────────────────────────────────────────┘
         │                    │
    GraceHUD (Tkinter)   Telegram Bot
    Flask server (5000)
```

---

## Getting started

### Prerequisites
- Python 3.10+
- A working microphone and webcam
- Windows (uses Windows-specific audio APIs)

### Installation

```bash
# Clone the repo
git clone https://github.com/pratham231207/grace.git
cd grace

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Open .env and fill in your actual API keys
```

### Environment variables

```
GEMINI_API_KEY       — Google Gemini API key
SUPABASE_URL         — Your Supabase project URL
SUPABASE_KEY         — Your Supabase anon/service key
TELEGRAM_TOKEN       — Telegram bot token (from @BotFather)
USER_CHAT_ID         — Your Telegram chat ID
GRACE_OUTPUT_DIR     — (optional) Where code files get saved
```

### Supabase setup

Run this SQL once in your Supabase SQL editor:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE grace_memory ADD COLUMN IF NOT EXISTS embedding VECTOR(384);
ALTER TABLE grace_memory ADD COLUMN IF NOT EXISTS weight FLOAT DEFAULT 0.3;
ALTER TABLE grace_mood ADD COLUMN IF NOT EXISTS last_sync TEXT;
```

### Run

```bash
python GRACE.py
```

A fullscreen HUD will appear and GRACE will start listening for the wake word.

---

## Wake word

Say **"Grace"** (or close variants — grey, great, pace, race) followed by your command.

---

## Key modules

| Module | Description |
|---|---|
| `NeuralEntropyManager` | Tracks cognitive load based on input frequency and CPU usage |
| `CognitiveRedirector` | Locks UI fullscreen when focus is critically low |
| `HeuristicVault` | Stores hourly behavioral patterns in JSON |
| `PatternEvolver` | Adjusts enforcement thresholds based on learned history |
| `TemporalPredictor` | Predicts minutes until focus collapse |
| `SemanticRouter` | Classifies user intent using cosine similarity on embeddings |
| `NeuralGovernor` | Monitors whether interventions actually changed behavior |
| `CodeFileWriter` | Extracts and saves code blocks from AI responses to disk |

---

## Built by

Pratham — [GitHub](https://github.com/pratham231207)
