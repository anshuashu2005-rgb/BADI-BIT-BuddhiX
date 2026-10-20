import os, json, re, sqlite3, time, base64
from datetime import datetime
import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
load_dotenv()
ROOT=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(ROOT,"buddhix.db")
st.set_page_config(page_title="BuddhiX",page_icon="🧠",layout="wide")
st.markdown("""<style>
:root { color-scheme: dark; }
.stApp { background: radial-gradient(circle at 80% 0%,#18234a 0%,transparent 36%),linear-gradient(145deg,#080d1c 0%,#0d1428 58%,#080d1c 100%); color:#e8eeff; }
.block-container {max-width:1360px;padding-top:.8rem;padding-bottom:6rem;}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{background:transparent!important;}
[data-testid="stSidebar"]{background:#0b1122;border-right:1px solid #24365d;}
[data-testid="stSidebar"] *{color:#dce7ff;}
.stApp p,.stApp label,.stApp span,[data-testid="stMarkdownContainer"],[data-testid="stMarkdownContainer"] p,[data-testid="stCaptionContainer"]{color:#c4d0ef;}
.hero{padding:20px 24px;border:1px solid #344578;border-radius:20px;background:linear-gradient(110deg,#141e3b,#102a3a);margin-bottom:14px;box-shadow:0 8px 32px #02061766;}
.agent-strip{display:flex;align-items:center;gap:9px;padding:9px 12px;border:1px solid #293c69;border-radius:12px;background:rgba(17,26,49,.88);margin:0 0 12px;font-size:12px;color:#aebfe4;}
.agent-dot{width:8px;height:8px;border-radius:50%;background:#22d3ee;display:inline-block;box-shadow:0 0 0 4px #22d3ee24,0 0 12px #22d3ee; }
.tool-card h4{font-size:15px!important;margin-bottom:.3rem!important;}
.tool-card p{font-size:12px!important;line-height:1.35!important;}
.tool-card [data-testid="stVerticalBlock"]{gap:.45rem!important;}
.tool-card .stButton>button{min-height:2.1rem;padding:.25rem .55rem;font-size:12px;}
.tool-card [data-testid="stFileUploader"] section{padding:.4rem!important;}
.tool-card [data-testid="stFileUploader"] small{font-size:10px!important;}
.hero h1{font-size:clamp(1.8rem,3vw,2.5rem);line-height:1.15;margin:0 0 .45rem;color:#f3f6ff;}
.hero p{color:#a9badf;margin-bottom:0;}
.stButton>button,[data-testid="stFormSubmitButton"] button{border-radius:12px;min-height:2.55rem;background:linear-gradient(100deg,#6757f5,#287ef0);color:white!important;border:1px solid #8da9ff;font-weight:650;}
.stButton>button:hover{filter:brightness(1.05);transform:translateY(-1px);}
[data-testid="stMetric"]{background:#111a31;border:1px solid #2b3b66;border-radius:15px;padding:13px;box-shadow:0 5px 18px #00000022;}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"],[data-testid="stMetricDelta"]{color:#e1eaff!important;}
[data-testid="stChatMessage"]{background:#111a31;border:1px solid #2b3b66;border-radius:16px;padding:.8rem 1rem;margin:.55rem 0;}
/* Fix BuddhiX chat composer: force readable dark input and light text across Streamlit versions */
[data-testid="stChatInput"],
[data-testid="stChatInput"] form,
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div[data-baseweb="textarea"],
[data-testid="stChatInput"] div[data-baseweb="textarea"] > div {
  background:#101a30!important;
  background-color:#101a30!important;
  border:1px solid #3a4f83!important;
  border-radius:16px!important;
  box-shadow:0 8px 28px #0008!important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] textarea:active,
[data-baseweb="textarea"] textarea {
  background:transparent!important;
  background-color:transparent!important;
  color:#f0f5ff!important;
  -webkit-text-fill-color:#f0f5ff!important;
  caret-color:#22d3ee!important;
  opacity:1!important;
}
[data-testid="stChatInput"] textarea::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
  color:#aebfe4!important;
  -webkit-text-fill-color:#aebfe4!important;
  opacity:1!important;
}
[data-testid="stChatInput"] button {color:#eaf2ff!important;}
[data-testid="stChatInput"] svg {fill:#dce7ff!important;color:#dce7ff!important;}
[data-testid="stBottom"],[data-testid="stBottom"]>div,[data-testid="stBottomBlockContainer"],[data-testid="stBottomBlockContainer"]>div{background:#080d1c!important;background-color:#080d1c!important;}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-baseweb="select"]>div,[data-testid="stNumberInput"] input{background:#101a30!important;color:#eef4ff!important;border-color:#344873!important;border-radius:10px!important;}
[data-testid="stFileUploader"] section{background:#101a30;border:1px dashed #536ba5;border-radius:12px;}
[data-testid="stFileUploader"] *{color:#dce7ff!important;}
[data-testid="stSidebar"] [role="radiogroup"] label{border-radius:11px;padding:.48rem .6rem;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:linear-gradient(100deg,#183565,#19264b);border:1px solid #4d91ff;color:#f2f5ff;}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:.62rem .72rem;margin-bottom:.18rem;border:1px solid transparent;transition:all .18s ease;}
hr{border-color:#26375e!important;}
.dash-hero{position:relative;overflow:hidden;padding:30px 30px 24px;border:1px solid #254d82;border-radius:22px;background:radial-gradient(ellipse at 78% 30%,#1455a855,transparent 36%),linear-gradient(115deg,#07152e 0%,#0b1d3a 55%,#102d4b 100%);margin-bottom:18px;box-shadow:0 16px 42px #02081780;}
.dash-hero:after{content:'✦';position:absolute;right:8%;top:10%;font-size:140px;color:#3997ff15;pointer-events:none;}
.dash-kicker{display:inline-block;padding:5px 10px;border:1px solid #24568a;border-radius:999px;background:#10294a;color:#8dcaff!important;font-size:11px;letter-spacing:.06em;font-weight:700;}
.dash-hero h1{font-size:clamp(2.4rem,4vw,3.5rem);font-weight:850;letter-spacing:-.04em;line-height:1.02;margin:12px 0 4px;background:linear-gradient(90deg,#40c6ff,#7d8bff 62%,#c17aff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.dash-hero h3{font-size:1.35rem;color:#f0f5ff!important;margin:.25rem 0 .6rem;}
.dash-hero p{max-width:580px;color:#b9cbed!important;font-size:14px;}
.dash-card{height:100%;padding:16px 16px 14px;border:1px solid #253d66;border-radius:17px;background:linear-gradient(145deg,#101d36,#0d172b);box-shadow:0 8px 22px #02081744;margin-bottom:10px;}
.dash-card h4{color:#edf4ff!important;font-size:15px;margin:8px 0 4px;}
.dash-card p{color:#9eb3d9!important;font-size:12px;line-height:1.45;min-height:30px;}
.dash-icon{display:inline-flex;width:42px;height:42px;align-items:center;justify-content:center;border-radius:13px;background:linear-gradient(135deg,#1760c9,#5b55e9);font-size:23px;box-shadow:0 5px 18px #2269df44;}
.dash-section{font-size:19px;font-weight:750;color:#eaf1ff;margin:10px 0 12px;}
.dash-panel{padding:16px;border:1px solid #253d66;border-radius:17px;background:linear-gradient(145deg,#0e1a31,#0a1426);margin-bottom:12px;}
.subject-pill{display:block;padding:13px 12px;border:1px solid #2a4a79;border-radius:13px;background:linear-gradient(120deg,#14294a,#101c33);min-height:82px;margin-bottom:8px;}
.subject-pill b{color:#e8f2ff;font-size:12px;}.subject-pill small{color:#9eb8e3;font-size:11px;}
.dash-quick{padding:12px;border:1px solid #29436d;border-radius:13px;background:#101f39;min-height:80px;margin-bottom:8px;}
.dash-quick b{color:#eaf2ff;font-size:12px;}.dash-quick small{color:#9eb4d8;font-size:11px;}
[data-testid="stMetric"]{background:linear-gradient(145deg,#12223e,#0e192d);border-color:#2a4168;}
@keyframes dashFade{from{opacity:.25;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
[data-testid="stMain"] .block-container{animation:dashFade .32s ease-out both;}
hr{border-color:#26375e!important;}
.battle-card{padding:22px;border-radius:20px;background:radial-gradient(circle at 85% 15%,#b7a4ff35,transparent 30%),linear-gradient(135deg,#111b3d,#29205f 55%,#123a55);color:#fff;border:1px solid #897cff;box-shadow:0 12px 35px #6555ff20;}
.battle-card h2,.battle-card p{color:#fff!important;}
.battle-stat{padding:14px;border:1px solid #d8dfff;border-radius:16px;background:linear-gradient(145deg,#fff,#f1f5ff);box-shadow:0 7px 22px #304d8410;}
.battle-question{padding:16px 18px;border:1px solid #cbd8ff;border-radius:16px;background:linear-gradient(120deg,#ffffff,#f4f6ff);margin:8px 0;}
.battle-badge{display:inline-block;padding:5px 10px;border-radius:999px;background:#eee9ff;color:#4b35c7;font-size:12px;font-weight:700;}
[data-testid="stProgressBar"]>div>div{background:linear-gradient(90deg,#6b5cff,#12bde7);}
@media(max-width:700px){.block-container{padding-top:.7rem}.hero{padding:18px;border-radius:16px}}
</style>""", unsafe_allow_html=True)
con=sqlite3.connect(DB,check_same_thread=False)
con.execute("CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, created TEXT, topic TEXT, score INTEGER, total INTEGER, weak TEXT)")
con.execute("CREATE TABLE IF NOT EXISTS profile(id INTEGER PRIMARY KEY CHECK(id=1), name TEXT)")
con.execute("CREATE TABLE IF NOT EXISTS goals(id INTEGER PRIMARY KEY, goal TEXT, done INTEGER DEFAULT 0, day TEXT)")
con.execute("CREATE TABLE IF NOT EXISTS planner_tasks(id INTEGER PRIMARY KEY, task TEXT NOT NULL, subject TEXT DEFAULT 'General', due_date TEXT NOT NULL, minutes INTEGER DEFAULT 30, priority TEXT DEFAULT 'Medium', done INTEGER DEFAULT 0, created_at TEXT)")
# Persistent Study Battle reward ledger; separate from quiz attempts so existing DB data stays compatible.
con.execute("CREATE TABLE IF NOT EXISTS battle_rewards(id INTEGER PRIMARY KEY, created TEXT NOT NULL, topic TEXT NOT NULL, difficulty TEXT NOT NULL, xp INTEGER NOT NULL DEFAULT 0, correct INTEGER NOT NULL DEFAULT 0, total INTEGER NOT NULL DEFAULT 0, best_streak INTEGER NOT NULL DEFAULT 0, bonus INTEGER NOT NULL DEFAULT 0, elapsed_seconds INTEGER NOT NULL DEFAULT 0)")
con.commit()
def cfg():
    return {
        "key": os.getenv("ASI_ONE_API_KEY", "").strip(),
        "base": os.getenv(
            "ASI_ONE_BASE_URL",
            "https://openrouter.ai/api/v1"
        ).rstrip("/"),
        "model": os.getenv("ASI_ONE_MODEL", "openrouter/free")
    }


SYSTEM = (
    "You are BuddhiX, a helpful AI learning assistant for students. "
    "Give clear, structured, accurate explanations. Prefer concise but complete answers. "
    "For student attempts, diagnose the first error and explain the correction. Never invent missing values or claim certainty when the prompt is ambiguous."
)

LANGUAGE_RULES = {
    "Hinglish": "Respond in natural, easy Hinglish (Hindi written in Roman script mixed with English technical terms).",
    "Hindi": "Respond in clear, simple Hindi using Devanagari script. Keep standard technical terms/formulas in English where appropriate and explain them in Hindi.",
    "English": "Respond in clear, simple English."
}

def system_for_language(extra=""):
    language = st.session_state.get("response_language", "Hinglish")
    rule = LANGUAGE_RULES.get(language, LANGUAGE_RULES["Hinglish"])
    math_rule = (
        "MATH FORMATTING: Render every equation using standard Markdown math delimiters. "
        "Use $...$ for inline formulas and $$...$$ on separate lines for display equations. "
        "Never wrap equations in square brackets like [ ... ], and never show raw LaTeX commands as plain text. "
        "Use proper notation, e.g. $$Y = \\overline{S}A + SB$$. "
        "For worked calculations, put each important step on its own display-math line."
    )
    return SYSTEM + "\nLANGUAGE REQUIREMENT: " + rule + " Keep formulas accurate; define symbols and show steps for numerical problems. " + math_rule + " " + extra


def format_math(text):
    """Normalize common raw-LaTeX wrappers into Streamlit's supported math Markdown."""
    if not isinstance(text, str):
        return str(text)
    # Standard LaTeX delimiters are understood by Streamlit, but models sometimes mix them.
    text = re.sub(r"\\\[(.*?)\\\]", lambda m: "\n$$\n" + m.group(1).strip() + "\n$$\n", text, flags=re.S)
    text = re.sub(r"\\\((.*?)\\\)", lambda m: "$" + m.group(1).strip() + "$", text, flags=re.S)
    # Convert a standalone [ ... ] line to display math only when it clearly contains LaTeX/math syntax.
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if (stripped.startswith("[") and stripped.endswith("]") and len(stripped) > 2
                and re.search(r"\\|=|\\frac|\\sum|\\int|\\mathcal|\\overline|\\rightarrow|\\Rightarrow|\\begin", stripped)):
            inner = stripped[1:-1].strip()
            lines.extend(["$$", inner, "$$"])
        else:
            lines.append(line)
    return "\n".join(lines)


def call(messages, temperature=.25, max_tokens=1400):
    c = cfg()
    if not c["key"]:
        return None, "API key missing. Add ASI_ONE_API_KEY to .env and restart."
    try:
        r = requests.post(
            c["base"] + "/chat/completions",
            headers={
                "Authorization": "Bearer " + c["key"],
                "Content-Type": "application/json"
            },
            json={
                "model": c["model"],
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=75
        )
        if r.status_code >= 400:
            return None, f"API HTTP {r.status_code}: {r.text[:500]}"
        return r.json()["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)


def create_gemini_live_token():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None, "GEMINI_API_KEY is missing from your private .env file."
    try:
        from google import genai
        client = genai.Client(api_key=api_key, http_options={"api_version": "v1beta"})
        model = os.getenv("GEMINI_LIVE_MODEL", "gemini-3.8-live").strip()
        token = client.auth_tokens.create(config={
            "uses": 1,
            "live_connect_constraints": {
                "model": model,
                "config": {
                    "response_modalities": ["AUDIO"],
                    "input_audio_transcription": {},
                    "output_audio_transcription": {},
                    "system_instruction": (
                        "You are BuddhiX, a friendly student learning tutor. Speak naturally and conversationally. "
                        "Explain concepts clearly in simple Hinglish unless the student speaks another language. "
                        "Keep spoken answers reasonably concise, ask helpful follow-up questions, and let the student interrupt. "
                        "For study questions, teach step by step and never invent facts."
                    ),
                },
            },
            "http_options": {"api_version": "v1beta"},
        })
        token_name = getattr(token, "name", None)
        if not token_name:
            return None, "Gemini did not return a temporary Live API token. Check your API access and model."
        return {"token": token_name, "model": model}, None
    except ImportError:
        return None, "Gemini SDK is not installed. Run: pip install -r requirements.txt"
    except Exception as exc:
        return None, "Could not start Gemini Live. Check API access, model availability and quota. Details: " + str(exc)[:350]


def render_gemini_live(token_name, model):
    safe_token = json.dumps(token_name)
    safe_model = json.dumps(model)
    html = r'''<div style="font-family:system-ui;background:#101a30;border:1px solid #344873;border-radius:16px;padding:14px;color:#eef4ff">
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
        <button id="start" style="background:#6757f5;color:white;border:0;border-radius:10px;padding:10px 14px;font-weight:700;cursor:pointer">🎙️ Connect microphone</button>
        <button id="stop" disabled style="background:#263858;color:white;border:0;border-radius:10px;padding:10px 14px;font-weight:700;cursor:pointer">⏹ End session</button>
        <span id="status" style="font-size:12px;color:#a9badf">Ready to connect</span>
      </div>
      <div id="transcript" style="margin-top:12px;max-height:180px;overflow:auto;white-space:pre-wrap;font-size:13px;line-height:1.5;color:#dce7ff"></div>
      <div style="margin-top:8px;font-size:11px;color:#8fa6d2">Allow microphone access. Speak naturally; you can interrupt the tutor while it is talking. Uses Gemini Live API and may consume your API quota.</div>
    </div>
    <script>
    (() => {
      const token = TOKEN_PLACEHOLDER;
      const model = MODEL_PLACEHOLDER;
      const statusEl = document.getElementById('status');
      const transcriptEl = document.getElementById('transcript');
      const startBtn = document.getElementById('start');
      const stopBtn = document.getElementById('stop');
      let ws = null, micStream = null, micCtx = null, source = null, processor = null;
      let playCtx = null, nextPlayTime = 0, active = false, setupReady = false;
      let userLine = '', assistantLine = '';
      const setStatus = (s) => { statusEl.textContent = s; };
      // Visible diagnostics: if this does not appear, the embedded component script did not load.
      setStatus('Voice panel loaded — click Connect microphone');
      window.addEventListener('error', (event) => {
        setStatus('Browser script error: ' + (event.message || 'unknown error'));
      });
      window.addEventListener('unhandledrejection', (event) => {
        const reason = event.reason && event.reason.message ? event.reason.message : String(event.reason || 'unknown error');
        setStatus('Voice error: ' + reason);
      });
      const addLine = (who, txt) => {
        if (!txt) return;
        const div = document.createElement('div');
        div.style.marginTop = '6px';
        const b = document.createElement('b'); b.textContent = who + ': ';
        div.appendChild(b); div.appendChild(document.createTextNode(txt));
        transcriptEl.appendChild(div); transcriptEl.scrollTop = transcriptEl.scrollHeight;
      };
      const b64 = (bytes) => { let bin=''; const chunk=0x8000; for(let i=0;i<bytes.length;i+=chunk) bin+=String.fromCharCode(...bytes.subarray(i,i+chunk)); return btoa(bin); };
      const fromB64 = (s) => { const bin=atob(s); const out=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) out[i]=bin.charCodeAt(i); return out; };
      function downsampleTo16k(float32, inputRate) {
        if (inputRate === 16000) return float32;
        const ratio = inputRate / 16000, len = Math.floor(float32.length / ratio), out = new Float32Array(len);
        for (let i=0;i<len;i++) { const start=Math.floor(i*ratio), end=Math.min(Math.floor((i+1)*ratio),float32.length); let sum=0; for(let j=start;j<end;j++) sum+=float32[j]; out[i]=sum/Math.max(1,end-start); }
        return out;
      }
      function pcm16(float32) {
        const out = new Int16Array(float32.length);
        for(let i=0;i<float32.length;i++){const x=Math.max(-1,Math.min(1,float32[i]));out[i]=x<0?x*32768:x*32767;}
        return new Uint8Array(out.buffer);
      }
      function stopPlayback() { if (playCtx) { try { playCtx.close(); } catch(e){} } playCtx=null; nextPlayTime=0; }
      function playPcm(base64) {
        const bytes=fromB64(base64); const pcm=new Int16Array(bytes.buffer,bytes.byteOffset,Math.floor(bytes.byteLength/2));
        if(!playCtx || playCtx.state==='closed') { playCtx=new AudioContext({sampleRate:24000}); nextPlayTime=playCtx.currentTime; }
        const buffer=playCtx.createBuffer(1,pcm.length,24000); const channel=buffer.getChannelData(0);
        for(let i=0;i<pcm.length;i++) channel[i]=pcm[i]/32768;
        const src=playCtx.createBufferSource(); src.buffer=buffer; src.connect(playCtx.destination);
        const when=Math.max(playCtx.currentTime+0.02,nextPlayTime); src.start(when); nextPlayTime=when+buffer.duration;
      }
      function cleanup() {
        active=false; setupReady=false;
        try { if(processor) processor.disconnect(); } catch(e){} processor=null;
        try { if(source) source.disconnect(); } catch(e){} source=null;
        try { if(micStream) micStream.getTracks().forEach(t=>t.stop()); } catch(e){} micStream=null;
        try { if(micCtx) micCtx.close(); } catch(e){} micCtx=null;
        try { if(ws && ws.readyState<2) ws.close(); } catch(e){} ws=null;
        stopPlayback(); startBtn.disabled=false; stopBtn.disabled=true;
      }
      function sendAudio(float32) {
        if(!active || !setupReady || !ws || ws.readyState!==WebSocket.OPEN) return;
        const sampled=downsampleTo16k(float32,micCtx.sampleRate);
        const bytes=pcm16(sampled);
        ws.send(JSON.stringify({realtimeInput:{mediaChunks:[{mimeType:'audio/pcm;rate=16000',data:b64(bytes)}]}}));
      }
      startBtn.addEventListener('click', async () => {
        if(active) return;
        startBtn.disabled=true; setStatus('Button clicked — checking microphone support…');
        try {
          if (!window.isSecureContext) throw new Error('Microphone requires HTTPS or localhost. Open BuddhiX on localhost/HTTPS.');
          if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) throw new Error('This browser frame cannot access the microphone. Try Chrome on localhost/HTTPS.');
          setStatus('Requesting microphone permission…');
          micStream=await navigator.mediaDevices.getUserMedia({audio:{channelCount:1,echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
          micCtx=new AudioContext(); await micCtx.resume(); source=micCtx.createMediaStreamSource(micStream);
          processor=micCtx.createScriptProcessor(4096,1,1);
          processor.onaudioprocess=(e)=>{if(active && setupReady) sendAudio(e.inputBuffer.getChannelData(0));};
          source.connect(processor); processor.connect(micCtx.destination);
          const endpoint='wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContentConstrained?access_token='+encodeURIComponent(token);
          ws=new WebSocket(endpoint); active=true; stopBtn.disabled=false;
          ws.onopen=()=>{
            setStatus('Connecting to Gemini Live…');
            const setupMessage = {
              setup: {
                model: 'models/' + model,
                generationConfig: {
                  responseModalities: ['AUDIO'],
                  speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Aoede' } } }
                },
                inputAudioTranscription: {},
                outputAudioTranscription: {},
                systemInstruction: { parts: [{ text: 'You are BuddhiX, a friendly student learning tutor. Speak naturally in simple Hinglish by default, unless the student speaks another language. Explain clearly, keep spoken answers reasonably concise, ask helpful follow-up questions, and allow interruptions. For study questions, teach step by step and never invent facts.' }] }
              }
            };
            ws.send(JSON.stringify(setupMessage));
          };
          ws.onmessage=(event)=>{
            let msg; try{msg=JSON.parse(event.data);}catch(e){return;}
            if(msg.setupComplete){setupReady=true;setStatus('Live — speak now');}
            if(msg.serverContent){
              if(msg.serverContent.interrupted){stopPlayback();setStatus('You interrupted — listening…');}
              const inputText=msg.serverContent.inputTranscription?.text;
              if(inputText){userLine+=inputText;}
              const outputText=msg.serverContent.outputTranscription?.text;
              if(outputText){assistantLine+=outputText;}
              if(msg.serverContent.turnComplete){if(userLine.trim())addLine('You',userLine.trim());if(assistantLine.trim())addLine('BuddhiX',assistantLine.trim());userLine='';assistantLine='';setStatus('Live — speak now');}
              const parts=msg.serverContent.modelTurn?.parts||[];
              for(const part of parts){const d=part.inlineData||part.inline_data;if(d && d.data && (d.mimeType||d.mime_type||'').includes('audio'))playPcm(d.data);}
            }
            if(msg.error){setStatus('Live API error: '+(msg.error.message||'request failed'));cleanup();}
          };
          ws.onerror=()=>{setStatus('WebSocket connection error. Check network, Live API access and model availability.');};
          ws.onclose=(ev)=>{if(active){const reason=(ev.reason||'no server reason supplied');setStatus('Session closed ('+ev.code+'): '+reason+'. Click Prepare Live Voice Session again before reconnecting.');cleanup();}};
        } catch(err) {setStatus('Could not start: '+(err.message||String(err)));cleanup();}
      });
      stopBtn.addEventListener('click', () => {setStatus('Session ended');cleanup();});
      window.addEventListener('beforeunload',cleanup);
    })();
    </script>'''
    html = html.replace('TOKEN_PLACEHOLDER', safe_token).replace('MODEL_PLACEHOLDER', safe_model)
    components.html(html, height=300, scrolling=False)


def transcribe_voice_audio(audio_file):
    """Transcribe a Streamlit-recorded audio file using optional Groq Whisper API."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return None, "Voice transcription needs a GROQ_API_KEY. Add it to your private .env file; your existing ASI/OpenRouter key is not used for this endpoint."
    try:
        audio_file.seek(0)
        response = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (getattr(audio_file, "name", "voice_input.wav"), audio_file.getvalue(), getattr(audio_file, "type", None) or "audio/wav")},
            data={"model": "whisper-large-v3-turbo", "response_format": "json"},
            timeout=90,
        )
        if response.status_code >= 400:
            return None, f"Speech-to-text request failed ({response.status_code}). Check the Groq key, quota, and network. {response.text[:300]}"
        transcript = str(response.json().get("text", "")).strip()
        if not transcript:
            return None, "No speech was detected. Try recording again in a quiet place."
        return transcript, None
    except requests.RequestException as exc:
        return None, f"Could not reach the speech-to-text service: {str(exc)[:220]}"
    except Exception as exc:
        return None, f"Could not process this recording: {str(exc)[:220]}"


def speech_friendly_text(value):
    # Clean Markdown/math formatting before passing the answer to browser speech.
    text = str(value or "")
    text = re.sub(r"```[^\n]*\n.*?```", " Code example shown on screen. ", text, flags=re.S)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", text)
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?m)^\s*>\s?", "", text)
    text = re.sub(r"(?m)^\s*[-+*]\s+", "", text)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text, flags=re.S)
    text = re.sub(r"(?<!\*)\*(?!\s)(.*?)(?<!\s)\*(?!\*)", r"\1", text, flags=re.S)
    text = re.sub(r"(?<!_)_(?!\s)(.*?)(?<!\s)_(?!_)", r"\1", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\$\$?", " ", text)
    text = re.sub(r"\\\\[()\[\]]", " ", text)
    text = re.sub(r"\\(?:text|mathrm|mathbf|mathit|operatorname)\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1 divided by \2", text)
    text = re.sub(r"\\sqrt\s*\{([^{}]*)\}", r"square root of \1", text)
    for pattern, phrase in [(r"\\times\b", " times "), (r"\\cdot\b", " times "), (r"\\rightarrow\b|\\\\to\b", " leads to "), (r"\\leq\b", " is less than or equal to "), (r"\\geq\b", " is greater than or equal to "), (r"\\neq\b", " is not equal to "), (r"\\approx\b", " approximately ")]:
        text = re.sub(pattern, phrase, text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = re.sub(r"[{}\\$]", " ", text)
    text = re.sub(r"[*_~#`|<>]", " ", text)
    text = re.sub(r"\s*([=+])\s*", r" \1 ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", ". ", text)
    text = re.sub(r"(?:\.\s*){2,}", ". ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,;:])(?=\S)", r"\1 ", text)
    return text.strip()


def render_speech_button(text_to_speak, key="voice_reply"):
    # Speak cleaned text; the displayed AI answer remains unchanged.
    speech_text = speech_friendly_text(str(text_to_speak)[:12000])
    safe_text = json.dumps(speech_text, ensure_ascii=False)
    html = f'''<div style="font-family:system-ui;background:#101a30;border:1px solid #344873;border-radius:12px;padding:10px;color:#eef4ff">
    <button id="speak" style="background:#6757f5;color:white;border:0;border-radius:9px;padding:8px 13px;cursor:pointer;font-weight:600">🔊 Read answer aloud</button>
    <button id="stop" style="background:#263858;color:white;border:0;border-radius:9px;padding:8px 13px;margin-left:6px;cursor:pointer">⏹ Stop</button>
    <span id="status" style="font-size:12px;margin-left:8px;color:#c4d0ef"></span></div>
    <script>
    const text = {safe_text};
    const status = document.getElementById('status');
    document.getElementById('speak').onclick = () => {{
      if (!('speechSynthesis' in window)) {{ status.textContent='Speech synthesis is not supported in this browser.'; return; }}
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-IN';
      u.rate = 0.96;
      u.onstart = () => status.textContent = 'Speaking…';
      u.onend = () => status.textContent = 'Finished';
      u.onerror = () => status.textContent = 'Audio playback failed';
      window.speechSynthesis.speak(u);
    }};
    document.getElementById('stop').onclick = () => {{ window.speechSynthesis.cancel(); status.textContent = 'Stopped'; }};
    </script>'''
    components.html(html, height=70, scrolling=False)


def parse_json(s):
    """Parse JSON returned by chat models, including fenced or prefaced JSON."""
    if not isinstance(s, str):
        raise ValueError("Model response was not text.")
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.I)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Find the first valid JSON object/array without a greedy regex swallowing prose.
        decoder = json.JSONDecoder()
        for i, ch in enumerate(cleaned):
            if ch in "{[":
                try:
                    obj, _ = decoder.raw_decode(cleaned[i:])
                    return obj
                except json.JSONDecodeError:
                    continue
    raise ValueError("No valid JSON found in model response.")


def quiz_make(topic, diff, n):
    """Generate a compact quiz quickly; only retry malformed model output, not API failures."""
    language = st.session_state.get("response_language", "Hinglish")
    prompt = (
        f"Create exactly {n} multiple-choice questions about: {topic}. Difficulty: {diff}. "
        f"Write in {language}. Return ONLY strict JSON using this schema: "
        '{"questions":[{"question":"...","options":{"A":"...","B":"...","C":"...","D":"..."},'
        '"answer":"A","explanation":"one short sentence","concept":"short tag"}]}. '
        f"Exactly {n} questions. Each question should be concise; options should be short; explanation must be one sentence. "
        "Exactly one option is correct. No Markdown, no introduction, no extra fields."
    )
    last_error = "Quiz generation failed. Please try again."
    # Keep output budget proportional to the quiz size instead of forcing 3,500 tokens for every request.
    token_budget = max(1100, n * 230)
    for attempt in range(2):
        messages = [
            {"role": "system", "content": "Create accurate educational MCQs. Output strict valid JSON only. Keep every field concise."},
            {"role": "user", "content": prompt if attempt == 0 else prompt + " Return corrected strict JSON only; previous output was invalid."}
        ]
        out, err = call(messages, .1, token_budget)
        if err:
            # An API/network failure won't be fixed by immediately sending the same request again.
            return None, err
        try:
            parsed = parse_json(out)
            qs = parsed.get("questions") if isinstance(parsed, dict) else None
            valid = isinstance(qs, list) and len(qs) == n
            if valid:
                for q in qs:
                    if not isinstance(q, dict) or not isinstance(q.get("question"), str) or not q["question"].strip():
                        valid = False; break
                    opts = q.get("options")
                    if not isinstance(opts, dict) or any(k not in opts or not str(opts[k]).strip() for k in "ABCD"):
                        valid = False; break
                    if q.get("answer") not in ("A", "B", "C", "D"):
                        valid = False; break
                    q.setdefault("explanation", "Review the correct option and underlying concept.")
                    q.setdefault("concept", topic)
            if valid:
                return qs, None
            last_error = f"The AI returned an incomplete quiz (expected {n} valid questions). Try 5 questions or a more specific topic."
        except Exception:
            last_error = "The AI returned an unreadable quiz format. Please try again or choose a more specific topic."
    return None, last_error


def pdf_text(f):
    """Extract selectable text while preserving page numbers for source references."""
    try:
        from pypdf import PdfReader
        pages = []
        for page_no, page in enumerate(PdfReader(f).pages, start=1):
            content = (page.extract_text() or "").strip()
            if content:
                pages.append(f"[PDF page {page_no}]\n{content}")
        return "\n\n".join(pages)[:30000]
    except Exception as e:
        return "[PDF extraction error: " + str(e) + "]"
# First-run name setup, stored locally in SQLite.
if "user_name" not in st.session_state:
    row = con.execute("SELECT name FROM profile WHERE id=1").fetchone()
    st.session_state.user_name = row[0] if row and row[0] else ""
if not st.session_state.user_name:
    st.markdown('<div class="hero"><h1>Welcome to BuddhiX 👋</h1><p>Your AI study companion. Let’s personalise your workspace.</p></div>', unsafe_allow_html=True)
    with st.form("welcome_name_form"):
        new_name = st.text_input("What should we call you?", placeholder="Enter your name")
        submitted_name = st.form_submit_button("Continue →", use_container_width=True)
    if submitted_name:
        if not new_name.strip(): st.warning("Please enter your name first.")
        else:
            st.session_state.user_name = new_name.strip()[:50]
            con.execute("INSERT INTO profile(id,name) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name", (st.session_state.user_name,))
            con.commit(); st.rerun()
    st.stop()

if "chat" not in st.session_state:st.session_state.chat=[]
if "quiz" not in st.session_state:st.session_state.quiz=None
if "submitted" not in st.session_state:st.session_state.submitted=False
if "notes" not in st.session_state:st.session_state.notes=""
if "pending_prompt" not in st.session_state:st.session_state.pending_prompt=None
if "use_pdf_context" not in st.session_state: st.session_state.use_pdf_context = False
if "response_depth" not in st.session_state: st.session_state.response_depth = "Detailed"
if "pending_mode" in st.session_state:
 st.session_state.visible_tutor_mode=st.session_state.pop("pending_mode")
NAV_ITEMS=["Home","Chat & Learn","Learning Kit","Practice","Study Battle","My Progress","Study Planner","Notes","Settings","Agent Blueprint"]
if st.session_state.get("pending_nav") in NAV_ITEMS:
 st.session_state["workspace_nav"]=st.session_state.pop("pending_nav")
elif st.session_state.get("workspace_nav") not in NAV_ITEMS:
 st.session_state["workspace_nav"]="Home"
NAV_ICONS={"Home":"⌂","Chat & Learn":"◉","Learning Kit":"▤","Practice":"✎","Study Battle":"⚔","My Progress":"▥","Study Planner":"▦","Notes":"▧","Settings":"⚙","Agent Blueprint":"⌘"}
NAV_TO_PAGE={"Home":"Home","Chat & Learn":"AI Tutor","Learning Kit":"Learning Kit","Practice":"Test Mode","Study Battle":"Battle Field","My Progress":"My Progress","Study Planner":"Study Planner","Notes":"Learning Kit","Settings":"Settings","Agent Blueprint":"Agent Blueprint"}
with st.sidebar:
 st.markdown("<div style='display:flex;align-items:center;gap:9px;margin:2px 0 20px'><span style='font-size:28px'>🧠</span><span style='font-size:23px;font-weight:850;letter-spacing:-.5px;color:#edf5ff'>Buddhi<span style='color:#4da6ff'>X</span></span></div>",unsafe_allow_html=True)
 st.caption("YOUR PERSONAL AI STUDY SPACE")
 st.markdown("<div style='padding:12px 13px;margin:10px 0 16px;border:1px solid #2e4265;border-radius:14px;background:linear-gradient(120deg,#142847,#101a2e)'><div style='font-size:11px;color:#77c8ff;letter-spacing:.08em;font-weight:700'>LEARN • PRACTISE • IMPROVE</div><div style='font-size:12px;color:#c8d7f4;margin-top:6px'>One workspace for your study journey.</div></div>",unsafe_allow_html=True)
 nav_label=st.radio("WORKSPACE",NAV_ITEMS,index=NAV_ITEMS.index(st.session_state.get("workspace_nav","Home")) if st.session_state.get("workspace_nav","Home") in NAV_ITEMS else 0,key="workspace_nav",format_func=lambda x:f"{NAV_ICONS[x]}   {x}",label_visibility="collapsed")
 page=NAV_TO_PAGE[nav_label]
 st.markdown("---")
 st.markdown("#### 🌐 Response language")
 st.selectbox("Choose language", ["Hinglish", "Hindi", "English"], key="response_language", label_visibility="collapsed", help="AI explanations, learning kits and study plans will follow this language.")
 st.caption("You can change this anytime.")
 st.markdown("<div style='padding:12px;margin-top:18px;border:1px solid #293d62;border-radius:14px;background:#0e192c'><b style='color:#e9f1ff'>✨ Unlock more</b><p style='font-size:11px;color:#9eb4d8'>More tools and a personalised learning journey.</p></div>",unsafe_allow_html=True)

# Page transition: change the animation name on every navigation rerun so the
# browser restarts the animation even though Streamlit reuses its main container.
_page_slug = re.sub(r"[^a-zA-Z0-9]", "", str(nav_label)) or "workspace"
st.markdown(f"""
<style>
@keyframes buddhixPageEnter_{_page_slug} {{
  0% {{ opacity: 0.12; transform: translateY(14px) scale(0.995); filter: blur(2px); }}
  65% {{ opacity: 1; filter: blur(0); }}
  100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
}}
@keyframes buddhixProgress_{_page_slug} {{
  0% {{ transform: scaleX(0); opacity: 1; }}
  75% {{ transform: scaleX(.88); opacity: .95; }}
  100% {{ transform: scaleX(1); opacity: 0; }}
}}
[data-testid="stMain"] .block-container {{
  animation: buddhixPageEnter_{_page_slug} .62s cubic-bezier(.2,.75,.25,1) both !important;
}}
[data-testid="stMain"] .block-container::before {{
  content: ""; position: fixed; z-index: 999999; top: 0; left: 0;
  width: 100%; height: 3px; transform-origin: left center;
  background: linear-gradient(90deg,#36b8ff,#6b63ff,#b16bff);
  pointer-events: none; animation: buddhixProgress_{_page_slug} .72s ease-out both;
}}
@media (prefers-reduced-motion: reduce) {{
  [data-testid="stMain"] .block-container {{ animation: none !important; }}
  [data-testid="stMain"] .block-container::before {{ animation: none !important; }}
}}
</style>
""", unsafe_allow_html=True)

if page=="Home":
 st.markdown(f'<div class="dash-hero"><span class="dash-kicker">✦ AI-POWERED LEARNING PLATFORM</span><h1>BuddhiX</h1><h3>Your AI Learning Assistant</h3><p>Hey {st.session_state.user_name}, learn smarter. Solve doubts faster. Build better habits.</p></div>',unsafe_allow_html=True)
 hero_a,hero_b=st.columns([1,1])
 with hero_a:
  if st.button("🚀  Start Learning",key="home_start",use_container_width=True): st.session_state.pending_nav="Chat & Learn"; st.rerun()
 with hero_b:
  if st.button("✦  Explore Features",key="home_explore",use_container_width=True): st.session_state.pending_nav="Learning Kit"; st.rerun()
 st.markdown("<div class='dash-section'>Your learning tools</div>",unsafe_allow_html=True)
 feature_data=[("📖","AI Tutor","Ask anything and learn step by step.","Chat & Learn"),("💡","Doubt Solver","Get instant concept clarity.","Chat & Learn"),("📝","Practice","Generate questions and quizzes.","Practice"),("🎯","Study Coach","Plan, track and stay consistent.","Study Planner")]
 fc=st.columns(4)
 for col,(ico,title,desc,dest) in zip(fc,feature_data):
  with col:
   st.markdown(f"<div class='dash-card'><span class='dash-icon'>{ico}</span><h4>{title}</h4><p>{desc}</p></div>",unsafe_allow_html=True)
   if st.button("Open →",key="home_feature_"+title,use_container_width=True): st.session_state.pending_nav=dest; st.rerun()
 left,right=st.columns([1.35,1])
 with left:
  st.markdown("<div class='dash-panel'><div class='dash-section'>📚 My Subjects</div>",unsafe_allow_html=True)
  subjects=[("Network Analysis & Synthesis","Notes · PYQs · Topics"),("Electronic Devices","Notes · PYQs · Examples"),("DBMS","Notes · PYQs · Queries"),("Python Programming","Notes · Examples · Code"),("Technical Communication","Notes · Resources · Tips")]
  subcols=st.columns(3)
  for i,(sub,details) in enumerate(subjects):
   with subcols[i%3]: st.markdown(f"<div class='subject-pill'><b>{sub}</b><br><small>{details}</small></div>",unsafe_allow_html=True)
  st.markdown("</div>",unsafe_allow_html=True)
 with right:
  st.markdown("<div class='dash-panel'><div class='dash-section'>⚡ Quick Resources</div>",unsafe_allow_html=True)
  resources=[("📤","Upload Notes","Add your own PDF"),("📑","Syllabus","Unit-wise topics"),("🧾","PYQs","Previous year questions"),("⭐","Bookmarks","Saved content")]
  rcols=st.columns(2)
  for i,(ico,title,desc) in enumerate(resources):
   with rcols[i%2]: st.markdown(f"<div class='dash-quick'>{ico} <b>{title}</b><br><small>{desc}</small></div>",unsafe_allow_html=True)
  if st.button("Open Learning Kit →",key="home_resources",use_container_width=True): st.session_state.pending_nav="Learning Kit"; st.rerun()
  st.markdown("</div>",unsafe_allow_html=True)
 pcol,activity=st.columns([1.4,1])
 rows=con.execute("SELECT score,total,topic,created FROM attempts ORDER BY id DESC LIMIT 30").fetchall()
 attempts=len(rows); avg=round(sum((r[0]/r[1]*100) for r in rows if r[1]) / max(1,sum(1 for r in rows if r[1]))) if rows else 0
 with pcol:
  st.markdown("<div class='dash-panel'><div class='dash-section'>📈 My Progress</div>",unsafe_allow_html=True)
  m1,m2,m3=st.columns(3);m1.metric("Quizzes attempted",attempts);m2.metric("Average score",f"{avg}%" if rows else "—");m3.metric("Subjects",5)
  st.caption("Progress is calculated from your locally saved quiz attempts; no demo scores are added.")
  if st.button("View full progress →",key="home_progress",use_container_width=True): st.session_state.pending_nav="My Progress"; st.rerun()
  st.markdown("</div>",unsafe_allow_html=True)
 with activity:
  st.markdown("<div class='dash-panel'><div class='dash-section'>🕒 Recent Activity</div>",unsafe_allow_html=True)
  if rows:
   for score,total,topic,created in rows[:4]: st.markdown(f"<div class='dash-quick'><b>{topic}</b><br><small>Score: {score}/{total} · {created}</small></div>",unsafe_allow_html=True)
  else: st.caption("Your quiz attempts will appear here after you practise.")
  st.markdown("</div>",unsafe_allow_html=True)
elif page=="Settings":
 st.markdown('<div class="hero"><h1>⚙️ Settings</h1><p>Manage your BuddhiX learning preferences.</p></div>',unsafe_allow_html=True)
 st.markdown("### Profile")
 st.write(f"Current profile name: **{st.session_state.user_name}**")
 with st.form("profile_edit"):
  edited_name=st.text_input("Display name",value=st.session_state.user_name)
  save_profile=st.form_submit_button("Save profile")
 if save_profile and edited_name.strip():
  st.session_state.user_name=edited_name.strip()[:50]
  con.execute("INSERT INTO profile(id,name) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name",(st.session_state.user_name,));con.commit();st.success("Profile updated.")
 st.markdown("### API connection")
 if cfg()["key"]: st.success("API key detected in your local environment.")
 else: st.warning("API key not found. Add ASI_ONE_API_KEY to your private .env file and restart Streamlit.")
 st.info("Keep your .env private. Never paste your API key into screenshots, chat, or source code.")
elif page=="AI Tutor":
 st.markdown(f'<div class="hero"><h1>Good to see you, {st.session_state.user_name}! 👋</h1><p>Your AI learning workspace — ask, diagnose, practise and improve.</p></div>',unsafe_allow_html=True)
 if "notes_name" not in st.session_state: st.session_state.notes_name="uploaded PDF"
 if "quick_action" not in st.session_state: st.session_state.quick_action=None
 # Chat workspace + right-side learning tools.
 chat_col, tools_col = st.columns([3.65, 1.05], gap="medium")
 mode_options = ["Smart Tutor","Deep Learning","Smart Doubt Solver","Exam Prep","Practice Coach","Notes Q&A","Study Coach","Analysis Mode"]
 mode_icons = {"Smart Tutor":"💬","Deep Learning":"🧠","Smart Doubt Solver":"🧩","Exam Prep":"🎯","Practice Coach":"✍️","Notes Q&A":"📄","Study Coach":"🗓️","Analysis Mode":"🔎"}
 mode_desc = {"Smart Tutor":"Everyday doubts and guided learning","Deep Learning":"Build concepts from basics to advanced","Smart Doubt Solver":"Check your attempt and find the first mistake","Exam Prep":"Structured, exam-ready explanations","Practice Coach":"One question at a time with feedback","Notes Q&A":"Answer using your uploaded notes","Study Coach":"Priorities, goals and realistic plans","Analysis Mode":"Organised problem-solving steps"}
 with chat_col:
  if st.session_state.get("pending_mode"):
   st.session_state["visible_tutor_mode"] = st.session_state.pop("pending_mode")
  st.markdown('<div class="agent-strip"><span class="agent-dot"></span><b>Learning agent ready</b><span>·</span><span>Context-aware tutoring</span><span>·</span><span>Local progress memory</span></div>',unsafe_allow_html=True)
  mode=st.selectbox("🎛️ Choose learning mode", mode_options, format_func=lambda x: f"{mode_icons[x]}  {x}", key="visible_tutor_mode")
  st.caption(f"**{mode}** · {mode_desc[mode]}")
  depth=st.selectbox("Answer detail",["Quick","Detailed","Exam-ready"],key="response_depth",label_visibility="collapsed")
  st.caption("Answer detail")
  if st.button("🧹 Clear conversation",key="clear_chat",use_container_width=False):
   st.session_state.chat=[]; st.session_state.quick_action=None; st.session_state.pending_prompt=None; st.rerun()
  for m in st.session_state.chat:
   with st.chat_message(m["role"]): st.markdown(format_math(m["content"]))
  pdf_available=bool(st.session_state.notes.strip())
  st.toggle("📎 Answer using my uploaded PDF",key="use_pdf_context",disabled=not pdf_available,help="When enabled, BuddhiX uses your uploaded notes as the primary source.")
  if pdf_available: st.caption(f"Source ready: {st.session_state.get('notes_name','uploaded PDF')}")
  else: st.caption("PDF source off · Upload notes from Learning tools on the right.")
  st.markdown("#### 🎙️ Voice Tutor")
  st.caption("Real-time voice conversation (Gemini Live) — speak naturally and interrupt the tutor anytime.")
  if "gemini_live_session" not in st.session_state:
   st.session_state.gemini_live_session = None
  if st.button("✨ Prepare Live Voice Session", key="prepare_gemini_live", use_container_width=True):
   with st.spinner("Preparing a secure temporary Gemini Live session…"):
    live_data, live_error = create_gemini_live_token()
   if live_error:
    st.error(live_error)
    if not os.getenv("GEMINI_API_KEY", "").strip():
     st.code("GEMINI_API_KEY=your_key_here", language="bash")
     st.caption("Add this to your private .env file, then restart Streamlit. Never paste the key into chat or screenshots.")
    st.session_state.gemini_live_session = None
   else:
    st.session_state.gemini_live_session = live_data
  if st.session_state.get("gemini_live_session"):
   live = st.session_state.gemini_live_session
   render_gemini_live(live["token"], live["model"])
   st.caption("If the session token expires or you end the session, prepare a new one. Browser microphone access is required.")
  with st.expander("Legacy record-and-transcribe mode", expanded=False):
    voice_audio=st.audio_input("Record your doubt",key="voice_input_audio")
  vcol1, vcol2 = st.columns([1, 2])
  with vcol1:
   transcribe_clicked=st.button("📝 Transcribe voice",key="transcribe_voice",use_container_width=True,disabled=voice_audio is None)
  with vcol2:
   st.caption("Speak clearly, then transcribe. Speech-to-text needs an optional Groq API key; answers can be read aloud in your browser.")
  if transcribe_clicked and voice_audio is not None:
   with st.spinner("Transcribing your recording…"):
    transcript, transcript_error = transcribe_voice_audio(voice_audio)
   if transcript_error:
    st.error(transcript_error)
    if not os.getenv("GROQ_API_KEY", "").strip():
     st.code("GROQ_API_KEY=your_groq_key_here", language="bash")
     st.caption("Add this line to your private .env file, then restart Streamlit. Get a key from the Groq Console. Never paste the key into chat or screenshots.")
   else:
    st.session_state["voice_transcript_draft"] = transcript
    st.success("Voice transcribed. Review the text below, then send it to BuddhiX.")
  if st.session_state.get("voice_transcript_draft") is not None:
   with st.form("voice_transcript_review"):
    reviewed_transcript=st.text_area("Review / edit transcript",value=st.session_state.get("voice_transcript_draft", ""),height=90)
    send_voice=st.form_submit_button("Send voice question to BuddhiX",use_container_width=True)
   if send_voice and reviewed_transcript.strip():
    st.session_state.pending_prompt=reviewed_transcript.strip()
    st.session_state.voice_transcript_draft=None
    st.rerun()
  typed_q=st.chat_input("Message BuddhiX…")
 with tools_col:
  st.markdown("### 🧰 Tools")
  st.caption("Focused actions · less clutter")
  with st.container(border=True):
   st.markdown("**📄 PDF Notes**")
   f=st.file_uploader("Upload PDF",type=["pdf"],key="pdf_notes_upload",label_visibility="collapsed",help="Selectable-text PDFs supported; scanned PDFs need OCR.")
   if f:
    t=pdf_text(f)
    if t.startswith("[PDF extraction error"): st.error(t)
    elif not t.strip(): st.warning("No selectable text found; scanned-PDF OCR is not included.")
    else:
     st.session_state.notes=t; st.session_state.notes_name=f.name
     st.success(f"Ready · {f.name}")
   elif st.session_state.notes.strip(): st.caption(f"Loaded · {st.session_state.get('notes_name','uploaded PDF')}")
  with st.container(border=True):
   st.markdown("**⚡ Quick action**")
   action_choice=st.selectbox("Choose an action",["Check my work","Explain a topic","Practice a topic"],key="right_quick_action",label_visibility="collapsed")
   if st.button("Open action →",key="right_open_action",use_container_width=True):
    st.session_state.quick_action={"Check my work":"doubt","Explain a topic":"explain","Practice a topic":"practice"}[action_choice]
  with st.expander("🎯 Today's goals",expanded=False):
   today=datetime.now().date().isoformat()
   goal_rows=con.execute("SELECT id,goal,done FROM goals WHERE day=? ORDER BY id",(today,)).fetchall()
   with st.form("daily_goal_add"):
    new_goal=st.text_input("Add a goal",placeholder="Revise RC circuits",label_visibility="collapsed")
    add_goal=st.form_submit_button("+ Add",use_container_width=True)
   if add_goal and new_goal.strip():
    con.execute("INSERT INTO goals(goal,done,day) VALUES(?,0,?)",(new_goal.strip(),today)); con.commit(); st.rerun()
   if goal_rows:
    for gid,gtext,gdone in goal_rows:
     checked=st.checkbox(gtext,key=f"goal_{gid}",value=bool(gdone))
     if checked != bool(gdone):
      con.execute("UPDATE goals SET done=? WHERE id=?",(int(checked),gid)); con.commit(); st.rerun()
    done_count=sum(int(x[2]) for x in goal_rows); st.progress(done_count/len(goal_rows),text=f"{done_count}/{len(goal_rows)} done")
   else: st.caption("Add one small goal for today.")
  with st.expander("🗂️ More workspace",expanded=False):
   if st.button("🗓️ Study Planner",key="right_study_planner",use_container_width=True,on_click=lambda: st.session_state.update({"workspace_nav":"Study Planner"})): pass
   if st.button("📈 My Progress",key="right_progress",use_container_width=True,on_click=lambda: st.session_state.update({"workspace_nav":"My Progress"})): pass
 # Quick task forms are shown in the tools column's workflow area after selecting a tool.
 quick_prompts={
  "explain": ("Explain a concept", "What concept do you want to understand?", "Teach me {topic} step by step. Start with intuition, then definition, explain each step, show a worked example, common mistakes, and finish with a short check question."),
  "practice": ("Practice questions", "Which topic should we practice?", "Act as an adaptive practice tutor for {topic}. Ask ONE question and wait. After I answer, mark it, explain the reasoning, diagnose the misconception if wrong, then ask a similar question at a suitable difficulty."),
  "pdf": ("Study from my PDF", "What topic or chapter from your uploaded PDF?", "Use my uploaded PDF notes as the primary source and help me study {topic}. Mention relevant PDF page numbers when available. Separate what the PDF says from extra explanation; if the notes do not support a claim, say so.")
 }
 if st.session_state.quick_action in quick_prompts or st.session_state.quick_action=="doubt":
  action=st.session_state.quick_action
  action_title="Smart Doubt Solver" if action=="doubt" else quick_prompts[action][0]
  with st.container(border=True):
   st.markdown(f"#### {action_title}")
   if action=="pdf" and not st.session_state.notes.strip(): st.info("Upload a PDF in Learning tools first.")
   with st.form("quick_start_topic_form"):
    if action=="doubt":
     st.caption("Share the original question and your attempt. You can also attach a clear image of a handwritten solution or question.")
     problem_for_doubt=st.text_area("Question / problem",placeholder="Paste the original question here…",height=100)
     attempt_for_doubt=st.text_area("Your attempted answer",placeholder="Show your steps or explain what you tried…",height=130)
     doubt_image=st.file_uploader("Optional image of question / working",type=["png","jpg","jpeg","webp"],key="smart_doubt_image",help="Image understanding depends on whether your configured AI model supports vision input.")
    else:
     _,topic_label,_=quick_prompts[action]
     topic_for_quick=st.text_input(topic_label,placeholder="e.g. Laplace transform / DBMS normalization / RC circuit")
    qa,qb=st.columns(2)
    with qa: quick_send=st.form_submit_button("Check my work" if action=="doubt" else "Continue",use_container_width=True)
    with qb: quick_cancel=st.form_submit_button("Cancel",use_container_width=True)
   if quick_cancel: st.session_state.quick_action=None; st.rerun()
   if quick_send:
    if action=="doubt":
     if not problem_for_doubt.strip() and not doubt_image: st.warning("Enter the question as text or attach an image of it.")
     elif not attempt_for_doubt.strip() and not doubt_image: st.warning("Enter your attempted answer, or attach an image that clearly shows your working.")
     else:
      doubt_prompt=("Act as BuddhiX Smart Doubt Solver. Give a detailed report using these exact sections: 1) Verdict (correct / partially correct / incorrect / insufficient information), 2) First incorrect step (quote the student's step; if none, say no error found), 3) Error type (conceptual / calculation / syntax / logic / reading error / none / uncertain), 4) Why it happened, 5) Corrected step, 6) Complete step-by-step solution, 7) Verification of the final answer, 8) One similar practice question WITHOUT its answer. Preserve all correct parts of the student's work. Never invent an error or unreadable image text. If the image is unclear, state what cannot be read and ask for a clearer image. Distinguish what is directly visible in the submission from any assumptions.\n\nQUESTION (if typed):\n"+ (problem_for_doubt.strip() or "See attached image; transcribe the question faithfully first.") + "\n\nSTUDENT ATTEMPT (if typed):\n" + (attempt_for_doubt.strip() or "See attached image; inspect the working carefully."))
      st.session_state.pending_prompt=doubt_prompt
      if doubt_image:
       mime=doubt_image.type or "image/png"
       encoded=base64.b64encode(doubt_image.getvalue()).decode("ascii")
       st.session_state.pending_doubt_image={"data_url":f"data:{mime};base64,{encoded}","name":doubt_image.name,"mime":mime}
      else:
       st.session_state.pending_doubt_image=None
      st.session_state.quick_action=None; st.session_state.pending_mode="Smart Doubt Solver"; st.rerun()
    elif not topic_for_quick.strip(): st.warning("Please enter a topic first.")
    elif action=="pdf" and not st.session_state.notes.strip(): st.warning("Upload a PDF first, then continue.")
    else:
     st.session_state.pending_prompt=quick_prompts[action][2].format(topic=topic_for_quick.strip())
     if action=="pdf": st.session_state.use_pdf_context=True
     st.session_state.quick_action=None; st.rerun()
 # Process typed chat or a submitted quick task.
 q=typed_q or st.session_state.get("pending_prompt")
 if q:
  st.session_state.pending_prompt=None
  st.session_state.chat.append({"role":"user","content":q})
  depth=st.session_state.get("response_depth","Detailed")
  depth_rules={"Quick":"Keep the answer concise: direct answer, essential reasoning, and formula if relevant.","Detailed":"Give a thorough but readable explanation: intuition, definition, step-by-step reasoning, worked example, key formulas with symbols defined, common mistakes, and a short recap. Adapt sections to the question; do not pad irrelevant sections.","Exam-ready":"Give a detailed explanation followed by an exam-ready answer, key points, labelled formula/derivation steps, and 2 practice questions. Do not claim these are exact past-paper questions unless verified."}
  mode_prompts={
   "Smart Tutor":"Teach in small steps and check understanding with a short question when useful.",
   "Deep Learning":"Act as a patient expert tutor. Teach from beginner to advanced in layers: intuition, prerequisites, precise definition, why/how it works, step-by-step derivation, worked example, common misconceptions, recap, and one check-for-understanding question. Do not skip algebra steps in engineering numericals.",
   "Smart Doubt Solver":"Return a detailed report with these sections: Verdict; First incorrect step; Error type; Why it happened; Corrected step; Complete step-by-step solution; Verification; One similar practice question without its answer. Preserve correct work, never invent an error, and clearly state when information or image text is uncertain.",
   "Exam Prep":"Prioritize syllabus-friendly definitions, derivations, labelled steps, exam-ready structure and likely practice questions. Never claim unverified questions are actual PYQs.",
   "Practice Coach":"Ask one question at a time, wait for the student's answer, evaluate it, explain mistakes without shaming, and adjust difficulty.",
   "Notes Q&A":"Use uploaded notes as primary source. If absent or unsupported, say so. Mention PDF page labels when available and distinguish source content from extra explanation.",
   "Study Coach":"Give realistic priorities, short study blocks, one next action and a quick way to measure completion.",
   "Analysis Mode":"Use headings: Problem, Given/Assumptions, Method, Steps, Final Answer, Verification. Explain the solution clearly; do not expose hidden chain-of-thought."
  }
  system_extra="MODE: "+mode_prompts[mode]+"\nANSWER DEPTH: "+depth_rules[depth]
  if st.session_state.get("use_pdf_context") and st.session_state.notes.strip():
   system_extra += "\nPDF SOURCE RULE: Treat the following uploaded PDF text as the primary source. Cite page labels like [PDF page 2] in prose when useful. If the PDF does not support the answer, explicitly say 'I could not find this in the uploaded PDF' before adding general explanation. Do not invent page numbers.\nUPLOADED PDF TEXT:\n"+st.session_state.notes
  hist=[{"role":"system","content":system_for_language(system_extra)}]+st.session_state.chat[-10:]
  # Attach an image only to the current Smart Doubt Solver request. OpenAI-compatible
  # vision APIs expect the user message content as text + image_url parts.
  pending_img=st.session_state.pop("pending_doubt_image",None)
  if pending_img and hist and hist[-1].get("role")=="user":
   hist[-1]={"role":"user","content":[
    {"type":"text","text":q+"\n\nAttached image filename: "+pending_img.get("name","uploaded image")+". Read the image carefully and use it as evidence for the question/attempt."},
    {"type":"image_url","image_url":{"url":pending_img["data_url"]}}
   ]}
  with chat_col:
   with st.chat_message("assistant"):
    with st.spinner("BuddhiX is thinking…"): ans,e=call(hist,max_tokens=2600 if depth!="Quick" else 1200)
    if e:
     st.error(e)
     if pending_img: ans="I couldn't analyze the image. Your configured model may not support image/vision input, or the provider rejected the image. Try a vision-capable model in .env, or paste the question and working as text. Details: "+str(e)[:250]
     else: ans="I couldn't complete this request. Check the API key/network and retry. Details: "+str(e)[:250]
    st.markdown(format_math(ans))
  st.session_state.chat.append({"role":"assistant","content":ans})
  if ans and not e:
   render_speech_button(ans, key="voice_reply_latest")

elif page=="Battle Field":
 st.markdown('<div class="hero"><h1>⚔️ Study Battle Arena</h1><p>Beat the clock, build a correct-answer streak, earn XP and review every answer.</p></div>',unsafe_allow_html=True)
 st.markdown('<div class="battle-card"><div style="font-size:12px;letter-spacing:.12em;color:#c8c3ff!important;font-weight:800">BUDDHIX ARENA</div><h2 style="margin:.35rem 0">Ready, challenger?</h2><p>Correct answers earn XP. Three correct answers in a row earn streak bonus. Finish fast for extra XP.</p></div>',unsafe_allow_html=True)
 reward_summary=con.execute("SELECT COALESCE(SUM(xp),0), COUNT(*), COALESCE(MAX(best_streak),0) FROM battle_rewards").fetchone()
 rx1,rx2,rx3=st.columns(3)
 rx1.metric("🏆 Lifetime XP", int(reward_summary[0] or 0))
 rx2.metric("⚔️ Battles completed", int(reward_summary[1] or 0))
 rx3.metric("🔥 Best streak", int(reward_summary[2] or 0))
 if "battle_quiz" not in st.session_state: st.session_state.battle_quiz=None
 if "battle_result" not in st.session_state: st.session_state.battle_result=None
 xp_map={"Easy":5,"Medium":10,"Hard":20}
 with st.form("battle_setup"):
  st.markdown("### 🛠️ Configure your battle")
  bc1,bc2,bc3=st.columns([1.5,1,1])
  with bc1: battle_topic=st.text_input("Topic / subject",placeholder="e.g. Laplace Transform, DBMS Normalization")
  with bc2: battle_diff=st.selectbox("Difficulty",["Easy","Medium","Hard"],index=1)
  with bc3: battle_n=st.selectbox("Questions",[5,10,15],index=0)
  timer_minutes=st.radio("Time limit",[2,5,10,15],index=1,horizontal=True)
  st.caption("XP per correct answer: Easy 5 · Medium 10 · Hard 20 | +5 XP per 3-answer streak | +10 fast finish | +25 perfect battle")
  start_battle=st.form_submit_button("⚡ Generate Questions & Enter Arena",use_container_width=True)
 if start_battle:
  if not battle_topic.strip(): st.error("Enter a topic first so BuddhiX knows what to ask.")
  else:
   with st.spinner(f"Generating {battle_n} concise {battle_diff.lower()} questions…"):
    qs,err=quiz_make(battle_topic.strip(),battle_diff,battle_n)
   if err:
    st.error("Battle questions could not be loaded.");st.warning(err)
    with st.expander("Troubleshooting"):
     st.markdown("- Try a specific topic instead of a broad subject name.\n- Start with **5 questions**.\n- Check your API quota and network if generation fails.")
   else:
    st.session_state.battle_quiz={"topic":battle_topic.strip(),"difficulty":battle_diff,"questions":qs,"minutes":timer_minutes,"started":datetime.now().timestamp()}
    st.session_state.battle_result=None
    for k in list(st.session_state.keys()):
     if str(k).startswith("battle_answer_"): del st.session_state[k]
    st.rerun()
 bq=st.session_state.battle_quiz
 if bq and not st.session_state.battle_result:
  questions=bq["questions"];total_q=len(questions);per_correct=xp_map.get(bq["difficulty"],10)
  st.markdown(f'### 🥊 {bq["topic"]} <span class="battle-badge">{bq["difficulty"].upper()} MODE</span>',unsafe_allow_html=True)
  # A native Streamlit fragment refreshes the clock once per second without resetting answers.
  @st.fragment(run_every="1s")
  def battle_clock(started, minutes):
   elapsed=max(0,int(datetime.now().timestamp()-started));remaining=max(0,minutes*60-elapsed)
   c1,c2,c3=st.columns(3)
   c1.metric("⚔️ Questions",str(total_q))
   c2.metric("⭐ XP per correct",f"{per_correct} XP")
   c3.metric("⏱️ Time remaining",f"{remaining//60:02d}:{remaining%60:02d}")
   if remaining<=0: st.error("⏰ Time is up! Submit now. Unanswered questions count as skipped.")
  battle_clock(bq["started"],bq["minutes"])
  answered=sum(1 for i in range(total_q) if st.session_state.get(f"battle_answer_{i}") is not None)
  st.progress(answered/total_q,text=f"{answered} of {total_q} answered")
  with st.form("battle_answers"):
   battle_answers={}
   for qi,item in enumerate(questions):
    st.markdown(f'<div class="battle-question"><span class="battle-badge">QUESTION {qi+1} / {total_q}</span><div style="font-size:17px;font-weight:700;color:#172554;margin-top:9px">{item["question"]}</div></div>',unsafe_allow_html=True)
    battle_answers[str(qi)]=st.radio("Choose one answer",["A","B","C","D"],key=f"battle_answer_{qi}",index=None,format_func=lambda k,o=item["options"]:f"{k}. {o[k]}",horizontal=False)
   submit_battle=st.form_submit_button("🏁 Submit Battle & Calculate XP",use_container_width=True)
  if submit_battle:
   elapsed=max(0,int(datetime.now().timestamp()-bq["started"]));remaining=max(0,bq["minutes"]*60-elapsed);on_time=remaining>0
   correct=sum(battle_answers.get(str(i))==item["answer"] for i,item in enumerate(questions))
   total=len(questions);streak=0;best_streak=0;streak_bonus=0;streak_details=[]
   for i,item in enumerate(questions):
    if battle_answers.get(str(i))==item["answer"]:
     streak+=1
     if streak%3==0: streak_bonus+=5
     best_streak=max(best_streak,streak)
    else: streak=0
   fast_bonus=10 if on_time and total>0 and correct/total>=.8 else 0
   perfect_bonus=25 if total>0 and correct==total else 0
   bonus=streak_bonus+fast_bonus+perfect_bonus
   xp=correct*per_correct+bonus
   weak=list(dict.fromkeys(item.get("concept",bq["topic"]) for i,item in enumerate(questions) if battle_answers.get(str(i))!=item["answer"]))
   completed_at=datetime.now().isoformat(timespec="seconds")
   con.execute("INSERT INTO attempts(created,topic,score,total,weak) VALUES(?,?,?,?,?)",(completed_at,"Battle: "+bq["topic"],correct,total,", ".join(weak)))
   con.execute("INSERT INTO battle_rewards(created,topic,difficulty,xp,correct,total,best_streak,bonus,elapsed_seconds) VALUES(?,?,?,?,?,?,?,?,?)",(completed_at,bq["topic"],bq["difficulty"],xp,correct,total,best_streak,bonus,elapsed))
   con.commit()
   st.session_state.battle_result={"correct":correct,"total":total,"xp":xp,"bonus":bonus,"streak_bonus":streak_bonus,"fast_bonus":fast_bonus,"perfect_bonus":perfect_bonus,"best_streak":best_streak,"answers":battle_answers,"weak":weak,"on_time":on_time,"elapsed":elapsed}
   st.rerun()
 if st.session_state.battle_result:
  br=st.session_state.battle_result;accuracy=round(100*br["correct"]/max(1,br["total"]))
  if accuracy==100: rank="🏆 S Rank — Perfect Run!"
  elif accuracy>=80: rank="🥇 A Rank — Excellent!"
  elif accuracy>=60: rank="🥈 B Rank — Good effort!"
  else: rank="⚔️ Keep training — rematch!"
  st.markdown(f'<div class="battle-card"><h2>🏆 Battle complete!</h2><p>{rank}</p><p>Your result is saved in local quiz history.</p></div>',unsafe_allow_html=True)
  r1,r2,r3,r4=st.columns(4);r1.metric("Correct answers",f"{br['correct']}/{br['total']}");r2.metric("Accuracy",f"{accuracy}%");r3.metric("XP earned",f"+{br['xp']}");r4.metric("Best streak",f"🔥 {br['best_streak']}")
  st.progress(br["correct"]/max(1,br["total"]),text=f"Final accuracy: {accuracy}%")
  st.markdown("### ✨ XP breakdown")
  x1,x2,x3=st.columns(3);x1.metric("Answer XP",br["xp"]-br["bonus"]);x2.metric("Streak bonus",f"+{br['streak_bonus']} XP");x3.metric("Achievement bonus",f"+{br['fast_bonus']+br['perfect_bonus']} XP")
  st.caption(f"Time used: {br['elapsed']//60:02d}:{br['elapsed']%60:02d} · {'Finished within time' if br['on_time'] else 'Time limit exceeded'}")
  st.markdown("### 🧾 Answer review")
  for qi,item in enumerate(st.session_state.battle_quiz["questions"]):
   ua=br["answers"].get(str(qi));is_correct=ua==item["answer"]
   with st.container(border=True):
    st.markdown(f"**{'✅' if is_correct else '❌'} Q{qi+1}. {item['question']}**")
    st.write(f"Your answer: {ua or 'Skipped'} · Correct answer: {item['answer']}")
    st.caption(item.get("explanation","Review this concept."))
  if br["weak"]: st.warning("Revision targets: "+", ".join(br["weak"]))
  if st.button("🔁 Start another battle",use_container_width=True):
   st.session_state.battle_quiz=None;st.session_state.battle_result=None
   for k in list(st.session_state.keys()):
    if str(k).startswith("battle_answer_"): del st.session_state[k]
   st.rerun()

elif page=="Test Mode":
 st.markdown('<div class="hero"><h1>🎯 Test Mode</h1><p>Generate questions, submit answers, see your score and review explanations.</p></div>',unsafe_allow_html=True)
 with st.form("gen"):
  topic=st.text_input("Topic",placeholder="e.g. RC charging in Network Analysis")
  diff=st.select_slider("Difficulty",["Easy","Medium","Hard"],value="Medium")
  n=st.select_slider("Questions",[3,5,8,10],value=5)
  go=st.form_submit_button("Generate quiz")
 if go:
  if not topic.strip():st.error("Enter a topic.")
  else:
   with st.spinner(f"Generating {n} concise questions for {topic.strip()}…"):qs,e=quiz_make(topic,diff,n)
   if e:st.error(e)
   else:st.session_state.quiz={"topic":topic,"questions":qs};st.session_state.submitted=False;st.session_state.answers={};st.rerun()
 qu=st.session_state.quiz
 if qu:
  st.subheader(qu["topic"])
  if not st.session_state.submitted:
   with st.form("quiz_submission_form"):
    ans={}
    for i,x in enumerate(qu["questions"]):
     st.markdown(f"**Q{i+1}. {x['question']}**")
     ans[str(i)]=st.radio("Select",["A","B","C","D"],format_func=lambda k,o=x["options"]:f"{k}. {o[k]}",key=f"ans{i}",index=None)
     st.divider()
    submit=st.form_submit_button("Submit & score")
   if submit:
    score=sum(ans.get(str(i))==x["answer"] for i,x in enumerate(qu["questions"]))
    weak=list(dict.fromkeys(x.get("concept",qu["topic"]) for i,x in enumerate(qu["questions"]) if ans.get(str(i))!=x["answer"]))
    con.execute("INSERT INTO attempts(created,topic,score,total,weak) VALUES(?,?,?,?,?)",(datetime.now().isoformat(timespec="minutes"),qu["topic"],score,len(qu["questions"]),", ".join(weak)));con.commit()
    st.session_state.answers=ans;st.session_state.score=score;st.session_state.submitted=True;st.rerun()
  else:
   total=len(qu["questions"]);score=st.session_state.score
   st.metric("Score",f"{score}/{total}",f"{round(100*score/total)}%")
   for i,x in enumerate(qu["questions"]):
    ua=st.session_state.answers.get(str(i))
    st.markdown(f"**Q{i+1}. {x['question']}**")
    st.write(f"Your answer: {ua or 'Not answered'} · Correct: {x['answer']}")
    st.write(("✅ Correct" if ua==x["answer"] else "❌ Review") + " — "+x.get("explanation",""))
    st.divider()
   if st.button("New quiz"):st.session_state.quiz=None;st.session_state.submitted=False;st.rerun()
elif page=="Learning Kit":
 st.markdown('<div class="hero"><h1>📚 Complete Learning Kit</h1><p>Explanations, formulas, examples, flashcards and revision questions.</p></div>',unsafe_allow_html=True)
 with st.form("kit"):
  topic=st.text_input("Topic")
  level=st.selectbox("Level",["Beginner","College / Engineering","Exam revision"])
  go=st.form_submit_button("Build learning kit")
 if go:
  with st.spinner("Building learning kit…"):
   out,e=call([
    {"role":"system","content":SYSTEM},
    {"role":"user","content":f"Create a thorough learning kit for {topic} at {level} in {st.session_state.get("response_language", "Hinglish")}. Include prerequisites, intuition, definition, step-by-step explanation/derivation, symbols explained, key formulas in Markdown math, a worked example, common mistakes, 5 revision bullets, 5 flashcards, 5 self-test questions, and answer key. Clearly distinguish verified source material from general explanation."}
   ],.25,2400)
  if e:
    st.error(e)
  else:
    st.markdown(format_math(out))
elif page=="Study Planner":
 st.markdown('<div class="hero"><h1>🗓️ Study Planner</h1><p>Plan your study sessions, track completion, and build a consistent weekly routine — no AI API needed for task tracking.</p></div>',unsafe_allow_html=True)
 import pandas as pd
 from datetime import date, timedelta
 today=date.today()
 all_tasks=con.execute("SELECT id,task,subject,due_date,minutes,priority,done FROM planner_tasks ORDER BY due_date, CASE priority WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END, id").fetchall()
 week_end=today+timedelta(days=6)
 week_tasks=[r for r in all_tasks if today.isoformat() <= r[3] <= week_end.isoformat()]
 completed_week=sum(1 for r in week_tasks if r[6])
 total_week=len(week_tasks)
 planned_minutes=sum(int(r[4] or 0) for r in week_tasks)
 m1,m2,m3,m4=st.columns(4)
 m1.metric("This week's tasks",total_week)
 m2.metric("Completed",completed_week)
 m3.metric("Completion",f"{round(completed_week/max(total_week,1)*100)}%" if total_week else "0%")
 m4.metric("Planned study",f"{planned_minutes//60}h {planned_minutes%60}m")
 st.progress(completed_week/max(total_week,1),text=f"Weekly progress · {completed_week}/{total_week} tasks complete")
 with st.expander("➕ Add a study task",expanded=not bool(all_tasks)):
  with st.form("planner_add_task",clear_on_submit=True):
   c1,c2=st.columns([2,1])
   with c1: task_name=st.text_input("Task",placeholder="e.g. Revise Thevenin theorem")
   with c2: task_subject=st.text_input("Subject",placeholder="NAS")
   c3,c4,c5=st.columns(3)
   with c3: due=st.date_input("Due date",value=today,min_value=today)
   with c4: minutes=st.selectbox("Study duration",[15,25,30,45,60,90,120],index=2,format_func=lambda x:f"{x} minutes")
   with c5: priority=st.selectbox("Priority",["High","Medium","Low"],index=1)
   add_task=st.form_submit_button("＋ Save task",use_container_width=True)
  if add_task:
   if task_name.strip():
    con.execute("INSERT INTO planner_tasks(task,subject,due_date,minutes,priority,done,created_at) VALUES(?,?,?,?,?,0,?)",(task_name.strip(),task_subject.strip() or "General",due.isoformat(),int(minutes),priority,datetime.now().isoformat(timespec="seconds")))
    con.commit(); st.success("Task saved to your local planner."); st.rerun()
   else: st.warning("Task ka naam enter karo.")
 st.markdown("### 📅 Your study tasks")
 f1,f2=st.columns([1,1])
 with f1: task_filter=st.selectbox("Show",["All tasks","Today","Next 7 days","Pending","Completed"],key="planner_filter")
 with f2: subject_filter=st.text_input("Filter by subject",placeholder="e.g. DBMS",key="planner_subject_filter")
 filtered=[]
 for r in all_tasks:
  rid,name,subject,due_s,duration,prio,done=r
  if task_filter=="Today" and due_s!=today.isoformat(): continue
  if task_filter=="Next 7 days" and not(today.isoformat()<=due_s<=week_end.isoformat()): continue
  if task_filter=="Pending" and done: continue
  if task_filter=="Completed" and not done: continue
  if subject_filter.strip() and subject_filter.lower() not in str(subject).lower(): continue
  filtered.append(r)
 if not filtered:
  st.info("No tasks match this filter. Add a task above to start tracking your study routine.")
 else:
  for rid,name,subject,due_s,duration,prio,done in filtered:
   with st.container(border=True):
    left,mid,right=st.columns([0.12,2.5,1])
    with left:
     checked=st.checkbox("Done",value=bool(done),key=f"planner_done_{rid}",label_visibility="collapsed")
    if checked != bool(done):
     con.execute("UPDATE planner_tasks SET done=? WHERE id=?",(int(checked),rid));con.commit();st.rerun()
    with mid:
     st.markdown(("~~"+name+"~~") if done else "**"+name+"**")
     st.caption(f"{subject} · {due_s} · {duration} min · {prio} priority")
    with right:
     if st.button("🗑 Delete",key=f"planner_delete_{rid}"):
      con.execute("DELETE FROM planner_tasks WHERE id=?",(rid,));con.commit();st.rerun()
 st.markdown("### 📊 Weekly completion by day")
 day_labels=[(today+timedelta(days=i)) for i in range(7)]
 chart_rows=[]
 for day in day_labels:
  rows=con.execute("SELECT COUNT(*), COALESCE(SUM(done),0) FROM planner_tasks WHERE due_date=?",(day.isoformat(),)).fetchone()
  chart_rows.append({"Day":day.strftime("%a %d"),"Tasks":int(rows[0] or 0),"Completed":int(rows[1] or 0)})
 st.bar_chart(pd.DataFrame(chart_rows).set_index("Day"),use_container_width=True)
 st.caption("Tasks and completion data are saved locally in buddhix.db on this device.")
 st.divider()
 st.markdown("### ✨ Generate an AI study schedule (optional)")
 st.caption("This section uses your AI API quota. The task planner above works without an API key.")
 with st.form("plan"):
  subjects=st.text_area("Subjects / backlog",placeholder="NAS, DBMS, Python…")
  hours=st.slider("Focused hours per day",1,8,3)
  days=st.slider("Plan length",1,14,7)
  deadline=st.text_input("Deadline/context")
  go=st.form_submit_button("Generate plan")
 if go:
  prompt=f"Create a realistic study plan as markdown. Subjects: {subjects}. Hours/day: {hours}. Days: {days}. Deadline: {deadline}. Use daily time blocks, breaks, deliverables, review, buffer. Do not exceed daily hours."
  with st.spinner("Planning…"):
   out,e=call([{"role":"system","content":system_for_language()},{"role":"user","content":prompt+" Write the plan in "+st.session_state.get("response_language", "Hinglish")}],.25,2200)
  if e: st.error(e)
  else: st.markdown(format_math(out))
elif page=="My Progress":
 st.markdown('<div class="hero"><h1>📈 My Progress</h1><p>Your real study analytics — built only from quizzes saved on this device.</p></div>',unsafe_allow_html=True)
 all_rows=con.execute("SELECT id,created,topic,score,total,weak FROM attempts ORDER BY id DESC").fetchall()
 if not all_rows:
  st.info("No quiz attempts saved yet. Complete a Practice quiz or Study Battle round and your real results will appear here.")
  st.markdown("### 🚀 How to start tracking")
  st.markdown("1. Open **Practice** or **Study Battle**.\n2. Complete a quiz and submit your answers.\n3. Return here to see your accuracy, weak topics and history.")
 else:
  import pandas as pd
  df=pd.DataFrame(all_rows,columns=["ID","Date","Topic","Score","Total","Weak topics"])
  df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
  df=df.dropna(subset=["Date"])
  f1,f2=st.columns([1,2])
  with f1:
   period=st.selectbox("Time range",["Last 7 days","Last 30 days","All time"],index=1,key="progress_period")
  with f2:
   search_topic=st.text_input("Find a topic",placeholder="e.g. Network Analysis, DBMS…",key="progress_topic_filter")
  filtered=df.copy()
  if period!="All time":
   days=7 if period=="Last 7 days" else 30
   cutoff=pd.Timestamp.now()-pd.Timedelta(days=days)
   filtered=filtered[filtered["Date"]>=cutoff]
  if search_topic.strip():
   filtered=filtered[filtered["Topic"].astype(str).str.contains(search_topic.strip(),case=False,na=False)]
  if filtered.empty:
   st.warning("No saved attempts match these filters. Try a wider time range or clear the topic search.")
  else:
   filtered=filtered.copy()
   filtered["Accuracy"]=(filtered["Score"] / filtered["Total"].clip(lower=1) * 100)
   attempts=len(filtered)
   questions=int(filtered["Total"].sum())
   correct=int(filtered["Score"].sum())
   accuracy=round(100*correct/max(1,questions))
   avg_attempt=round(filtered["Accuracy"].mean())
   best=int(filtered["Accuracy"].max())
   m1,m2,m3,m4=st.columns(4)
   m1.metric("Quiz attempts",attempts)
   m2.metric("Questions answered",questions)
   m3.metric("Overall accuracy",f"{accuracy}%")
   m4.metric("Best attempt",f"{best}%")
   st.caption(f"Showing {attempts} saved attempt(s) · weighted accuracy uses total correct answers ÷ total questions. Average quiz accuracy: {avg_attempt}%.")
   st.markdown("### 📈 Performance over time")
   trend=filtered.sort_values("Date").set_index("Date")
   st.line_chart(trend[["Accuracy"]],y="Accuracy",use_container_width=True)
   topic_stats=(filtered.groupby("Topic",as_index=False)
                .agg(Attempts=("Accuracy","count"),
                     Questions=("Total","sum"),
                     Correct=("Score","sum"),
                     Accuracy=("Accuracy","mean")))
   topic_stats["Accuracy"]=topic_stats["Accuracy"].round().astype(int)
   topic_stats=topic_stats.sort_values(["Accuracy","Attempts"],ascending=[True,False])
   left,right=st.columns([1.15,1])
   with left:
    st.markdown("### 🎯 Topic-wise performance")
    chart=topic_stats.set_index("Topic")[["Accuracy"]].rename(columns={"Accuracy":"Accuracy (%)"})
    st.bar_chart(chart,use_container_width=True)
   with right:
    st.markdown("### 🧭 What to revise next")
    weak_topics=topic_stats[topic_stats["Accuracy"]<80].head(5)
    if weak_topics.empty:
     st.success("Great work — all topics in this view are at 80% accuracy or above. Keep revising to retain them.")
    else:
     for _,item in weak_topics.iterrows():
      label=str(item["Topic"])
      acc=int(item["Accuracy"])
      st.write(f"**{label}** · {acc}% · {int(item['Attempts'])} attempt(s)")
      if acc<60: st.caption("Priority: revise the basics, then retry a short quiz.")
      else: st.caption("Practise a few more questions and review mistakes.")
   st.markdown("### 🗂️ Attempt history")
   history=filtered.sort_values("Date",ascending=False).copy()
   history["Date"]=history["Date"].dt.strftime("%d %b %Y, %I:%M %p")
   history["Accuracy"]=history["Accuracy"].round().astype(int).astype(str)+"%"
   st.dataframe(history[["Date","Topic","Score","Total","Accuracy","Weak topics"]],use_container_width=True,hide_index=True)
   with st.expander("How these numbers are calculated"):
    st.write("**Overall accuracy** = all correct answers divided by all questions in the selected attempts. **Topic accuracy** = average quiz accuracy for each saved topic. The dashboard does not generate or add sample scores.")
 st.caption("Data source: local buddhix.db on this computer. It is not cloud-synced.")
elif page=="Agent Blueprint":
 st.markdown('<div class="hero"><h1>🧩 Agent Blueprint</h1><p>Implemented modules are separated from planned distributed agents.</p></div>',unsafe_allow_html=True)
 st.code("""Student
  ↓
BuddhiX Streamlit UI
  ├─ Tutor / Analysis / Exam Prep → ASI:One Chat Completions API
  ├─ Quiz Generator → AI-generated JSON → validation → local scoring
  ├─ Learning Kit → structured AI content
  ├─ Study Planner → AI-generated schedule
  ├─ Notes Q&A → PDF text extraction → AI
  └─ Progress Tracker → local SQLite""")
 st.info("Implemented when configured: API-powered tutoring, quiz generation/scoring, learning kit, planner, selectable-text PDF extraction, local progress, daily goals, and Battle Field scoring. Voice Tutor supports optional Groq Whisper transcription (GROQ_API_KEY) and browser-native text-to-speech; transcription needs internet access and a valid Groq key.")
 st.warning("Separate distributed Fetch.ai uAgents are NOT implemented in this ZIP yet. Do not claim they are running. The diagram shows app modules, not independent network agents.")
 st.info("Tutor improvements in this version: visible learning modes, selectable response depth, PDF-source toggle, page-labelled PDF extraction, adaptive practice instructions, and more detailed learning kits.")
 st.markdown("### Run")
 st.code("python -m pip install -r requirements.txt\\nstreamlit run app.py")
 st.markdown("### API settings")
 st.code("ASI_ONE_API_KEY=your_key_here\\nASI_ONE_BASE_URL=https://api.asi1.ai/v1\\nASI_ONE_MODEL=asi1")
