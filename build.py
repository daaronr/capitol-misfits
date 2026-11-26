"""Render the static gallery and its ready-to-share card images."""

from html import escape
import json
from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
BASE = "https://daaronr.github.io/capitol-misfits/"
FONTS = Path(os.environ.get("CARD_FONT_DIR", "/System/Library/Fonts/Supplemental"))
INK = "#21172c"
PAPER = "#fff8e8"
WIDTH, HEIGHT = 750, 1050


def typeface(family, size):
    return ImageFont.truetype(str(FONTS / (family + ".ttf")), size)


def fit_type(draw, words, family, size, width):
    font = typeface(family, size)
    while draw.textlength(words, font=font) > width:
        size -= 1
        font = typeface(family, size)
    return font


def draw_front(card, number):
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((17, 17, WIDTH - 18, HEIGHT - 18), fill=INK)
    draw.rectangle((23, 23, WIDTH - 24, HEIGHT - 24), fill=card["color"])
    source = Image.open(ROOT / "art" / f'{card["id"]}.webp')
    art = ImageOps.fit(source.convert("RGB"), (692, 788), Image.Resampling.LANCZOS)
    image.paste(art, (29, 91))
    draw.rectangle((23, 84, WIDTH - 24, 90), fill=INK)
    draw.rectangle((23, 879, WIDTH - 24, 885), fill=INK)
    mono = typeface("Courier New Bold", 30)
    draw.text((40, 55), "CAPITOL MISFITS", font=mono, fill=INK, anchor="lm")
    draw.text((710, 55), f"NO. {number:02}", font=mono, fill=INK, anchor="rm")
    words = card["name"].upper()
    title = fit_type(draw, words, "Impact", 78, WIDTH - 80)
    draw.text((WIDTH // 2, 943), words, fill=INK, font=title, anchor="mm")
    tagline = typeface("Arial Bold", 24)
    draw.text((WIDTH // 2, 1003), card["tagline"], fill=INK, font=tagline, anchor="mm")
    image.save(ASSETS / f'{card["id"]}.png', optimize=True)
    image.save(ASSETS / f'{card["id"]}.webp', quality=91, method=6)


def draw_social(card, slug, title_lines, tagline, color):
    preview = Image.new("RGB", (1200, 630), color)
    draw = ImageDraw.Draw(preview)
    for x in range(17, 1200, 15):
        for y in range(15, 630, 15):
            draw.ellipse((x, y, x + 2, y + 2), fill="#a58dc8")
    draw.rectangle((20, 20, 1179, 609), outline=INK, width=3)
    cover = Image.open(ASSETS / f'{card["id"]}.png')
    cover.thumbnail((375, 495), Image.Resampling.LANCZOS)
    x, y = 990 - cover.width // 2, (630 - cover.height) // 2
    draw.rectangle((x + 10, y + 10, x + cover.width + 10, y + cover.height + 10), fill=INK)
    preview.paste(cover, (x, y))
    draw.rectangle((x, y, x + cover.width, y + cover.height), outline=INK, width=3)
    draw.text((75, 124), "CAPITOL MISFITS / SERIES ONE", fill=INK, font=typeface("Courier New Bold", 28))
    for index, title in enumerate(title_lines):
        font = fit_type(draw, title, "Impact", 128, 680)
        draw.text((68, 176 + 114 * index), title, fill=INK, font=font, anchor="lt")
    draw.text((74, 455), tagline, fill=INK, font=typeface("Arial Bold", 32))
    preview.save(ASSETS / f'{slug}-social.jpg', quality=92, optimize=True)


def shell(title, description, suffix, social, social_alt, prefix, body):
    e = escape
    url = BASE + suffix
    poster = BASE + "assets/" + social + "-social.jpg"
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Capitol Misfits">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:image" content="{poster}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(social_alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="{prefix}gallery.css">
  <script src="{prefix}gallery.js" defer></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="top">
    <div class="wrap">
      <a class="wordmark" href="{prefix or './'}">Capitol Misfits</a>
      <nav aria-label="Main">
        <a href="{prefix}#deck">All cards</a>
        <a href="{prefix}#next">More ideas</a>
      </nav>
    </div>
  </header>
  {body}
  <footer class="footer">
    <div class="wrap">
      <span>Independent political parody · AI-generated illustrations</span>
      <a href="https://github.com/daaronr/capitol-misfits">GitHub source</a>
    </div>
  </footer>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def render_card(card, number, single=False):
    e = escape
    cid, name = card["id"], e(card["name"])
    prefix = "../" if single else ""
    asset = f"{prefix}assets/{cid}"
    route = "./" if single else cid + "/"
    title = "" if single else f'<h3 id="{cid}-name">{name}</h3>'
    label = "page-title" if single else cid + "-name"
    stats = "".join(f'<div><dt>{e(key)}</dt><dd>{e(value)}</dd></div>' for key, value in card["stats"])
    facts = "".join(f"<li>{e(fact)}</li>" for fact in card["facts"])
    sources = " · ".join(f'<a href="{e(url)}">{e(text)}</a>' for text, url in card["sources"])
    credit = ""
    if "credit" in card:
        text, url = card["credit"]
        credit = f'<p class="credit"><a href="{e(url)}">{e(text)}</a>.</p>'
    page = "" if single else f'<a href="{route}" aria-label="Open {name} card page">Card page</a>'
    loading = "eager" if single else "lazy"
    return f"""
    <article class="card" id="{cid}" data-card aria-labelledby="{label}" style="--accent:{card['color']};--back-paper:{card['paper']}">
      <img class="card-face" data-front src="{asset}.webp" width="{WIDTH}" height="{HEIGHT}" loading="{loading}" alt="{e(card['alt'])} Card text reads {name}, {e(card['tagline'])}.">
      <div class="card-back" id="{cid}-back" data-back>
        <p class="back-series"><span>Capitol Misfits</span> <span>No. {number:02}</span></p>
        <p class="back-title">{name}</p>
        <p class="back-blurb">{e(card['blurb'])}</p>
        <p class="stat-label">Made-up stats</p>
        <dl class="stat-list">{stats}</dl>
        <section class="facts" aria-labelledby="{cid}-facts">
          <h4 id="{cid}-facts">Real facts about {e(card['person'])}</h4>
          <ul>{facts}</ul>
          <p>{sources}</p>
        </section>
        {credit}
      </div>
      {title}
      <div class="card-tools">
        <button class="flip" data-flip type="button" aria-expanded="false" aria-controls="{cid}-back" hidden>Flip card</button>
        {page}
        <a href="{asset}.png" download aria-label="Download {name} card as PNG">Save PNG</a>
        <button class="data-copy" data-copy="{route}" type="button" aria-label="Copy link to {name}" hidden>Copy link</button>
        <span class="status" role="status"></span>
      </div>
    </article>
    """


def write_site(cards):
    fronts = [render_card(card, i) for i, card in enumerate(cards, 1)]
    gallery = "\n".join(fronts[:3])
    bonus = "\n".join(fronts[3:])
    body = f"""
  <main id="main">
    <section class="hero">
      <div class="wrap hero-inner">
        <div>
          <p class="eyebrow">Series one · Political parody</p>
          <h1>Capitol <span>Misfits</span></h1>
          <p class="lede">Six gross-out trading cards from the messiest place in Washington.</p>
          <a class="action" href="#deck">Browse the cards ↓</a>
        </div>
        <a class="hero-feature" href="howard-nutlick/" aria-label="Open the Howard Nutlick card">
          <img src="assets/howard-nutlick.webp" width="{WIDTH}" height="{HEIGHT}" alt="Howard Nutlick and his giant pistachio">
        </a>
      </div>
    </section>
    <section id="deck" class="wrap gallery">
      <header class="section-head">
        <h2>Series one</h2>
        <p>Flip each card for made-up stats and real facts.</p>
      </header>
      <div class="deck">{gallery}</div>
      <section class="bonus" aria-labelledby="bonus-title">
        <header class="section-head">
          <h2 id="bonus-title">Bonus sheet</h2>
        </header>
        <div class="deck">{bonus}</div>
      </section>
    </section>
    <section id="next" class="wrap next">
      <h2>Ideas for the next pack</h2>
      <ul>
        <li><strong>AOC-to-pus</strong> Eight arms, nine committees. One tentacle has to chair two hearings.</li>
        <li><strong>Elizabeth Warren Piece</strong> She slices up a giant blueberry pie chart. One guy gets 99 percent and everyone else gets a fork.</li>
        <li><strong>Donald Trum-Pet</strong> He blows a gold trumpet so loud his comb-over turns into sheet music.</li>
        <li><strong>Hakeem Jeffreeze</strong> He freezes the House floor. A clerk skates by with a stack of bills.</li>
        <li><strong>Pete Butti-Jets</strong> He straps a jet engine to a city bus. The next stop is technically the moon.</li>
        <li><strong>Gavin News-slime</strong> A press conference goes swimmingly until a tidal wave of hair gel takes the podium.</li>
        <li><strong>Mitch McTurtle</strong> He retreats into his shell and files a motion to keep the shell in session.</li>
        <li><strong>Kristi Gnome</strong> A lawn gnome plants herself at a press briefing. The sprinklers take the first question.</li>
      </ul>
    </section>
  </main>
"""
    (DOCS / "index.html").write_text(shell(
        "Capitol Misfits", "Six gross-out political trading cards. Flip for made-up stats and sourced facts.",
        "", "gallery", "Capitol Misfits trading cards featuring Howard Nutlick and a giant pistachio.", "", body
    ), encoding="utf-8")
    for number, card in enumerate(cards, 1):
        e = escape
        credit = ""
        if "credit" in card:
            text, url = card["credit"]
            credit = f'<p><a href="{e(url)}">{e(text)}</a>.</p>'
        body = f"""
  <main id="main" class="wrap single">
    <div class="single-copy">
      <p class="eyebrow">Series one · Card {number:02}</p>
      <h1 id="page-title">{e(card["name"])}</h1>
      <p class="lede">{e(card["tagline"])}. {e(card["blurb"])}</p>
      {credit}
    </div>
    {render_card(card, number, single=True)}
  </main>
"""
        page = DOCS / card["id"]
        page.mkdir(exist_ok=True)
        (page / "index.html").write_text(shell(
            card["name"] + " | Capitol Misfits", card["tagline"] + ". " + card["blurb"],
            card["id"] + "/", card["id"], card["alt"], "../", body
        ), encoding="utf-8")


def main():
    cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
    ASSETS.mkdir(parents=True, exist_ok=True)
    for number, card in enumerate(cards, 1):
        draw_front(card, number)
        words = card["name"].upper().split(" ", 1)
        draw_social(card, card["id"], words, card["tagline"], card["paper"])
    featured = next(card for card in cards if card["id"] == "howard-nutlick")
    draw_social(featured, "gallery", ["CAPITOL", "MISFITS"], "Six gross-out trading cards", "#e6d7ff")
    write_site(cards)


if __name__ == "__main__":
    main()
