"""Rakentaa etusivun pelikortit ja julkaisulistan games.json-tiedostosta.

Käyttö:  python build_games.py [--today YYYY-MM-DD]
Kirjoittaa index.html:n merkkien väliin:
  <!-- GAMES:START --> ... <!-- GAMES:END -->        (Our games -kortit)
  <!-- RELEASES:START --> ... <!-- RELEASES:END -->  (About-osion julkaisulista, vanhin ensin)
Sivu pysyy staattisena HTML:nä (hakukoneet ja hitaat yhteydet), mutta pelejä ei tarvitse kirjoittaa käsin.
Uusi julkaisu näkyy NEW_DAYS päivää merkillä NEW, OUT NOW ja ensimmäisenä listassa.
"""
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEW_DAYS = 30
BADGE = '<img src="google-play-badge.png" alt="Get it on Google Play" class="badge" loading="lazy">'


def card(g, today):
    st = g["status"]
    rel = dt.date.fromisoformat(g["released"]) if g.get("released") else None
    is_new = st == "out" and rel is not None and (today - rel).days <= NEW_DAYS
    label, cls = {"out": ("NEW, OUT NOW" if is_new else "OUT NOW", " soon" if is_new else ""),
                  "test": ("CLOSED TEST OPEN", " test"), "soon": ("COMING SOON", " test")}[st]
    external = g["url"].startswith("http")
    attrs = ' target="_blank" rel="noopener"' if external else ""
    kind = "game" if st == "out" else "game upcoming join"
    cta = BADGE if st == "out" else f'<span class="join-cta">{html.escape(g.get("cta", "Learn more"))} &rarr;</span>'
    return (f'                    <a href="{html.escape(g["url"])}"{attrs} class="{kind}">\n'
            f'                        <div class="game-top">\n'
            f'                            <img src="{html.escape(g["icon"])}" alt="" class="game-icon" width="80" height="80" loading="lazy">\n'
            f'                            <div class="game-head">\n'
            f'                                <h3>{html.escape(g["name"])}</h3>\n'
            f'                                <span class="status{cls}">{label}</span>\n'
            f'                            </div>\n'
            f'                        </div>\n'
            f'                        <p>{html.escape(g["desc"])}</p>\n'
            f'                        {cta}\n'
            f'                    </a>\n'), is_new, rel


def sort_key(item):
    g, is_new, rel = item
    group = 0 if is_new else {"test": 1, "soon": 2}.get(g["status"], 3)
    return (group, -(rel.toordinal() if rel else 0))


def replace_block(text, name, body):
    pat = re.compile(rf"(<!-- {name}:START -->\n).*?([ \t]*<!-- {name}:END -->)", re.S)
    if not pat.search(text):
        sys.exit(f"index.html: merkit <!-- {name}:START/END --> puuttuvat")
    return pat.sub(lambda m: m.group(1) + body + m.group(2), text)


def main():
    today = dt.date.today()
    if "--today" in sys.argv:
        today = dt.date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
    games = json.loads((HERE / "games.json").read_text(encoding="utf-8"))["games"]
    items = sorted(((g,) + card(g, today)[1:] for g in games), key=sort_key)
    cards = "".join(card(g, today)[0] for g, _, _ in items)
    rels = sorted((g for g in games if g["status"] == "out" and g.get("released")), key=lambda g: g["released"])
    log = "".join(f'                        <li><time datetime="{g["released"][:7]}">{g["released"][:7].replace("-", ".")}</time>'
                  f'<span>{html.escape(g["name"])} on Google Play</span></li>\n' for g in rels)
    idx = HERE / "index.html"
    text = idx.read_text(encoding="utf-8")
    text = replace_block(text, "GAMES", cards)
    text = replace_block(text, "RELEASES", log)
    idx.write_text(text, encoding="utf-8", newline="\n")
    print(f"{len(games)} peliä, {len(rels)} julkaisua -> index.html ({today})")


if __name__ == "__main__":
    main()
