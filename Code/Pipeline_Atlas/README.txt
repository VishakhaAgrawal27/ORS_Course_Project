HYDERABAD URBAN GROWTH ATLAS
============================
CA-MLR-GA Spatial Modeling | IIIT Hyderabad | 1990 to 2050

19 immersive interactive visualizations of a 30-year cellular automaton
simulation of Hyderabad's urban growth, calibrated against Landsat-classified
historical land cover.

QUICK START
-----------
Browsers block fetch() from file:// URLs, so you must run a local web server:

    cd hyderabad_atlas
    python3 -m http.server 8000

Then open http://localhost:8000/index.html in your browser.

CONTENTS
--------
index.html              Atlas index with 5 themed tabs and modal-iframe viewer
charts/                 19 immersive chart pages (one per visualization)
charts/_shared.css      Shared design tokens (dark cinematic theme)
data.json               Canonical data source (1.9 MB)
libs/                   Three.js, D3, Plotly (offline copies)
audit_report_v2.md      Numeric audit cross-checking every value displayed in
                        the atlas against canonical data.json. 100% pass rate.

CHARTS BY THEME
---------------
Time & Cadence         01 Growth Cadence Clock, 17 City Year by Year, 20 Bubble Race
Spatial Reveals        19 Skyline of Age, 10 Origins Map, 11 Sigmoid of Fate,
                       15 Six Periods of Flow, 09 Transition Matrix
Driver Mechanics       03 Driver Polarity Rose, 04 Correlation Network,
                       12 Driver Distributions
Scenario Sweep         05 Constellation, 07 Sensitivity Cathedral,
                       16 Similarity Chord, 18 Compactness Ridge,
                       13 Conservation vs Boom, 14 Agreement Field
Mechanism Diagnostics  02 Barren Paradox, 06 Quota Ribbon

AUTHORS
-------
Vishakha Agrawal, Goni Anagha, Gandlur Valli, Nunna Sri Abhinaya
Optical Remote Sensing, IIIT Hyderabad, 2026
