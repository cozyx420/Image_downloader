# downloader.py
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class DownloadError(Exception):
    """Eigener Fehler für Download-Probleme."""
    pass


def sanitize_filename(name: str) -> str:
    # Ungültige Zeichen für Dateinamen entfernen/ersetzen
    name = name.strip().replace(" ", "_")
    return re.sub(r'[^A-Za-z0-9_\-\.]', '_', name)


def get_page_soup(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def extract_image_urls(page_url: str) -> list[tuple[str, str]]:
    """
    Gibt eine Liste (bild_url, ursprünglicher_name) zurück.
    """
    soup = get_page_soup(page_url)
    img_tags = soup.find_all("img")

    image_urls: list[tuple[str, str]] = []
    seen = set()

    for img in img_tags:
        src = img.get("src")
        if not src:
            continue
        # data:-URLs ignorieren
        if src.startswith("data:"):
            continue

        full_url = urljoin(page_url, src)
        if full_url in seen:
            continue
        seen.add(full_url)

        parsed = urlparse(full_url)
        filename = os.path.basename(parsed.path) or "image"
        image_urls.append((full_url, filename))

    return image_urls


def download_images(
    page_url: str,
    target_folder: str,
    naming_scheme: str = "original",
) -> dict:
    """
    Lädt alle Bilder von page_url in target_folder.

    naming_scheme:
        - "original": Original-Dateinamen, Duplikate werden durchnummeriert
        - "slugged":  seitenname-001.jpg, seitenname-002.jpg, ...
    Rückgabe: dict mit Infos für die GUI.
    """
    if not page_url.startswith("http"):
        raise DownloadError("Bitte eine gültige URL mit http/https angeben.")

    image_infos = extract_image_urls(page_url)
    if not image_infos:
        return {"count": 0, "folder": target_folder, "details": []}

    target = Path(target_folder).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    # Basisname für slugged
    parsed = urlparse(page_url)
    domain = parsed.netloc.replace(":", "_")
    path_slug = parsed.path.strip("/").replace("/", "_")
    base_slug = domain or "seite"
    if path_slug:
        base_slug += "_" + path_slug
    base_slug = sanitize_filename(base_slug)

    used_names: set[str] = set()
    downloaded = []
    errors = []

    for idx, (img_url, original_name) in enumerate(image_infos, start=1):
        try:
            if naming_scheme == "slugged":
                ext = os.path.splitext(original_name)[1] or ".jpg"
                filename = f"{base_slug}-{idx:03d}{ext}"
            else:
                filename = sanitize_filename(original_name) or "image.jpg"

            # Duplikate vermeiden
            candidate = filename
            counter = 1
            while candidate in used_names or (target / candidate).exists():
                stem, ext = os.path.splitext(filename)
                candidate = f"{stem}_{counter}{ext}"
                counter += 1

            used_names.add(candidate)

            resp = requests.get(img_url, timeout=20)
            resp.raise_for_status()

            dest_path = target / candidate
            with open(dest_path, "wb") as f:
                f.write(resp.content)

            downloaded.append(str(dest_path))
            time.sleep(0.05)  # Server nicht zu hart stressen

        except Exception as e:
            errors.append((img_url, str(e)))

    return {
        "count": len(downloaded),
        "folder": str(target),
        "downloaded": downloaded,
        "errors": errors,
        "total_found": len(image_infos),
    }
