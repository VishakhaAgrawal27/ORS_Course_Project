# Cellular Automata Modeling of Urban Expansion in Hyderabad Metropolitan Area (2020-2050)

**Course:** Optical Remote Sensing (ORS), Spring 2026

**Team:**
Vishakha Agrawal (2023101040), Goni Anagha (2023101124), Gandlur Valli (2023102068), Nunna Sri Abhinaya (2023102071)

---

## Overview

This project develops a hybrid CA-MLR-GA model for spatially explicit urban growth prediction in Hyderabad, India. The model integrates Random Forest land use classification (1990-2020), Multinomial Logistic Regression for transition probability estimation, genetic algorithm parameter optimization, and quota-based cellular automata simulation to predict built-up area expansion from 456.76 km² (2020) to 1,006.91 km² (2050) at 30 m resolution over a 1,691 x 1,691 pixel grid (2.86 million cells).

### Key Results

| Metric | Value |
|---|---|
| RF Classification Accuracy | 80.12% (Kappa 0.735) |
| CA Calibration Accuracy (1990-2000) | 93.50% (Kappa 0.913) |
| CA Validation Accuracy (2000-2010) | 93.48% (Kappa 0.913) |
| Predicted Built-up 2050 | 1,006.91 km² (+120.4% from 2020) |
| Pseudo R² (MLR) | 0.226 |
| Study Area | 25 km radius, Hyderabad center (78.4867°E, 17.3850°N) |

### Interactive Atlas

An interactive 3D visualization atlas (19 charts) of the results is available at:
**https://web.iiit.ac.in/~vishakha.agrawal/viz/other/ors/**

---

## Repository Structure

```
ORS_Course_Project/
├── Code/
│   ├── ORS_Course_Project_April19.ipynb       # Main project notebook (Google Colab)
│   └── Pipeline_Atlas/                        # Interactive 3D visualization atlas
│       ├── index.html                         # Atlas entry point
│       ├── data.json                          # Extracted project data
│       ├── charts/                            # 19 interactive HTML charts
│       │   ├── 01_growth_cadence_clock.html
│       │   ├── 02_the_barren_paradox.html
│       │   ├── ...
│       │   └── 20_driver-space_bubble_race.html
│       └── libs/                              # D3, Plotly, Three.js
├── Report/
│   ├── Report.tex                             # LaTeX source (authoritative)
│   ├── Report.pdf                             # Compiled PDF (64 pages)
│   ├── Report.docx                            # Word document version
│   └── pic/                                   # 28 figures used in the report
├── End_Eval/
│   ├── Urban_Growth_EndPPT_V7.pptx            # Final presentation (43 slides)
│   ├── Urban_Growth_EndPPT_V7.pdf
│   └── figures/                               # Presentation figures
│       ├── core_methodology/                  # 28 core figures
│       └── parameter_analysis/                # 25 parameter analysis figures
├── Mid_Eval/
│   ├── MidEval_PPT.tex                        # Mid-evaluation LaTeX slides
│   └── Mideval_PPT.pdf
├── Ref_and_Proposal/
│   ├── CA_MLR_GA_Proposal_Improved_from_DrKirans_Guidance.pdf
│   └── CA_MLR_GA_Ref.pdf                      # Vani & Prasad (2022) reference paper
└── README.md
```

---

## Methodology

The project follows a five-phase pipeline:

**Phase 1: LULC Classification.** Random Forest classification of Landsat 5/7/8 imagery (1990-2020) trained on ESA WorldCover 2020 into four classes: Water, Vegetation, Barren, Built-up. Validated against ESA WorldCover 2021 (OA 80.12%, Kappa 0.735).

**Phase 2: Driver Extraction.** Five spatially explicit drivers standardized via z-score normalization: slope and elevation (SRTM DEM, 30 m), population density (JRC GHS-POP, 1990-2024), distance to roads (OpenStreetMap, 10,105 segments), and distance to city center (1990 built-up centroid). All drivers tested for multicollinearity (VIF range: 1.01-1.14).

**Phase 3: MLR and CA Calibration.** Multinomial Logistic Regression on 4,126 stratified sample points yields transition probabilities (Pseudo R² = 0.226). Genetic algorithm optimizes CA parameters: neighborhood weight (omega = 1.200), stochasticity (alpha = 0.050), iterations = 10. Sample-based calibration (1990-2000) and validation (2000-2010) achieve 93.50% and 93.48% accuracy.

**Phase 4: Full-Resolution Prediction.** Quota-based CA simulation at 30 m resolution on the complete 1,691 x 1,691 grid. Urban demand constrained to 2.67% annual growth rate (2010-2020 historical trend). Predictions generated for 2025, 2030, 2035, 2040, 2045, 2050.

**Phase 5: Sensitivity and Scenario Analysis.** 17 parameter scenarios testing neighborhood weight, stochasticity, and growth rate effects on spatial metrics (compactness index, edge density, patch count). Growth rate dominates spatial pattern (14-53x stronger than CA parameters).

---

## Data Sources

| Dataset | Source | Resolution | Role |
|---|---|---|---|
| Landsat 5 TM / 7 ETM+ / 8 OLI | USGS via GEE | 30 m | LULC classification |
| ESA WorldCover 2020 | ESA via GEE | 10 m | RF training reference |
| SRTM DEM | NASA via GEE | 30 m | Elevation and slope |
| GHS-POP | JRC via GEE | 100 m | Population density |
| OpenStreetMap | OSM Overpass API | Vector | Distance to roads |

All processing performed on Google Earth Engine and Google Colaboratory.

---

## Running the Notebook

### Prerequisites

- Google account with access to Google Earth Engine
- Google Colaboratory (free tier sufficient)

### Setup

1. Open `Code/ORS_Course_Project_April19.ipynb` in Google Colab
2. Authenticate with Google Earth Engine when prompted
3. Run cells sequentially (the notebook is self-contained)

The notebook exports all intermediate results (LULC maps, driver arrays, MLR coefficients, CA parameters, prediction grids) and generates all figures used in the report and presentation.

### Notes

- Full execution takes approximately 2-4 hours on Colab free tier
- The notebook uses `geemap`, `sklearn`, `scipy`, and standard scientific Python libraries
- All Landsat imagery is accessed directly from the GEE data catalog (no local downloads required)
- Study area center coordinates are set to 78.4867°E, 17.3850°N (Hyderabad) with a 25 km radius

---

## Report

The report is available in three formats in the `Report/` directory:

- `Report.tex` (LaTeX source, authoritative version)
- `Report.pdf` (compiled, 64 pages)
- `Report.docx` (Word document)

The report follows the stipulated format: Introduction (with literature survey, objectives, study area), Materials and Methods, Results and Discussion, Data and Code Availability, Acknowledgements, and References (25 cited works, all DOIs verified).

---

## References

The project methodology follows and extends:

> M. Vani and P. Rama Chandra Prasad, "Modelling urban expansion of a south-east Asian city, India: comparison between SLEUTH and a hybrid CA model," *Modeling Earth Systems and Environment*, vol. 8, pp. 1419-1431, 2022. https://doi.org/10.1007/s40808-021-01150-3

The full bibliography (25 references) is available in the report.

---

## Acknowledgements

We thank Dr. Kiran Chand Thumaty and Dr. P. Rama Chandra Prasad for their guidance and instruction throughout the course of this project. This work was done using open-source datasets and tools, with computational resources provided by Google Colaboratory.