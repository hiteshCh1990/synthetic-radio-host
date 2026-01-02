
import ipywidgets as widgets
from IPython.display import display, Audio, clear_output
from engine import generate_radio_show_from_script
from openai import OpenAI
import wikipedia

# ===============================
# 🔑 OPENAI API KEY
# ===============================
OPENAI_API_KEY = "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"
client = OpenAI(api_key="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")

# ===============================
# GLOBAL STATE
# ===============================
current_script = None
current_topic = None

# ===============================
# UI ELEMENTS
# ===============================

title = widgets.HTML("<h2>🎙️ Radio AI – Smart RJ Generator</h2>")

topic_input = widgets.Text(
    placeholder="Enter Wikipedia topic (e.g. National Stock Exchange)",
    description="Topic:",
    layout=widgets.Layout(width="70%")
)

status = widgets.HTML("<b>Status:</b> Waiting")

generate_btn = widgets.Button(
    description="🎧 Generate Audio",
    button_style="success",
    layout=widgets.Layout(width="40%")
)

approve_btn = widgets.Button(
    description="✅ Approve & Continue",
    button_style="info",
    disabled=True,
    layout=widgets.Layout(width="40%")
)

regen_btn = widgets.Button(
    description="🔁 Regenerate Script",
    button_style="warning",
    disabled=True,
    layout=widgets.Layout(width="40%")
)

script_box = widgets.Textarea(
    layout=widgets.Layout(width="95%", height="360px"),
    disabled=True
)

output = widgets.Output()

# ===============================
# SCRIPT GENERATION
# ===============================

def generate_script():
    global current_script

    status.value = "🔍 Fetching Wikipedia content"
    wiki = wikipedia.summary(current_topic, sentences=20)

    status.value = "✍️ Writing radio conversation"

    prompt = f"""
You are a professional Indian FM RJ.

STRICT RULES:
- EXACTLY 30 lines
- 15 lines start with Anjli:
- 15 lines start with Hitesh:
- Hinglish, casual RJ tone
- Always use station name "Radio AI"
- Never use "Radio XYZ"
- Only dialogue

Topic:
{wiki}

Output ONLY dialogue.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    current_script = response.choices[0].message.content.strip()
    script_box.value = current_script
    script_box.disabled = False

    approve_btn.disabled = False
    regen_btn.disabled = False

    status.value = "📖 Review the script, then approve or regenerate"

# ===============================
# AUDIO GENERATION (APPROVED SCRIPT ONLY)
# ===============================

def generate_audio():
    with output:
        clear_output()
        status.value = "🎙️ Generating audio from approved script"

        approved_script = script_box.value.strip()
        if not approved_script:
            print("❌ Script is empty")
            return

        def progress(msg):
            print(msg)

        audio = generate_radio_show_from_script(
            approved_script,
            progress
        )

        status.value = "✅ Radio show complete"
        display(Audio(audio))

# ===============================
# BUTTON HANDLERS
# ===============================

def on_generate_clicked(b):
    global current_topic
    current_topic = topic_input.value.strip()

    if not current_topic:
        status.value = "❌ Please enter a topic"
        return

    approve_btn.disabled = True
    regen_btn.disabled = True
    script_box.disabled = True

    generate_script()

def on_approve_clicked(b):
    approve_btn.disabled = True
    regen_btn.disabled = True
    generate_audio()

def on_regen_clicked(b):
    approve_btn.disabled = True
    regen_btn.disabled = True
    generate_script()

generate_btn.on_click(on_generate_clicked)
approve_btn.on_click(on_approve_clicked)
regen_btn.on_click(on_regen_clicked)

# ===============================
# DISPLAY GUI
# ===============================

display(
    widgets.VBox([
        title,
        topic_input,
        status,
        generate_btn,
        script_box,
        widgets.HBox([approve_btn, regen_btn]),
        output
    ])
)
