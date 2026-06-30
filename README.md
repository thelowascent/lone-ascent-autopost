# The Lone Ascent — daily auto-poster

Runs free, in the cloud, untouched. Once a day GitHub Actions wakes, Gemini writes an
original line, Pillow renders a branded card, the image is committed (so it has a public
URL), and Instagram's Graph API posts it.

**Cost: ₹0/month.** GitHub Actions (free), Gemini Flash free tier, Pillow, Graph API — all free.

```
make_post.py   -> Gemini quote + caption + hashtags, render PNG, write latest.json
(git commit)   -> pushes the PNG so raw.githubusercontent.com serves it publicly
publish.py     -> create media container from that URL -> publish
```

---

## What you do once (the only manual part)

### A. Instagram / Meta side  (~45–90 min, do it fresh, not at 2am)

1. **Make the IG account Professional.** In the Instagram app: Settings → switch to
   **Business** or **Creator**. (Personal accounts cannot use the publishing API.)
2. **Link it to a Facebook Page.** Create a Page if you don't have one, then link the IG
   account to it (Instagram settings → Page linking). The Page link is mandatory.
3. **Create a Meta app.** Go to developers.facebook.com → My Apps → Create App →
   type **Business** → add the **Instagram** / Instagram Graph API product.
4. **Get a non-expiring token (the important bit).** In **Meta Business Settings → System
   Users**, create a system user, assign it your app + Page/IG asset, and **generate a
   token** with scopes: `instagram_basic`, `instagram_content_publish`,
   `pages_show_list`, `pages_read_engagement`, `business_management`.
   System-user tokens **don't expire** — so there's no 60-day refresh chore.
5. **Get your IG user ID.** Call (Graph API Explorer or curl):
   `GET /<PAGE_ID>?fields=instagram_business_account&access_token=<TOKEN>`
   The returned `instagram_business_account.id` is your `IG_USER_ID`.
6. **You do NOT need App Review** for this. App Review / the 25-user limit only applies
   when an app posts to *other people's* accounts. You're posting to your own account as
   the app owner, so the app can stay in **development mode**. (If a "Page Publishing
   Authorization" prompt appears, complete it once.)

> Note: Meta renames screens often. The two things you must walk away with are the
> **token** and the **IG_USER_ID**. Everything else is plumbing to get those two.

### B. Gemini key  (~3 min)

- aistudio.google.com → **Get API key** → create key in a new project. No card needed.
  Free tier is ~1,500 requests/day — one post/day doesn't dent it.

### C. GitHub side  (~10 min)

1. Create a **public** repo (public so the raw image URL is fetchable by Meta) and push
   this folder to it.
2. Repo → **Settings → Secrets and variables → Actions → New repository secret**, add:
   - `GEMINI_API_KEY`
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`  (the system-user token)
3. (Optional) under the **Variables** tab add `GRAPH_VERSION` = `v22.0`.
4. Open `src/config.py` and set `HANDLE` to your exact IG handle. Tweak colors if you want.
5. Repo → **Actions** tab → enable workflows → open **Daily Instagram post** →
   **Run workflow** to fire a manual test. Watch it post.

After the test works, it runs on its own at the cron time (default 03:30 UTC = 09:00 IST).
Change the time in `.github/workflows/daily-post.yml`.

---

## Local test (optional)
```bash
pip install -r requirements.txt
export GEMINI_API_KEY=...      # test text + render only
cd src && python make_post.py  # writes output/<date>.png + latest.json
```

## Knobs
- **Voice:** `src/config.py` → `VOICE_BRIEF`.
- **Look:** `src/config.py` colors, or drop a custom `.ttf` into `assets/fonts/` and point
  `QUOTE_FONT` at it.
- **Posting time:** the `cron` line in the workflow.
- Instagram allows 50 posts / 24h — far above one a day.
