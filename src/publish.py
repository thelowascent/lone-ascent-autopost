"""
publish.py — STEP 2 of the daily job (runs AFTER the image is committed + pushed).
Builds the public raw.githubusercontent URL for today's card, waits for it to be
reachable, then does the Instagram two-step publish (create container -> publish).

Env required:
  IG_USER_ID        Instagram Business/Creator account ID
  IG_ACCESS_TOKEN   long-lived or (better) non-expiring system-user token
  GITHUB_REPOSITORY owner/repo            (auto-set by GitHub Actions)
  GITHUB_REF_NAME   branch, e.g. main     (auto-set by GitHub Actions)
Optional:
  GRAPH_VERSION     default v22.0
"""
import os
import json
import time
import requests
import config

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
GRAPH = f"https://graph.facebook.com/{config.GRAPH_VERSION}"


def raw_url(filename: str) -> str:
    repo = os.environ["GITHUB_REPOSITORY"]            # owner/repo
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/output/{filename}"


def wait_until_live(url: str, tries: int = 12, delay: int = 15):
    for i in range(tries):
        try:
            if requests.head(url, timeout=20).status_code == 200:
                return True
        except requests.RequestException:
            pass
        print(f"image not live yet ({i+1}/{tries}); waiting {delay}s")
        time.sleep(delay)
    raise RuntimeError(f"image never became reachable: {url}")


def publish(image_url: str, caption: str):
    ig_id = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]

    # 1) create media container
    r = requests.post(f"{GRAPH}/{ig_id}/media",
                      data={"image_url": image_url, "caption": caption,
                            "access_token": token}, timeout=60)
    if not r.ok:
        print("Meta error:", r.status_code, r.text)
    r.raise_for_status()
    creation_id = r.json()["id"]
    print("container:", creation_id)

    # 2) small wait for Instagram to fetch/process the image
    time.sleep(10)

    # 3) publish
    r = requests.post(f"{GRAPH}/{ig_id}/media_publish",
                      data={"creation_id": creation_id, "access_token": token},
                      timeout=60)
    r.raise_for_status()
    print("published media id:", r.json().get("id"))


def main():
    with open(os.path.join(OUT_DIR, "latest.json"), encoding="utf-8") as f:
        meta = json.load(f)
    url = raw_url(meta["filename"])
    print("image url:", url)
    wait_until_live(url)
    publish(url, meta["caption"])


if __name__ == "__main__":
    main()
