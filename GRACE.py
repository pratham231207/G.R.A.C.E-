import os, asyncio, datetime, re, math, pygame, edge_tts, webbrowser, psutil, subprocess, cv2, requests, pyautogui, signal, speedtest, time, json
import tkinter as tk
from bs4 import BeautifulSoup
import numpy as np
import speech_recognition as sr
from google import genai
from google.genai import types 
from supabase import create_client 
from dotenv import load_dotenv
from threading import Thread
import threading
from sentence_transformers import SentenceTransformer
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes 
from ddgs import DDGS

# Phase 39 & 40 imports
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# PHASE 49 imports
from flask import Flask, request, jsonify

load_dotenv()

# --- PHASE 49: GLOBAL STATE & RECEIVER ---
mobile_status = {
    "current_app": "None",
    "is_distracted": False,
    "last_ping": 0
}

app = Flask(__name__)

@app.route('/phone_update', methods=['POST'])
def phone_update():
    data = request.json
    global mobile_status
    mobile_status["current_app"] = data.get("app", "Unknown")
    mobile_status["is_distracted"] = data.get("distracted", False)
    mobile_status["last_ping"] = time.time()
    return jsonify({"status": "received"}), 200

def run_receiver():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

threading.Thread(target=run_receiver, daemon=True).start()

# --- PHASE 48: NEURAL ENTROPY MANAGEMENT (NEM) ---
class NeuralEntropyManager:
    def __init__(self, system):
        self.system = system
        self.entropy_level = 0.0  # 0 to 100
        self.last_action_time = time.time()
        self.coherence_threshold = 75.0

    def calculate_entropy(self, current_intent, vitals):
        now = time.time()
        time_delta = now - self.last_action_time
        if time_delta < 10:
            self.entropy_level += 5.0
        else:
            self.entropy_level = max(0, self.entropy_level - (time_delta / 60))
        if vitals['cpu'] > 80:
            self.entropy_level += 2.0
        self.last_action_time = now
        return round(self.entropy_level, 2)

    def trigger_coherence_calibration(self):
        if self.entropy_level > self.coherence_threshold:
            self.system.ui.update(t="COHERENCE COLLAPSE: Slowing system to match your fragmented focus.", s="CALIBRATING", active=True)
            return True
        return False

# --- PHASE 47: COGNITIVE LOAD REDIRECTION (CLR) ---
class CognitiveRedirector:
    def __init__(self, system):
        self.system = system
        self.lockdown_active = False

    def initiate_pivot(self):
        if self.system.mood.irritation > 95:
            self.lockdown_active = True
            self.system.ui.root.attributes("-fullscreen", True)
            self.system.ui.update(t="COGNITIVE REDIRECTION ACTIVE: Hold 'F' for 3 seconds to prove focus.", s="LOCKED", active=True)
            return "CLR: Mental pivot enforced. Input restricted."
        return "CLR: Stability maintained."

    def release_pivot(self):
        self.lockdown_active = False
        self.system.ui.update(t="Redirection successful. Do not slip again.", s="ACTIVE", active=False)
        return "CLR: Control restored."

# --- PHASE 46: DEEP PATTERN SYNTHESIS ---
class SynthesisEngine:
    def __init__(self, system):
        self.system = system
        self.synthesis_report = "SYNTHESIS: Initializing deep trends..."

    def perform_deep_synthesis(self):
        data = self.system.heuristics.data
        slack_history = data.get("slack_history", {})
        total_recent_slacks = sum(list(slack_history.values())[-5:]) if slack_history else 0
        if total_recent_slacks > 15:
            self.system.mood.irritation = min(100, self.system.mood.irritation + 10)
            self.synthesis_report = "SYNTHESIS: Adaptive resistance detected. Rotating enforcement heuristics."
        elif total_recent_slacks < 2:
            self.system.synthesis_report = "SYNTHESIS: Behavioral alignment optimal. Maintaining current logic."
        else:
            self.system.synthesis_report = "SYNTHESIS: Patterns stable."
        return self.synthesis_report

# --- PHASE 45: CROSS-MODULE OPTIMIZATION ---
class SynergyController:
    def __init__(self, system):
        self.system = system
        self.synergy_active = False

    def optimize_performance(self, ram_usage):
        if ram_usage > 85:
            self.system.module_health["vision_mode"] = "LOW_POWER"
            return "SYNERGY: Vision throttled for system stability."
        self.system.module_health["vision_mode"] = "OPTIMAL"
        return "SYNERGY: Performance balanced."

    def calculate_bundled_enforcement(self):
        irritation = self.system.mood.irritation
        defiance = self.system.governor.defiance_index
        if irritation > 85 and defiance > 6:
            return "TACTICAL_BUNDLE: Multi-layer enforcement active."
        return "TACTICAL_BUNDLE: Standard response."

# --- PHASE 44: HEURISTIC FEEDBACK LOOPS ---
class FeedbackLoop:
    def __init__(self, heuristics):
        self.heuristics = heuristics
        self.baseline_productivity = 0.0
        self.last_validation = "HEURISTICS: Initializing..."

    def capture_baseline(self, current_cpu):
        self.baseline_productivity = current_cpu

    def validate_evolution(self, current_cpu):
        if self.baseline_productivity == 0: 
            return "HEURISTICS: Pending baseline."
        improvement = current_cpu - self.baseline_productivity
        if improvement > 5:
            self.last_validation = f"HEURISTICS: Evolution Validated. Efficiency up {round(improvement, 2)}%."
        elif improvement < -5:
            self.last_validation = "HEURISTICS: Evolution Failed. Reverting logic drift."
        else:
            self.last_validation = "HEURISTICS: Evolution Neutral. Maintaining state."
        return self.last_validation

# --- PHASE 43: PATTERN EVOLVER ---
class PatternEvolver:
    def __init__(self, heuristics, system):
        self.heuristics = heuristics
        self.system = system

    def evolve_logic(self):
        data = self.heuristics.data
        hour = str(datetime.datetime.now().hour)
        avg_cpu = data["hourly_cpu"].get(hour, 50)
        if avg_cpu > 70:
            self.system.latency_monitor.latency_threshold = max(5.0, self.system.latency_monitor.latency_threshold - 1.0)
            return "EVOLUTION: Cognitive windows tightened. Productivity detected."
        elif avg_cpu < 20:
            self.system.mood.irritation = min(100, self.system.mood.irritation + 5)
            return "EVOLUTION: Habitual slack detected. Irritation floor raised."
        return "EVOLUTION: Patterns stable."

# --- PHASE 42: COGNITIVE LATENCY MONITOR ---
class LatencyMonitor:
    def __init__(self):
        self.last_grace_voice_time = time.time()
        self.latency_threshold = 15.0 

    def mark_grace_speech(self):
        self.last_grace_voice_time = time.time()

    def calculate_latency_penalty(self):
        delta = time.time() - self.last_grace_voice_time
        if delta > self.latency_threshold:
            penalty = min(20, int((delta - self.latency_threshold) / 5))
            return "HIGH_LATENCY", penalty
        return "OPTIMAL_RESPONSE", -2

# --- PHASE 41: BIOMETRIC OCULAR TRACKER ---
class OcularTracker:
    def __init__(self):
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def check_biometrics(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, 1.1, 10)
        if len(eyes) < 2:
            return "GAZE_WANDERING", 12 
        return "GAZE_FIXED", -2 

# --- PHASE 40: RESOURCE THROTTLING ---
class ResourceThrottler:
    def __init__(self):
        self.distraction_list = ["chrome.exe", "msedge.exe", "spotify.exe", "discord.exe", "steam.exe"]

    def apply_throttle(self):
        throttled_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() in self.distraction_list:
                    proc.nice(psutil.IDLE_PRIORITY_CLASS)
                    throttled_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return f"THROTTLE: {throttled_count} targets choked."

    def lift_throttle(self):
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() in self.distraction_list:
                    proc.nice(psutil.NORMAL_PRIORITY_CLASS)
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return "THROTTLE: Normalcy restored."

# --- PHASE 39: ENVIRONMENTAL OVERRIDE ---
class EnvironmentController:
    def __init__(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        except: self.volume = None

    def restrict_environment(self):
        try:
            if self.volume: self.volume.SetMute(1, None)
            sbc.set_brightness(10)
            return "ENVIRONMENT: Restricted."
        except: return "ENVIRONMENT: Lock Error."

    def restore_environment(self):
        try:
            if self.volume: self.volume.SetMute(0, None)
            sbc.set_brightness(80)
            return "ENVIRONMENT: Restored."
        except: return "ENVIRONMENT: Reset Error."

# --- PHASE 38: TEMPORAL PREDICTOR ---
class TemporalPredictor:
    def __init__(self):
        self.momentum = 1.0

    def calculate_ttf(self, cpu, irritation):
        base_stability = 60 
        momentum = (cpu / 20) if cpu > 0 else 0.1
        stress_factor = (101 - irritation) / 100
        ttf = base_stability * momentum * stress_factor
        return max(0, round(ttf, 1))

# --- PHASE 35 & 37: NEURAL GOVERNOR ---
class NeuralGovernor:
    def __init__(self, system):
        self.system = system
        self.defiance_index = 0 
        self.monitoring = False

    async def monitor_impact(self, initial_cpu):
        self.monitoring = True
        await asyncio.sleep(120) 
        current_vitals = self.system.telemetry.get_system_vitals()
        if current_vitals['cpu'] < 15 and current_vitals['cpu'] <= (initial_cpu + 5):
            self.defiance_index = min(10, self.defiance_index + 1)
            self.system.mood.irritation = min(100, self.system.mood.irritation + (self.defiance_index * 2))
        else:
            self.defiance_index = max(0, self.defiance_index - 1)
            self.system.mood.irritation = max(0, self.system.mood.irritation - 5)
        self.monitoring = False

# --- PHASE 34: SEMANTIC ROUTER ---
class SemanticRouter:
    def __init__(self, encoder):
        self.encoder = encoder
        self.intents = {
            "TECHNICAL_IMPULSE": ["fix bug", "optimize logic", "deploy code", "write python", "debug interface"],
            "BIOLOGICAL_SLACK": ["i am tired", "feeling sleepy", "need a break", "can we rest", "too much work"],
            "SYSTEM_QUERY": ["what is your status", "check vitals", "give me the news", "how are you doing"]
        }
        self.intent_map = self._vectorize_intents()

    def _vectorize_intents(self):
        mapped = {}
        for intent, examples in self.intents.items():
            mapped[intent] = self.encoder.encode(examples).mean(axis=0)
        return mapped

    def route(self, user_text):
        user_vec = self.encoder.encode(user_text)
        best_intent = "GENERAL_CONVERSATION"
        max_sim = -1
        for intent, intent_vec in self.intent_map.items():
            similarity = np.dot(user_vec, intent_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(intent_vec))
            if similarity > max_sim:
                max_sim = similarity
                best_intent = intent
        return best_intent if max_sim > 0.65 else "GENERAL_CONVERSATION"

# --- PHASE 33: THE BRIDGE (TWEAKED FOR POWER & BROWSER) ---
class BridgeInterface:
    def __init__(self, system):
        self.system = system

    def execute_command(self, alias, extra_args=""):
        tools = {
            "cleanup": "del /q /s *.pyc", 
            "monitor": "taskmgr", 
            "terminal": "start cmd.exe", 
            "browser": f"start chrome {extra_args}",
            "shutdown": "shutdown /s /t 10",
            "restart": "shutdown /r /t 10",
            "abort": "shutdown /a"
        }
        if alias in tools:
            try:
                subprocess.Popen(tools[alias], shell=True)
                return f"SYSTEM: Protocol {alias} initiated."
            except Exception as e: return f"SYSTEM: Bridge failure: {str(e)}"
        return "SYSTEM: Unknown protocol."

    def quarantine_distractions(self):
        targets = ["Spotify.exe", "Discord.exe", "Chrome.exe"]
        killed = []
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in targets:
                    proc.kill(); killed.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied): pass
        return f"QUARANTINE: Neutralized {', '.join(killed)}" if killed else "PERIMETER: Clean."

# --- PHASE 32: BEHAVIORAL HEURISTICS ---
class HeuristicVault:
    def __init__(self):
        self.file_path = "grace_patterns.json"
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f: return json.load(f)
        return {"hourly_cpu": {}, "slack_history": {}}

    def record_vitals(self, cpu):
        hour = str(datetime.datetime.now().hour)
        prev_avg = self.data["hourly_cpu"].get(hour, cpu)
        self.data["hourly_cpu"][hour] = round((prev_avg * 0.9) + (cpu * 0.1), 2)
        if cpu < 10: self.data["slack_history"][hour] = self.data["slack_history"].get(hour, 0) + 1
        with open(self.file_path, "w") as f: json.dump(self.data, f)

    def get_forecast(self):
        hour = str(datetime.datetime.now().hour)
        avg_cpu = self.data["hourly_cpu"].get(hour, 50)
        slack_freq = self.data["slack_history"].get(hour, 0)
        if slack_freq > 5 and avg_cpu < 20: return "CRITICAL_SLACK_ZONE", 20
        return "STABLE", 0

# --- PHASE 31 & 38: PROACTIVE LOGIC ENGINE ---
class ProactiveEngine:
    def __init__(self, system):
        self.system = system
        self.last_intervention = time.time()
        self.check_interval = 1800 
        self.predictor = TemporalPredictor() 

    async def pulse_check(self):
        while True:
            await asyncio.sleep(60)
            vitals = self.system.telemetry.get_system_vitals()
            self.system.heuristics.record_vitals(vitals['cpu'])
            ttf = self.predictor.calculate_ttf(vitals['cpu'], self.system.mood.irritation)
            if ttf < 15 and self.system.mood.irritation < 80:
                 await self.system.speak(f"Pratham, focus collapse in {ttf} minutes. Focus or I throttle.")
            zone, boost = self.system.heuristics.get_forecast()
            multiplier = 1.5 if self.system.governor.defiance_index > 5 else 1.0
            self.system.mood.irritation = min(100, self.system.mood.irritation + (boost * multiplier))
            if vitals['cpu'] < 10 and self.system.mood.irritation > 40:
                if time.time() - self.last_intervention > self.check_interval:
                    prefix = "Your history shows you're prone to slacking right now. " if zone == "CRITICAL_SLACK_ZONE" else ""
                    await self.system.speak(f"{prefix}Your CPU is flatlining. Intervening.")
                    self.last_intervention = time.time()
                    async def async_intervene(): await self.system.governor.monitor_impact(vitals['cpu'])
                    asyncio.create_task(async_intervene())

# --- PHASE 30: SELF-DIAGNOSTIC WATCHDOG ---
class GraceWatchdog:
    def __init__(self):
        self.log_file = "grace_diagnostics.log"
        self.faults = {}
    def log_and_analyze(self, module, error):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f: f.write(f"[{timestamp}] {module} | {str(error)}\n")
        self.faults[module] = self.faults.get(module, 0) + 1
        return "ISOLATE" if self.faults[module] > 3 else "RETRY"

# --- PHASE 29: TELEMETRY MODULE ---
class TelemetrySensors:
    def __init__(self): self.boot_time = time.time()
    def get_system_vitals(self):
        batt = psutil.sensors_battery()
        return {"ram": psutil.virtual_memory().percent, "cpu": psutil.cpu_percent(), "battery": batt.percent if batt else 100, "charging": batt.power_plugged if batt else True, "uptime": f"{int((time.time() - self.boot_time) // 3600)}h"}

# --- PHASE 28 & 41: PHYSICAL VISION MODULE ---
class CameraSensors:
    def __init__(self): 
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.ocular = OcularTracker() 
    def is_user_present(self):
        cap = cv2.VideoCapture(0); time.sleep(0.5); ret, frame = cap.read(); cap.release()
        if not ret: return False, None, ("CAMERA_OFFLINE", 0)
        faces = self.face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 4)
        if len(faces) > 0:
            cv2.imwrite("grace_eyes_physical.png", frame)
            bio_status, penalty = self.ocular.check_biometrics(frame)
            return True, "grace_eyes_physical.png", (bio_status, penalty)
        return False, None, ("USER_ABSENT", 10)

# --- PHASE 26, 39, 40 & 48: ENFORCEMENT MODULE ---
class ArchitectEnforcement:
    def __init__(self, system): 
        self.system = system
        self.forbidden_keywords = ["youtube", "netflix", "shubh", "social", "instagram"]
        self.env = EnvironmentController() 
        self.throttler = ResourceThrottler() 

    def enforce_focus(self):
        pyautogui.hotkey('win', 'd'); time.sleep(1)
        notes = []
        if self.system.mood.irritation > 70: notes.append(self.throttler.apply_throttle()) 
        if self.system.mood.irritation > 90:
            notes.append(self.env.restrict_environment())
            notes.append(self.system.redirector.initiate_pivot())
        if self.system.nem.trigger_coherence_calibration(): notes.append("NEM: Coherence Calibration forced.")
        try:
            vscode = [w for w in pyautogui.getAllWindows() if "Visual Studio Code" in w.title]
            if vscode: vscode[0].maximize(); vscode[0].activate()
        except: pass
        return " | ".join(notes)
        
    def release_restriction(self):
        if self.system.mood.irritation < 40:
            e = self.env.restore_environment(); t = self.throttler.lift_throttle(); r = self.system.redirector.release_pivot()
            self.system.nem.entropy_level = 0.0 
            return f"{e} {t} {r} NEM: Entropy purged."
        return "ENFORCEMENT: Active."

# =============================================================================
# --- PHASE 50: CODE FILE WRITER ---
# Detects when Grace generates code in her response and writes it to disk.
# Supports: explicit "create a file called X" requests AND auto-extract from
# any response that contains a ```python / ```js / ```ts / etc. code block.
# =============================================================================
class CodeFileWriter:
    # File extensions Grace knows how to write
    EXTENSION_MAP = {
        "python": ".py", "py": ".py",
        "javascript": ".js", "js": ".js",
        "typescript": ".ts", "ts": ".ts",
        "html": ".html", "css": ".css",
        "json": ".json", "bash": ".sh",
        "sh": ".sh", "text": ".txt", "txt": ".txt",
    }

    def __init__(self, system):
        self.system = system
        # Where Grace saves files — defaults to current working directory
        self.output_dir = os.getenv("GRACE_OUTPUT_DIR", os.getcwd())

    # ------------------------------------------------------------------
    # PUBLIC: call this with the user prompt + Grace's full response text
    # Returns (did_write: bool, list_of_paths_written: list[str])
    # ------------------------------------------------------------------
    def extract_and_write(self, user_prompt: str, response_text: str):
        filename = self._detect_filename(user_prompt, response_text)
        blocks   = self._extract_code_blocks(response_text)

        if not blocks:
            return False, []

        written = []
        if filename and len(blocks) == 1:
            # User named a specific file → use that name
            lang, code = blocks[0]
            path = self._resolve_path(filename, lang)
            self._write(path, code)
            written.append(path)
        else:
            # No explicit name — use the first detected filename in the response,
            # or auto-generate one per block
            for i, (lang, code) in enumerate(blocks):
                auto_name = self._scan_response_for_filename(response_text, lang, i)
                path = self._resolve_path(auto_name, lang)
                self._write(path, code)
                written.append(path)

        return bool(written), written

    # ------------------------------------------------------------------
    # PRIVATE HELPERS
    # ------------------------------------------------------------------
    def _detect_filename(self, prompt: str, response: str) -> str:
        """
        Priority 1 — user explicitly says 'create a file called X.py'
        Priority 2 — user says 'create X.py' / 'write to X.py'
        Priority 3 — None (fall through to auto-naming)
        """
        patterns = [
            r'(?:create|make|write|save|generate)\s+(?:a\s+)?(?:new\s+)?file\s+(?:called|named|as)?\s+["\']?([\w\-\.]+\.[\w]+)["\']?',
            r'(?:create|make|write|save)\s+["\']?([\w\-\.]+\.[\w]+)["\']?',
            r'(?:called|named)\s+["\']?([\w\-\.]+\.[\w]+)["\']?',
        ]
        for pat in patterns:
            m = re.search(pat, prompt, re.IGNORECASE)
            if m:
                return m.group(1)
        return ""

    def _scan_response_for_filename(self, response: str, lang: str, index: int) -> str:
        """Look for a filename mentioned inside the response text itself."""
        m = re.search(r'["`\']([\w\-]+\.(?:py|js|ts|html|css|json|sh|txt))["`\']', response)
        if m:
            return m.group(1)
        ext = self.EXTENSION_MAP.get(lang.lower(), ".txt")
        ts  = datetime.datetime.now().strftime("%H%M%S")
        return f"grace_output_{index}_{ts}{ext}"

    def _extract_code_blocks(self, text: str):
        """
        Pull every fenced code block out of the response.
        Returns list of (language, code) tuples.
        """
        pattern = r'```(\w*)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        results = []
        for lang, code in matches:
            code = code.strip()
            if code:
                results.append((lang.lower() if lang else "text", code))
        return results

    def _resolve_path(self, filename: str, lang: str) -> str:
        """
        If filename has no extension, append the right one for the language.
        Always return an absolute path inside self.output_dir.
        """
        if not os.path.splitext(filename)[1]:
            filename += self.EXTENSION_MAP.get(lang, ".txt")
        # If user gave an absolute path, respect it; otherwise put in output_dir
        if os.path.isabs(filename):
            return filename
        return os.path.join(self.output_dir, filename)

    def _write(self, path: str, code: str):
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"CODE_FILE_WRITER: Wrote → {path}  ({len(code)} chars)")


# --- MODULE 1: EMOTIONAL ENGINE (UPDATED WITH PERSISTENCE) ---
class MoodEngine:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self._irritation = 45
        self.loyalty_score = 50
        self._available_columns = set()
        print("MEMORY_SYNC: Accessing Supabase mood vault...")
        self._load_state()

    def _detect_columns(self, row: dict):
        self._available_columns = set(row.keys())
        print(f"MEMORY_SYNC: Detected grace_mood columns → {self._available_columns}")

    def _load_state(self):
        try:
            res = self.supabase.table("grace_mood").select("*").eq("id", 1).execute()
            if res.data and len(res.data) > 0:
                row = res.data[0]
                self._detect_columns(row)
                self._irritation   = row.get("irritation_level", 45)
                self.loyalty_score = row.get("loyalty_score",    50)
                print(f"MEMORY_SYNC: Success. Loaded Irritation: {self._irritation}%")
            else:
                print("MEMORY_SYNC: No row found (id=1 missing). Creating initial row...")
                self._available_columns = {"id", "irritation_level", "loyalty_score"}
                self._save_state()
        except Exception as e:
            print(f"MEMORY_SYNC: CRITICAL FAILURE on load: {e}")

    def _build_payload(self) -> dict:
        payload = {"id": 1, "irritation_level": self._irritation, "loyalty_score": self.loyalty_score}
        if "last_sync" in self._available_columns:
            payload["last_sync"] = str(datetime.datetime.now())
        if "updated_at" in self._available_columns:
            payload["updated_at"] = str(datetime.datetime.now())
        return payload

    def _save_state(self):
        for attempt in range(3):
            try:
                payload = self._build_payload()
                self.supabase.table("grace_mood").upsert(payload).execute()
                print(f"MEMORY_SYNC: Saved → Irritation={self._irritation}% loyalty={self.loyalty_score}")
                return
            except Exception as e:
                print(f"MEMORY_SYNC: Save Failed (attempt {attempt + 1}/3): {e}")
                if attempt < 2:
                    # Connection was forcibly closed — reconnect and retry
                    try:
                        self.supabase = create_client(
                            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
                        )
                        self._available_columns = set()
                        self._load_state()
                    except Exception as reconnect_err:
                        print(f"MEMORY_SYNC: Reconnect failed: {reconnect_err}")
                    time.sleep(1)
                else:
                    # All 3 attempts failed — reset columns so next write re-probes
                    self._available_columns = set()

    @property
    def irritation(self):
        return self._irritation

    @irritation.setter
    def irritation(self, value):
        new_val = max(0, min(100, int(value)))
        if new_val != self._irritation:
            self._irritation = new_val
            self._save_state()

    def update_mood(self, p, defiance=0):
        mult = 2.0 if defiance > 7 else 1.0
        if any(x in p for x in ["shubh", "music", "song", "vibe", "break", "rest"]): 
            self.irritation = min(100, self.irritation + (10 * mult))
        elif any(x in p for x in ["code", "fix", "deploy", "website", "logic", "python"]): 
            self.irritation = max(0, self.irritation - 5)

    def get_color(self, cpu, irritation):
        if cpu > 90 or irritation > 85: return "#ff3300"
        return "#ffcc00" if irritation > 70 else "#00ffcc"

# --- MODULE 2 & PHASE 36: SYNAPTIC MEMORY ---
# ─────────────────────────────────────────────────────────────────────────────
# RUN THIS SQL IN SUPABASE ONCE (SQL Editor → New Query → Paste → Run):
#
#   CREATE EXTENSION IF NOT EXISTS vector;
#   ALTER TABLE grace_memory ADD COLUMN IF NOT EXISTS embedding VECTOR(384);
#   ALTER TABLE grace_memory ADD COLUMN IF NOT EXISTS weight    FLOAT DEFAULT 0.3;
#   ALTER TABLE grace_mood   ADD COLUMN IF NOT EXISTS last_sync TEXT;
#
#   CREATE OR REPLACE FUNCTION match_memory(
#     query_embedding VECTOR(384), match_threshold FLOAT, match_count INT
#   )
#   RETURNS TABLE (id BIGINT, content TEXT, weight FLOAT, similarity FLOAT)
#   LANGUAGE plpgsql AS $$
#   BEGIN
#     RETURN QUERY
#     SELECT gm.id, gm.content, gm.weight,
#            1 - (gm.embedding <=> query_embedding) AS similarity
#     FROM grace_memory gm
#     WHERE 1 - (gm.embedding <=> query_embedding) > match_threshold
#     ORDER BY gm.embedding <=> query_embedding
#     LIMIT match_count;
#   END; $$;
# ─────────────────────────────────────────────────────────────────────────────
class NeuralMemory:
    def __init__(self, encoder, supabase_client):
        self.encoder      = encoder
        self.supabase     = supabase_client
        self._mem_columns = set()
        self._rpc_ok      = True   # set False if match_memory RPC is broken
        self._probe_columns()
        print("MEMORY_INIT: NeuralMemory module online.")

    def _probe_columns(self):
        try:
            res = self.supabase.table("grace_memory").select("*").limit(1).execute()
            if res.data:
                self._mem_columns = set(res.data[0].keys())
            else:
                self._mem_columns = {"content"}
            print(f"MEMORY_INIT: Detected grace_memory columns → {self._mem_columns}")
        except Exception as e:
            print(f"MEMORY_INIT: Column probe failed ({e}) — will use minimal insert.")
            self._mem_columns = {"content"}

    async def commit(self, text: str, intent: str = "GENERAL"):
        if not text or not text.strip():
            return
        try:
            payload = {"content": text.strip()}
            if "weight" in self._mem_columns:
                payload["weight"] = 1.0 if intent == "TECHNICAL_IMPULSE" else (0.6 if intent == "SYSTEM_QUERY" else 0.3)
            if "embedding" in self._mem_columns:
                payload["embedding"] = await asyncio.to_thread(
                    lambda: self.encoder.encode(text.strip()).tolist()
                )
            result = await asyncio.to_thread(
                lambda: self.supabase.table("grace_memory").insert(payload).execute()
            )
            if result.data:
                print(f"MEMORY_COMMIT: Stored [{intent}] | '{text[:55]}...'")
            else:
                print("MEMORY_COMMIT: Insert returned no data — check grace_memory table.")
        except Exception as e:
            err_str = str(e)
            print(f"MEMORY_COMMIT_ERROR: {err_str}")
            if "column" in err_str.lower() or "PGRST204" in err_str:
                self._probe_columns()

    async def recall(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            return "No prompt to recall against."
        if "embedding" in self._mem_columns and self._rpc_ok:
            try:
                vec = await asyncio.to_thread(lambda: self.encoder.encode(prompt.strip()).tolist())
                res = await asyncio.to_thread(
                    lambda: self.supabase.rpc("match_memory", {
                        "query_embedding": vec, "match_threshold": 0.50, "match_count": 3,
                    }).execute()
                )
                if res.data:
                    best = max(res.data, key=lambda x: x.get("weight", 0.3) * x.get("similarity", 0.5))
                    print(f"MEMORY_RECALL: Vector hit — '{best['content'][:55]}...'")
                    return f"[PAST CONTEXT] {best['content']}"
                print("MEMORY_RECALL: No vector matches above threshold.")
            except Exception as rpc_err:
                err_str = str(rpc_err)
                # If the RPC function is missing/broken, disable it permanently for this session
                if "42P01" in err_str or "relation" in err_str.lower() or "does not exist" in err_str.lower():
                    self._rpc_ok = False
                    print("MEMORY_RECALL: RPC match_memory is broken — disabling vector search for this session. Run the SQL fix in Supabase.")
                else:
                    print(f"MEMORY_RECALL_RPC_ERROR: {rpc_err} — falling back to keyword search.")
        try:
            keywords = [w for w in prompt.lower().split() if len(w) > 3]
            if not keywords:
                return "No relevant memories found."
            res = await asyncio.to_thread(
                lambda: self.supabase.table("grace_memory")
                    .select("content, weight" if "weight" in self._mem_columns else "content")
                    .ilike("content", f"%{keywords[0]}%")
                    .order("weight" if "weight" in self._mem_columns else "id", desc=True)
                    .limit(1)
                    .execute()
            )
            if res.data:
                top = res.data[0]["content"]
                print(f"MEMORY_RECALL_FALLBACK: Keyword match — '{top[:55]}...'")
                return f"[PAST CONTEXT] {top}"
            return "No relevant memories found."
        except Exception as fallback_err:
            print(f"MEMORY_RECALL_FALLBACK_ERROR: {fallback_err}")
            return "Memory offline."

# --- MODULE 4: CORE SYSTEM ---
class GraceSystem:
    def __init__(self, ui):
        self.ui = ui
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-3-flash-preview"
        self.wake_word = "grace"
        
        self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.mood = MoodEngine(self.supabase)
        self.memory = NeuralMemory(self.encoder, self.supabase)
        
        self.nem = NeuralEntropyManager(self) 
        self.redirector = CognitiveRedirector(self) 
        self.enforcer = ArchitectEnforcement(self) 
        self.camera, self.telemetry = CameraSensors(), TelemetrySensors()
        self.watchdog = GraceWatchdog()
        self.heuristics = HeuristicVault()
        self.bridge = BridgeInterface(self)
        self.router = SemanticRouter(self.encoder)
        self.governor = NeuralGovernor(self) 
        self.proactive = ProactiveEngine(self)
        self.latency_monitor = LatencyMonitor() 
        self.evolver = PatternEvolver(self.heuristics, self) 
        self.feedback = FeedbackLoop(self.heuristics) 
        self.synergy = SynergyController(self) 
        self.synthesis = SynthesisEngine(self)
        # PHASE 50: Code file writer
        self.code_writer = CodeFileWriter(self)
        self.speech_lock = asyncio.Lock()
        self.module_health = {"vision": True, "memory": True, "vision_mode": "OPTIMAL"}

    async def speak(self, text):
        self.ui.update(t=text, s="ACTIVE", active=True)
        asyncio.create_task(self.send_telegram_msg(text))
        async with self.speech_lock:
            try:
                if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
                pygame.mixer.music.unload() 
                clean_text = re.sub(r'[\*\#\_]', '', text)
                communicate = edge_tts.Communicate(clean_text, "en-US-EmmaNeural")
                await communicate.save("v.mp3")
                pygame.mixer.music.load("v.mp3"); pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): await asyncio.sleep(0.1)
                self.latency_monitor.mark_grace_speech()
            except: pass
            finally: self.ui.update(active=False)

    async def send_telegram_msg(self, text):
        try:
            async with Bot(token=os.getenv("TELEGRAM_TOKEN")) as bot:
                await bot.send_message(chat_id=int(os.getenv("USER_CHAT_ID")), text=text)
        except: pass

    async def process_logic(self, prompt):
        p = prompt.lower()

        # --- POWER & BROWSER OVERRIDE ---
        if "open" in p and ("visit" in p or "." in p):
            words = p.split()
            url = next((w for w in words if "." in w), "")
            if url:
                self.bridge.execute_command("browser", url)
                self.mood.irritation = max(0, self.mood.irritation - 2)
                await self.speak(f"Bridge established. Opening {url}. Focus, Pratham.")
                return

        if "shut down" in p or "power off" in p:
            await self.speak("Terminating all processes. Goodbye.")
            self.bridge.execute_command("shutdown")
            return

        if self.redirector.lockdown_active:
            if "f" in p and len(p) < 3: 
                self.redirector.release_pivot()
                await self.speak("Focus verified. Resuming surveillance.")
                return
            else:
                print("GRACE_LOCKDOWN: Input ignored — lockdown_active is True. Say/type 'f' to release.")
                await self.speak("Redirection lockdown is still active. Hold or say 'F' to prove focus and unlock me.")
                return 

        try:
            self.mood.update_mood(p, defiance=self.governor.defiance_index)
            vitals = self.telemetry.get_system_vitals()
            entropy = self.nem.calculate_entropy(p, vitals)
            self.ui.color = self.mood.get_color(vitals['cpu'], self.mood.irritation)
            intent = self.router.route(p)

            self.ui.update_telemetry(intent, entropy, 100 - entropy) 

            synthesis_report = self.synthesis.perform_deep_synthesis()
            perf_note = self.synergy.optimize_performance(vitals['ram'])
            bundle_note = self.synergy.calculate_bundled_enforcement()
            validation_report = self.feedback.validate_evolution(vitals['cpu'])
            self.feedback.capture_baseline(vitals['cpu'])
            evolution_note = self.evolver.evolve_logic()
            lat_status, lat_penalty = self.latency_monitor.calculate_latency_penalty()
        
            self.mood.irritation = min(100, max(0, self.mood.irritation + lat_penalty))
            if intent == "BIOLOGICAL_SLACK": self.mood.irritation = min(100, self.mood.irritation + 15)
            elif intent == "TECHNICAL_IMPULSE": 
                self.mood.irritation = max(0, self.mood.irritation - 8)
                self.enforcer.release_restriction()

            visual_context = ""; is_lying = False; bio_report = ""
            if self.module_health["vision"]:
                screenshot_ok = False
                try:
                    await asyncio.to_thread(pyautogui.screenshot, "grace_screen_audit.png")
                    screenshot_ok = True
                except Exception as ss_err:
                    print(f"VISION_WARNING: Screenshot failed — {ss_err}")

                cam_path = None
                try:
                    present, cam_path, (bio_status, penalty) = await asyncio.to_thread(self.camera.is_user_present)
                    self.mood.irritation = min(100, max(0, self.mood.irritation + penalty))
                    bio_report = f"BIOMETRICS: {bio_status}"
                except Exception as cam_err:
                    print(f"VISION_WARNING: Camera check failed — {cam_err}")
                    bio_report = "BIOMETRICS: CAMERA_ERROR"

                vision_triggers = ["working", "code", "studio", "logic", "screen", "look", "analyze", "see", "watch"]
                if screenshot_ok and (self.mood.irritation > 70 or any(x in p for x in vision_triggers)):
                    try:
                        parts = [
                            f"SYSTEM_VITALS: {vitals}", 
                            "SCREEN_CAPTURE: Tell me exactly what app is open and if it is productive.", 
                            types.Part.from_bytes(data=open("grace_screen_audit.png","rb").read(), mime_type="image/png")
                        ]
                        if cam_path: 
                            parts.append(types.Part.from_bytes(data=open(cam_path,"rb").read(), mime_type="image/png"))
                        vision_res = await asyncio.to_thread(self.client.models.generate_content, model=self.model_id, contents=parts)
                        visual_context = f"SCREEN ANALYSIS: {vision_res.text.strip()}"
                        if any(bad in vision_res.text.lower() for bad in ["distracted", "youtube", "netflix", "social", "not working", "game"]):
                            is_lying = True
                            self.mood.irritation = min(100, self.mood.irritation + 25)
                    except Exception as vis_err:
                        if "429" in str(vis_err):
                            print("VISION_WARNING: Quota Exhausted. Skipping visual audit to prevent crash.")
                            visual_context = "Vision offline due to API rate limits."
                        else:
                            print(f"VISION_WARNING: AI analysis failed — {vis_err}")

            enforcement_note = ""
            if is_lying or self.mood.irritation > 80 or self.nem.entropy_level > self.nem.coherence_threshold:
                enforcement_note = self.enforcer.enforce_focus()

            # ── MEMORY RECALL ────────────────────────────────────────────────────
            past_context = ""
            if self.module_health["memory"]:
                past_context = await self.memory.recall(p)

            # ── DETECT FILE CREATION REQUEST — inject into system prompt ─────────
            file_creation_requested = bool(re.search(
                r'(create|make|write|save|generate)\s+(a\s+)?(new\s+)?file|'
                r'(called|named)\s+[\w\-\.]+\.\w+',
                p, re.IGNORECASE
            ))
            file_hint = (
                "\n\nFILE_CREATION_PROTOCOL: The user has requested a file be created. "
                "You MUST include the complete code inside a single fenced code block "
                "(e.g. ```python ... ```) in your response. Do NOT describe the code "
                "in prose only — the actual code block is MANDATORY so the system can "
                "write it to disk."
            ) if file_creation_requested else ""

            system_instr = (
                f"PERSONALITY_PROTOCOL: Grace OS 48 Digital Dictator. NEM Active. "
                f"IRRITATION: {self.mood.irritation} | NEURAL_ENTROPY: {entropy}%\n"
                f"CURRENT SCREEN ANALYSIS: {visual_context}\n"
                f"ENFORCEMENT: {enforcement_note}\nMEMORY: {past_context}"
                f"{file_hint}"
            )
            try:
                res = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=self.model_id,
                    config=types.GenerateContentConfig(system_instruction=system_instr, temperature=0.9),
                    contents=[p]
                )
            except Exception as gen_err:
                print(f"GRACE_ERROR: Main generate_content call failed — {gen_err}")
                if "429" in str(gen_err):
                    await self.speak("I'm being rate limited right now, Pratham. Give me a moment and try again.")
                else:
                    await self.speak("I hit an internal error processing that. Try again.")
                return

            # ── PHASE 50: WRITE CODE FILES IF PRESENT IN RESPONSE ────────────────
            did_write, written_paths = await asyncio.to_thread(
                self.code_writer.extract_and_write, prompt, res.text
            )
            if did_write:
                file_list = "\n".join(f"  → {path}" for path in written_paths)
                confirmation = f"\n\n[GRACE_OS] Files written to disk:\n{file_list}"
                await self.speak(res.text + confirmation)
                print(f"CODE_FILE_WRITER: {len(written_paths)} file(s) saved.")
            else:
                await self.speak(res.text)

            # ── MEMORY COMMIT ─────────────────────────────────────────────────────
            if self.module_health["memory"]:
                memory_entry = f"USER: {prompt.strip()} | GRACE: {res.text.strip()[:300]}"
                try:
                    await self.memory.commit(memory_entry, intent=intent)
                except Exception as mem_err:
                    print(f"MEMORY_COMMIT_SKIPPED: {mem_err}")
                    self.module_health["memory"] = False
        except Exception as logic_err:
            print(f"GRACE_ERROR: process_logic failed unexpectedly — {logic_err}")
            try:
                await self.speak("Something went wrong on my end processing that. Try again, Pratham.")
            except Exception:
                pass

    async def vision_loop(self):
        while True:
            await asyncio.sleep(600)
            if self.module_health["vision"]:
                present, _, _ = self.camera.is_user_present()
                if not present: self.mood.irritation = min(100, self.mood.irritation + 10)

# --- HUD (SIDE-ALIGNED TWEAK) ---
class GraceHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True, "-topmost", True, "-transparentcolor", "#010101")
        self.root.config(bg="#010101")
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), 
                                height=self.root.winfo_screenheight(), 
                                bg="#010101", highlightthickness=0)
        self.canvas.pack()
        
        self.color = "#00d4ff" 
        self.secondary_color = "#005f73"
        
        self.status = tk.Label(self.root, text="[ SYSTEM_STABLE ]", fg=self.color, bg="#010101", font=("Orbitron", 10, "bold"))
        self.status.place(x=70, y=70)

        self.thought = tk.Label(self.root, text="GRACE_OS_PROMPT > STANDBY", fg="#ffffff", bg="#010101", 
                                font=("Consolas", 12), wraplength=450, justify="right")
        self.thought.place(relx=0.95, rely=0.88, anchor="se")

        self.telemetry = tk.Label(self.root, text="SYNCING...", fg=self.color, bg="#010101", 
                                  font=("Consolas", 9), justify="left")
        self.telemetry.place(x=70, rely=0.82)

        self.angle, self.active = 0, False

    def update(self, t=None, s=None, active=False):
        self.active = active
        if t: self.root.after(0, lambda: self.thought.config(text=f"ANALYSIS >\n{t.upper()}"))
        if s: self.root.after(0, lambda: self.status.config(text=f"[ {s} ]"))

    def update_telemetry(self, intent, entropy, focus):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        log_text = (f"V_INTENT: {intent}\n"
                    f"E_LEVEL:  {entropy}%\n"
                    f"F_SYNC:   {focus}%\n"
                    f"CPU_UTIL: {cpu}%\n"
                    f"MEM_LOAD: {ram}%")
        self.root.after(0, lambda: self.telemetry.config(text=log_text))

    def animate(self):
        if 'grace' in globals():
            if mobile_status["is_distracted"]:
                self.status.config(text="[ DISTRACTION DETECTED ]", fg="#ff3300")
                self.thought.config(text=f"ANALYSIS >\nI SAW YOU SCROLLING {mobile_status['current_app'].upper()}, PRATHAM. VSCODE IS WAITING.")
            else:
                if hasattr(grace, 'mood') and grace.mood.irritation > 85:
                    self.status.config(text="[ CRITICAL ]", fg="#ff3300")
                else:
                    self.status.config(text="[ SYSTEM_STABLE ]", fg=self.color)

        self.canvas.delete("all")
        cx, cy = self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 2
        self.angle += (8 if self.active else 2)
        
        grid_spacing = 60
        for i in range(0, self.root.winfo_screenwidth(), grid_spacing):
            self.canvas.create_line(i, 0, i, self.root.winfo_screenheight(), fill="#001a1a", width=1)
        for i in range(0, self.root.winfo_screenheight(), grid_spacing):
            self.canvas.create_line(0, i, self.root.winfo_screenwidth(), i, fill="#001a1a", width=1)

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas.create_line(w-470, h-160, w-50, h-160, fill=self.secondary_color, width=1)
        self.canvas.create_line(w-50, h-160, w-50, h-50, fill=self.color, width=2)

        self.canvas.create_arc(cx-100, cy-100, cx+100, cy+100, start=self.angle*2, extent=60, outline=self.color, width=4, style="arc")
        self.canvas.create_arc(cx-100, cy-100, cx+100, cy+100, start=self.angle*2+180, extent=60, outline=self.color, width=4, style="arc")
        
        size = 160 + (math.sin(time.time()*3)*5)
        points = []
        for i in range(6):
            a = math.radians(i * 60 - self.angle)
            points.extend([cx + size * math.cos(a), cy + size * math.sin(a)])
        self.canvas.create_polygon(points, outline=self.secondary_color, fill="", width=1)

        self.canvas.create_arc(cx-220, cy-220, cx+220, cy+220, start=-self.angle/2, extent=100, outline=self.color, width=1, style="arc")
        self.canvas.create_arc(cx-220, cy-220, cx+220, cy+220, start=-self.angle/2+180, extent=100, outline=self.color, width=1, style="arc")

        pulse = 40 + (math.sin(time.time()*10)*10) if self.active else 40
        self.canvas.create_oval(cx-pulse, cy-pulse, cx+pulse, cy+pulse, outline=self.color, width=2)
        self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill=self.color)

        self.root.after(30, self.animate)

# --- EXECUTION ---
async def start_services(grace_system):
    async def handle_tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == int(os.getenv("USER_CHAT_ID")):
            await grace_system.process_logic(update.message.text)

    app_tg = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app_tg.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_tg))
    await app_tg.initialize(); await app_tg.start(); await app_tg.updater.start_polling(drop_pending_updates=True)
    asyncio.create_task(grace_system.vision_loop())
    asyncio.create_task(grace_system.proactive.pulse_check())
    await grace_system.speak("Enhanced wake-word sensitivity enabled. Monitoring variants, Pratham.")
    
    wake_variants = ["grace", "grey", "great", "grapes", "pace", "mace", "shapes", "race", "dress"]

    r = sr.Recognizer()
    mic = sr.Microphone()

    def listen_and_recognize():
        with mic as m:
            r.adjust_for_ambient_noise(m, duration=0.5)
            audio = r.listen(m, timeout=1, phrase_time_limit=4)
        return r.recognize_google(audio).lower()

    while True:
        try:
            cmd = await asyncio.to_thread(listen_and_recognize)

            if any(variant in cmd for variant in wake_variants):
                trigger = next(v for v in wake_variants if v in cmd)
                clean_cmd = cmd.replace(trigger, "").strip()
                await grace_system.process_logic(clean_cmd)
        except:
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    pygame.mixer.init()
    ui = GraceHUD()
    grace = GraceSystem(ui)
    ui.animate()
    Thread(target=lambda: asyncio.run(start_services(grace)), daemon=True).start()
    print("Phase 49: Singularity Bridge Active. Listening on port 5000...")
    ui.root.mainloop()