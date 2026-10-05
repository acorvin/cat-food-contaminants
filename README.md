# Contaminants in cat food, 2026

Three pages that set out the figures published in the Clean Label Project's 2026 Cat Food Category Report: 100 cat foods from 62 brands, screened for more than 122 contaminants.

All three pages use the report's summary figures only. The Clean Label Project has not released results for individual products, so there is no product-level data here.

## Files

- `docs/index.html` is the explanatory page with charts and table views, published with GitHub Pages from `main` and `/docs`.
- `docs/study.html` is the scrolling dot study: a row of 100 dots for each substance, a log-scale dot plot for the multiples, rows of 100 dots for the shares and a panel on what the figures cannot show. It reflows to one column on phones.
- `docs/poster.html` is the overview, an interactive page that shows every figure on one screen. It states the main caveat under the headline, draws the detection counts as bars out of 100, groups the multiples by protein, format and across all products, and scales to fit the window with no scrolling. On a phone it switches to four tabs. A readout at the bottom gives each figure and where it was confirmed, and a data table button lists all 31 figures.
- `src/page.template.html`, `src/study.template.html` and `src/poster.template.html` (the overview) are the page sources. Edit copy and layout there.
- `data/cat-food-contaminants.csv` holds every figure the page uses, one row per figure, with the places each was confirmed.
- `scripts/build.py` checks the figures for consistency and writes `docs/index.html`, `docs/study.html`, `docs/poster.html` and `docs/data/`.
- `embed/snippet.html`, `embed/study-snippet.html` and `embed/poster-snippet.html` are the iframe snippets for embedding each page on another site. The overview snippet uses a 16:9 box and needs no height script.

## Rebuild

```
python3 scripts/build.py
```

The build stops if the format counts do not add up to 100, if the poultry and fish shares do not agree with the stated gap and ratio, or if a source code is not recognised.

## Source codes

| Code | Source |
|---|---|
| R | Clean Label Project, Cat Food Category Report (PDF) |
| W | Clean Label Project, Cat Food Study page |
| P | Clean Label Project press release |
| C | CNN or Scripps News coverage |
| N | Newsweek |

## Notes on the figures

- The standard behind "met the standard" is the Clean Label Project's own. It is set against the other products in the study, and the report says no regulatory limits apply.
- The 28x mercury multiple for fish-based wet foods appears on the study page and in the press release. In the report PDF it is a chart label and not in the running text.
- Mercury has no overall detection rate in the report text, so it appears only in the comparisons.
- Each product was tested from a single batch.
- In the study and the overview, each row of dots is a count of products and not a list, because the report does not say which products. Share rows draw a partial last dot for the fraction. The multiples sit on one log axis with an open dot at 1x for the group compared with; glyphosate is shown apart because it is an association, not a ratio.
- The glyphosate figure ("about 40% more for each added plant ingredient") is plotted as 1.4 times on the first page and labeled an association. The overview shows it as +40% in text, apart from the ratio chart.

Report: https://cleanlabelproject.org/wp-content/uploads/clean-label-project-cat-food-study-2026.pdf
Study page: https://cleanlabelproject.org/cat-food-study/
