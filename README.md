# Diffusers GitHub Insights reproduction

CD61203 term project, roll number 26AI60R04.

The project reproduces the Contributors, Commits, Code frequency, and Top
committers charts from https://github.com/huggingface/diffusers using Matplotlib.
Reference screenshots and raw data are captured from GitHub, with acquisition
metadata retained to make the comparison reproducible.

`tmp-check/` is reserved for checkpoint files requested during the session.

## Deliverables

| Directory | Figure | Snapshot scope |
| --- | --- | --- |
| `fig1-contributors/` | Ten contributor small multiples | 9 Aug–8 Nov 2026 |
| `fig2-commits/` | Weekly commits, 52 green columns | 16 Nov 2025–8 Nov 2026 |
| `fig3-code-frequency/` | Additions and negative deletions | 233 weeks, May 2022–Nov 2026 |
| `fig4-top-committers/` | Pulse author counts, 15 green columns | Pulse period 5–12 Nov 2026 |

Every figure directory includes `raw_data.csv`, `plot.py`, `generated.png`,
`reference.png`, and `reference-metadata.json`. References are unmodified
screenshots of the matching GitHub chart region. Contributor figures show the
same first ten cards as the reference crop. The full 100-contributor response
is additionally exported to `fig1-contributors/all_contributors.csv`.

GitHub automatically groups the code-frequency weekly observations into 55
calendar-month sums at the captured viewport. Both weekly raw data and the
exact displayed monthly values are retained. Deletions remain negative.
The actual Top committers chart is under **Insights → Pulse**.

## Rebuild offline

Install the Python dependencies from `requirements.txt`, then run:

```sh
python reproduce.py
python tools/validate.py
```

Each `plot.py` also runs independently from any working directory. The four
plotting scripts read their own raw CSVs and use `tools/plot_style.py`.
`validation.json` records exact agreement for all 317 displayed values,
checked against the independent accessible point labels saved with the
reference captures. Weekly commit totals are also checked against daily sums.

Build the report using either:

```sh
pdflatex main.tex
pdflatex main.tex
```

or `tectonic main.tex`. The completed submission is `main.pdf`.

## Data provenance

All snapshots were acquired on **13 November 2026**. Source URLs, browser
viewport, capture time, labels, and point values are retained in each figure's
metadata. `data/*-data.json` contains the original GitHub chart responses;
`data/*-final.html` and `data/pulse-rendered.html` retain rendered source pages.
`tools/prepare_data.py` regenerates CSVs from these saved snapshots.
`tools/capture_references.py` records browser screenshots using Chrome and
Playwright; `tools/download_avatars.py` retrieves the matching public avatar
labels. These acquisition tools require network access, while plotting and
validation run entirely offline. The CSV date filters describe this fixed
snapshot; they must be updated deliberately if collecting a later period.

`tools/capture_top_committers.py` refreshes only the Pulse chart, its CSV,
rendered source, and metadata. It waits until every avatar label has loaded
and verifies that their author names match the chart's data points before
saving the reference. Validation checks those category labels as well as
the plotted values. Live counts can change between captures; regenerate
the plot and update any counts quoted in the report after refreshing.

Font rendering and interactive controls may differ; chart type, series,
numeric values, axis placement, date labels, and visible ranges follow the
captured references. The author-count chart retains avatar category labels,
with the corresponding full author names available in its CSV.
