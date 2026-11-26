# Capitol Misfits

[Open the gallery](https://daaronr.github.io/capitol-misfits/) or share the [Howard Nutlick card](https://daaronr.github.io/capitol-misfits/howard-nutlick/). The six-card political parody series has illustrated fronts, downloadable PNGs, and backs with made-up stats and linked biographical facts.

## Update the deck

Edit `cards.json` for card copy, facts and sources. The original illustrated panels are in `art/`. The layout and build script are in `build.py`. Edit `docs/gallery.css` or `docs/gallery.js` for style and interaction changes.

Run `python3 build.py` with Pillow installed. The image renderer uses the macOS supplemental Impact, Arial Bold and Courier New Bold fonts. Set `CARD_FONT_DIR` to point to a folder containing those fonts if needed. The resulting site in `docs/` is checked in and needs no build on the server.

Run `python3 -m http.server 8000 --directory docs` to preview. Open the gallery and a direct card page, flip a card in both directions and try saving its PNG. GitHub Pages publishes `main:/docs`. Check both links above against the live site after a push.

## Illustration prompts

The Codex built-in image generator made the six panels. Each prompt used this shared direction and the matching scene below.

> Create one full-bleed portrait 4:5 central trading-card ILLUSTRATION, image only, for Capitol Misfits, an original retro 1980s gross-out sticker-card parody of US politicians. Professional highly expressive painted editorial caricature, oversized head, strong action silhouette, punchy ink lines and detailed painterly colors, comically distorted perspective, crisp expressive face and high contrast, fine offset-print halftone grain in the background, visual humor suited for kids. Make the gag unmistakable at small size. Fill the whole frame with scene and keep key character and objects inside margins. Absolutely no text, border, lettering, card header, logo or watermark; real typesetting will be added separately.

- **Burn-ey Sanders.** Recognizable Bernie Sanders caricature with wild white hair, spectacles, oversized head, rumpled blue suit at a Senate lectern. He is fiercely filibustering a gigantic personified sun with a bored expression. Absurd cartoon sun scorch: one side of his face has smoky soot and exaggerated raised red and orange bumps like toasted marshmallow, corner of jacket charred, bowing microphone melting. No open wounds or realistic burns. Solar orange and shocking cerulean.
- **V.D. Jance.** Recognizable JD Vance caricature with dark beard and short brown hair, navy suit, startled expression, in a Capitol hallway. His worn briefcase bursts and sprays lurid fluorescent lime toy slime in looping arcs. He tries to plug it with a sock while a tiny office fan blows paperwork across the floor. Raspberry, green and electric azure.
- **Howard Nutlick.** A recognizable Howard Lutnick caricature, silver side-parted hair, rounded cheeks, confident smile, dark suit and turquoise tie, holds one gigantic split pistachio the size of his head with both hands. A cartoon tongue playfully taste-tests a visible bright green pistachio kernel in the split shell. A mound of small pistachios and a few salt crystals fly about. Wholesome food gag and cheeky eyebrows. Acid green and lilac with a coral accent.
- **Marco Rubble-O.** Recognizable Marco Rubio caricature, dark slicked hair, large eyebrows, oversized head and dress shirt and tie. A collapsed lectern has left him in a silly pile of cartoon rubble, a microphone perched absurdly on top, holding a single glass of water completely level while chunks of foam-looking stone bounce around. Lavender and copper with yellow accents.
- **Chuck Chummer.** Recognizable Chuck Schumer caricature, bald crown and gray fringe, spectacles low on the nose. On a tiny capsizing fishing skiff in an indoor Senate reflecting pool, he ladles a bucketful of cartoon rubber fish and pink sludge into the water, while a curious shark fin zigzags toward a gavel bobbing like a float. Aqua ink, orange and pink.
- **Ted Cruise.** Recognizable Ted Cruz caricature, dark full beard, short slick hair, arched eyebrows, deck shirt over a rumpled suit and socks with sandals, negotiating with a mutinous sea gull on a comically small inflatable cruise boat stranded in bright slushy snow. A wheelie suitcase is stuck in a drift beside him. Icy turquoise and blazing vacation pink with yellow.
