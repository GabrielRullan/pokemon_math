#!/usr/bin/env python3
"""
Descarga y cachea localmente (offline) los nombres/IDs de especies Pokémon
y sus artworks oficiales en PNG desde PokeAPI/sprites para todos los Pokémon
que aparecen en problemas_2..6_primaria.md.
"""

from __future__ import annotations

import json
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
IMG_DIR = ROOT_DIR / "html" / "assets" / "images"
OLD_IMG_DIR = Path(r"C:\Users\gabri\Documents\pokemon\assets\images")

# Compañeros por defecto para problemas que no nombran una especie concreta
COMPANION_DEFAULTS = {
    "pikachu": 25,
    "eevee": 133,
    "bulbasaur": 1,
    "charmander": 4,
    "squirtle": 7,
    "chansey": 113,
    "geodude": 74,
    "staryu": 120,
    "meowth": 52,
    "togepi": 175,
    "jigglypuff": 39,
    "snorlax": 143,
    "lucario": 448,
    "psyduck": 54,
    "piplup": 393,
    "gengar": 94,
}


def fetch_species_map() -> dict[str, int]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DATA_DIR / "pokemon_species.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    url = "https://pokeapi.co/api/v2/pokemon-species?limit=1025"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8"))
    species = {}
    for item in data["results"]:
        pid = int(item["url"].rstrip("/").split("/")[-1])
        species[item["name"]] = pid

    cache_path.write_text(json.dumps(species, ensure_ascii=False, indent=2), encoding="utf-8")
    return species


def collect_used_ids(species: dict[str, int]) -> dict[int, str]:
    used: dict[int, str] = {pid: name for name, pid in COMPANION_DEFAULTS.items()}
    all_text = "\n".join(
        (ROOT_DIR / f"problemas_{g}_primaria.md").read_text(encoding="utf-8").split("## Parte 2:")[0].lower()
        for g in (2, 3, 4, 5, 6)
        if (ROOT_DIR / f"problemas_{g}_primaria.md").exists()
    )

    for sname, pid in species.items():
        pat = r"\b" + re.escape(sname.replace("-", "[- ]?")) + r"\b"
        if re.search(pat, all_text):
            used[pid] = sname
    return used


def download_one(pid: int, name: str) -> tuple[int, str, str]:
    target = IMG_DIR / f"{pid}.png"
    if target.exists() and target.stat().st_size > 1000:
        return pid, name, "cached"

    # Reutilizar si existe en el proyecto antiguo por nombre
    old_file = OLD_IMG_DIR / f"{name.lower()}.png"
    if old_file.exists() and old_file.stat().st_size > 1000:
        shutil.copy2(old_file, target)
        return pid, name, "copied"

    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pid}.png"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            target.write_bytes(resp.read())
        return pid, name, "downloaded"
    except Exception as exc:
        return pid, name, f"error: {exc}"


def main() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    species = fetch_species_map()
    used = collect_used_ids(species)
    print(f"Especies a cachear: {len(used)}")

    stats = {"cached": 0, "copied": 0, "downloaded": 0, "error": 0}
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(download_one, pid, name) for pid, name in sorted(used.items())]
        for fut in as_completed(futures):
            pid, name, status = fut.result()
            if status in stats:
                stats[status] += 1
            else:
                stats["error"] += 1
                print(f"[WARN] #{pid} {name}: {status}")

    print("Resumen imágenes:", stats)


if __name__ == "__main__":
    main()
