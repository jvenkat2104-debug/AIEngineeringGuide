# Website publishing

The free Zensical build projects maintained files in `content/` and `downloads/` into ignored `tmp/web-docs/`. Do not edit the generated copy. Root planning documents and raw archives stay on GitHub rather than appearing in reader navigation.

## Build

Use Python 3.12 or later, create a virtual environment and install `requirements-site.txt`. Run:

```sh
python scripts/prepare_site.py
zensical build --clean
python scripts/add_legacy_redirects.py
```

Generated HTML is in `dist/site/`. Preview with a local static server or `zensical serve` after preparing the source. The checked-in `site/` directory contains authored styling and theme overrides, not generated output.

The site uses only the open-source Zensical package and standard GitHub Actions/GitHub Pages. Studio, Spark, paid runners, custom domains and paid APIs are not required.

The build workflow can be dispatched without deployment for artifact inspection. Deployment requires GitHub Pages configured with GitHub Actions as its build source. Keep the community-draft notice until named reviewers have actually reviewed content. Existing PDF downloads are original editions, not exports of all current website chapters.

## Deployment and local compatibility

Pushes to `main` build and deploy automatically. A manual run can set `deploy=false` for artifact inspection. Public website: https://jvenkat2104-debug.github.io/ . The first verified build used Linux/Python 3.12 and Zensical 0.1.1. Native Windows builds encountered a Zensical URL-parsing panic; the Linux workflow is the verified build route. Download the `site-preview` artifact to preview generated files locally with a static HTTP server.

## Account-site migration

The repository is `jvenkat2104-debug/jvenkat2104-debug.github.io`; the canonical site is https://jvenkat2104-debug.github.io/ . After building, `scripts/add_legacy_redirects.py` creates lightweight redirects for former `/AIEngineeringGuide/` HTML routes. They point to the corresponding root-site pages and preserve query strings and anchors when JavaScript is available. These are compatibility pages, not duplicate maintained content. The workspace folder may retain its original name.

## One-page printables

Edit `publishing/printables.json`, update the edition in `scripts/build_printables.py`, and run `python scripts/build_printables.py` with `requirements-printables.txt` installed. This generates the matching web pages and PDFs. Visually check all three one-page PDFs before committing the Markdown and `downloads/` copies. Local delivery copies go to ignored `output/pdf/`. CI regenerates the sheets before building the site.

The site projection maps the historical tools and industry-tour source folders to clean public URLs. Compatibility pages preserve both the former paths and the old `/AIEngineeringGuide/` prefix.
