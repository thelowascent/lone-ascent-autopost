"""
Central config for The Lone Ascent auto-poster.
Edit brand colors, handle, and the AI voice here — nothing else needs touching.
"""
import os

# ---- Brand handle shown on every card ----
HANDLE = "@thelowascent"   # <-- change to your exact IG handle

# ---- Canvas (Instagram 4:5 portrait = best feed real estate) ----
WIDTH, HEIGHT = 1080, 1350

# ---- Palette (dark / cinematic / grindset) ----
BG_TOP     = (10, 10, 12)      # near-black, top of gradient
BG_BOTTOM  = (18, 18, 22)      # slightly lifted, bottom of gradient
TEXT       = (243, 245, 250)   # icy white
ACCENT     = (214, 40, 40)     # red accent bar
MUTED      = (120, 122, 130)   # handle / footer

# ---- Fonts (bundled in assets/fonts so the runner needs no system fonts) ----
_FONT_DIR  = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
QUOTE_FONT = os.path.join(_FONT_DIR, "Poppins-Bold.ttf")
META_FONT  = os.path.join(_FONT_DIR, "DejaVuSans.ttf")

# ---- The AI voice. This is what makes posts sound like YOU, not generic. ----
VOICE_BRIEF = (
    "You write for 'The Lone Ascent', a faceless self-improvement and fitness brand. "
    "Voice: dark, stoic, disciplined, first-person, grindset — like a quiet inner monologue "
    "at 5am, not a loud motivational poster. No emojis in the quote. No hashtags in the quote. "
    "Every line must be ORIGINAL — never reproduce or lightly reword any existing quote, lyric, "
    "book line, or known saying."
)

# Model on Gemini's free tier
GEMINI_MODEL = "gemini-2.5-flash"

# Graph API version (bump when Meta deprecates; configurable via repo variable)
GRAPH_VERSION = os.environ.get("GRAPH_VERSION") or "v22.0"
