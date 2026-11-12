# Website publishing

The free Zensical build projects maintained files in `content/` and `downloads/` into ignored `tmp/web-docs/`. Do not edit the generated copy. Root planning documents and raw archives stay on GitHub rather than appearing in reader navigation.

## Build

Use Python 3.12 or later, create a virtual environment and install `requirements-site.txt`. Run:

```sh
python scripts/prepare_site.py
zensical build --clean
```

Generated HTML is in `dist/site/`. Preview with a local static server or `zensical serve` after preparing the source. The checked-in `site/` directory contains authored styling and theme overrides, not generated output.

The site uses only the open-source Zensical package and standard GitHub Actions/GitHub Pages. Studio, Spark, paid runners, custom domains and paid APIs are not required.

The build workflow can be dispatched without deployment for artifact inspection. Deployment requires GitHub Pages configured with GitHub Actions as its build source. Keep the community-draft notice until named reviewers have actually reviewed content. Existing PDF downloads are original editions, not exports of all current website chapters.
