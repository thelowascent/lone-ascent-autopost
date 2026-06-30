"""
make_post.py — STEP 1 of the daily job (runs before the git commit).
Generates the quote, renders the card to output/YYYY-MM-DD.png, and writes
output/latest.json so the publish step knows the filename + caption.
"""
import os
import json
import datetime
import generate_quote
import render_card

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    today = datetime.date.today().isoformat()
    filename = f"{today}.png"
    png_path = os.path.join(OUT_DIR, filename)

    post = generate_quote.generate()
    render_card.render(post["quote"], png_path)

    caption = post["caption"].strip()
    if post.get("hashtag_line"):
        caption += "\n\n" + post["hashtag_line"]

    meta = {"filename": filename, "caption": caption, "quote": post["quote"]}
    with open(os.path.join(OUT_DIR, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("Generated:", post["quote"])
    print("Saved:", png_path)


if __name__ == "__main__":
    main()
