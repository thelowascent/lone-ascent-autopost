"""
render_card.py — turn a quote string into a branded PNG.
Auto-shrinks the quote font so any length fits cleanly inside the safe area.
"""
from PIL import Image, ImageDraw, ImageFont
import config


def _gradient(w, h, top, bottom):
    base = Image.new("RGB", (w, h), top)
    top_r, top_g, top_b = top
    bot_r, bot_g, bot_b = bottom
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top_r + (bot_r - top_r) * t)
        g = int(top_g + (bot_g - top_g) * t)
        b = int(top_b + (bot_b - top_b) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return base


def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def render(quote: str, out_path: str):
    W, H = config.WIDTH, config.HEIGHT
    img = _gradient(W, H, config.BG_TOP, config.BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    margin = 130
    max_w = W - margin * 2
    max_block_h = H - margin * 2 - 200  # leave room for accent bar + handle

    # Auto-fit: find the biggest font size whose wrapped block fits.
    chosen_font, chosen_lines, line_h = None, None, None
    for size in range(96, 39, -2):
        font = ImageFont.truetype(config.QUOTE_FONT, size)
        lines = _wrap(draw, quote, font, max_w)
        asc, desc = font.getmetrics()
        lh = int((asc + desc) * 1.22)
        if lh * len(lines) <= max_block_h:
            chosen_font, chosen_lines, line_h = font, lines, lh
            break
    if chosen_font is None:  # extremely long quote fallback
        chosen_font = ImageFont.truetype(config.QUOTE_FONT, 40)
        chosen_lines = _wrap(draw, quote, chosen_font, max_w)
        asc, desc = chosen_font.getmetrics()
        line_h = int((asc + desc) * 1.22)

    block_h = line_h * len(chosen_lines)
    y = (H - block_h) // 2 - 40

    # Accent bar above the quote
    draw.rectangle([margin, y - 60, margin + 90, y - 50], fill=config.ACCENT)

    for line in chosen_lines:
        draw.text((margin, y), line, font=chosen_font, fill=config.TEXT)
        y += line_h

    # Handle, bottom-left, with a small red tick
    meta_font = ImageFont.truetype(config.META_FONT, 34)
    hy = H - margin + 10
    draw.rectangle([margin, hy + 6, margin + 28, hy + 12], fill=config.ACCENT)
    draw.text((margin + 44, hy - 8), config.HANDLE, font=meta_font, fill=config.MUTED)

    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    render("Discipline is just remembering what you actually want.",
           "output/_preview.png")
    print("wrote output/_preview.png")
