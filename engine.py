
import os
import requests
from pydub import AudioSegment

# ===============================
# 🔑 ELEVENLABS API KEY
# ===============================
ELEVENLABS_API_KEY = "sk_15846313afd9dc965a913202c6346b35ff56b9f37df607e7"

# ===============================
# 📁 PATHS
# ===============================
BASE_PATH = "/content"
AUDIO_PATH = f"{BASE_PATH}/RJ/Audios"
BG_MUSIC = f"{BASE_PATH}/RJ/bg_music.mp3"

os.makedirs(AUDIO_PATH, exist_ok=True)

# ===============================
# 🎙️ VOICE MAP (ONLY THESE)
# ===============================
VOICE_MAP = {
    "Anjli": "CtsswjMPVCOJeWrOc8lS",
    "Hitesh": "m5qndnI7u4OAdXhH0Mr5"
}

# ===============================
# 🎧 ELEVENLABS TTS
# ===============================
def generate_audio(text, voice_id, filename):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)

    with open(filename, "wb") as f:
        f.write(r.content)

# ===============================
# 🧠 FINAL ENGINE FUNCTION
# ===============================
def generate_radio_show_from_script(script_text, progress_callback=None):

    def log(msg):
        if progress_callback:
            progress_callback(msg)

    log("🎙️ Generating audio from approved script")

    dialogue = []
    for line in script_text.split("\n"):
        line = line.strip()
        if line.startswith("Anjli:"):
            dialogue.append(("Anjli", line[6:].strip()))
        elif line.startswith("Hitesh:"):
            dialogue.append(("Hitesh", line[7:].strip()))

    if not dialogue:
        raise Exception("No valid dialogue found in script")

    audio_segments = []

    for i, (speaker, text) in enumerate(dialogue):
        log(f"🔊 Voice {i+1}/{len(dialogue)}")
        filename = f"{AUDIO_PATH}/{i}_{speaker}.mp3"
        generate_audio(text, VOICE_MAP[speaker], filename)
        audio_segments.append(AudioSegment.from_mp3(filename))

    final_audio = sum(audio_segments)

    if os.path.exists(BG_MUSIC):
        log("🎼 Mixing background music")
        bg = AudioSegment.from_mp3(BG_MUSIC) - 12
        bg = bg * (len(final_audio)//len(bg)+1)
        final_audio = bg[:len(final_audio)].overlay(final_audio)

    final_audio.export("final_radio_show.mp3", format="mp3")

    log("✅ Radio show complete")
    return "final_radio_show.mp3"
