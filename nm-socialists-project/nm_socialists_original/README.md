
# New Mexico Socialists – Netlify Site (V8 FULL, de-duplicated memes)

Changes from V7 FULL:

- **No duplicate memes**:
  - Only original PNGs from `/mnt/data` whose filenames do NOT start with `meme_` are used.
  - Exact binary duplicates are removed via SHA-256 hash checking.
  - Each source image becomes `assets/img/meme_#.png` used once in the gallery.

- Keeps everything else:
  - Interactive gallery (view/download/share/copy link).
  - Netlify Forms wired `join` form.
  - Resource links (Marx/Engels EN+ES, Libcom, PSL, Liberation News).

Deploy this folder as your Netlify site root and you should see a single instance of each meme.

Domain, email, and Facebook page baked in:

- Canonical / SEO domain: https://newmexicosocialists.com
- Facebook page: https://www.facebook.com/profile.php?id=61584102062292
- Contact email: NewMexicoSocialists@proton.me
