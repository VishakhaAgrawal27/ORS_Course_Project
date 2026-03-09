# Urban Expansion Analysis: Setup and Troubleshooting Guide

## Table of Contents

### Project Coordination

0. [Reference Material](#0-reference-material)
1. [Milestones Completed](#1-milestones-completed)
2. [Milestones and Tasks Remaining](#2-milestones-and-tasks-remaining)
3. [Task Volunteers](#3-task-volunteers)
4. [Action Plan and Deadlines](#4-action-plan-and-deadlines)
5. [Repository and Collaboration](#5-repository-and-collaboration)

### Technical Guide

6. [What is This Project?](#6-what-is-this-project)
7. [What is the Google Cloud Project?](#7-what-is-the-google-cloud-project)
8. [Do You Need Pre-existing Files?](#8-do-you-need-pre-existing-files)
9. [Project Initialization Explained](#9-project-initialization-explained)
10. [Step-by-Step Setup for New Users](#10-step-by-step-setup-for-new-users)
11. [Common Errors and Fixes](#11-common-errors-and-fixes)
12. [Parts of the Code You MUST Change](#12-parts-of-the-code-you-must-change)
13. [Google Drive and File Path Changes](#13-google-drive-and-file-path-changes)
14. [Troubleshooting Checklist](#14-troubleshooting-checklist)

---

# Part A: Project Coordination

## 0. Reference Material

Both are in the root of the repository:

- **Project Proposal** (with improvements from Dr. Kiran's guidance):
  [`CA_MLR_GA_Proposal_Imptoved_from_DrKirans_Guidance.pdf`](CA_MLR_GA_Proposal_Imptoved_from_DrKirans_Guidance.pdf)
- **Primary Reference Paper**:
  [`Reference_Paper.pdf`](Reference_Paper.pdf)

All team members should be familiar with both documents before picking up tasks.

---

## 1. Milestones Completed

> *To be filled in: list milestones from the project proposal that have been
> completed so far.*

<!-- Example format:
- [x] Milestone 1: GEE data acquisition and Landsat composite generation
  (1990-2024)
- [x] Milestone 2: Random Forest LULC classification with ESA WorldCover
  training labels
- [x] Milestone 3: Driver extraction (slope, elevation, population, distance
  to roads, distance to center, water exclusion)
- [x] Milestone 4: VIF analysis and MLR model fitting
- [x] Milestone 5: GA calibration (1990 to 2000) and CA simulation
- [x] Milestone 6: Multi-scenario analysis (19 scenarios)
- [x] Milestone 7: GeoTIFF export for GeoServer visualization
-->

---

## 2. Milestones and Tasks Remaining

> *To be filled in: list remaining milestones from the proposal, plus any
> critique or additional requirements raised by Dr. Kiran.*

<!-- Example format:
### From the Project Proposal
- [ ] Task A: ...
- [ ] Task B: ...

### From Dr. Kiran's Critique
- [ ] Critique 1: ...
- [ ] Critique 2: ...
-->

---

## 3. Task Volunteers

> *To be filled in: team members volunteering for each remaining task.*

<!-- Example format:
| Task | Volunteer(s) | Status |
|------|-------------|--------|
| Task A | Name1, Name2 | Not started |
| Task B | Name3 | In progress |
-->

---

## 4. Action Plan and Deadlines

> *To be filled in: timeline and deadlines for each task.*

<!-- Example format:
| Task | Deadline | Dependencies |
|------|----------|-------------|
| Task A | YYYY-MM-DD | None |
| Task B | YYYY-MM-DD | Depends on Task A |
-->

---

## 5. Repository and Collaboration

**Repo**: [https://github.com/VishakhaAgrawal27/ORS_Course_Project](https://github.com/VishakhaAgrawal27/ORS_Course_Project)

Invites have been sent to all team members' IIIT email addresses. **Please
accept the invite** to get push access.

### How to Contribute

1. Accept the GitHub invite sent to your IIIT email.
2. Clone the repo:
   ```bash
   git clone https://github.com/VishakhaAgrawal27/ORS_Course_Project.git
   ```
3. Create a branch for your task:
   ```bash
   git checkout -b feature/your-task-name
   ```
4. Push your changes and open a pull request for review.

### Repo Structure

```
ORS_Course_Project/
  CA_MLR_GA_Proposal_Imptoved_from_DrKirans_Guidance.pdf   # Project proposal
  Reference_Paper.pdf                                       # Primary reference paper
  ORS_Course_Project_Feb19.ipynb                            # Main notebook
  README.md                                                 # This file
  Mid_Eval/
    images.zip                                              # Figures used in mid-eval
    Mideval_PPT.pdf                                         # Mid-evaluation presentation (compiled)
    MidEval_PPT.tex                                         # Mid-evaluation presentation (LaTeX source)
```

---

# Part B: Technical Guide

## 6. What is This Project?

This notebook performs **urban expansion analysis for Hyderabad, India** using a
CA-MLR-GA (Cellular Automata, Multinomial Logistic Regression, Genetic Algorithm)
modeling pipeline. It uses satellite imagery from Landsat (1990 to 2024) via
Google Earth Engine (GEE) to classify land use and land cover (LULC) and then
predicts future urban growth (2030, 2040, 2050).

The pipeline has these major phases:

- **Phase 1**: Authenticate and initialize GEE, load Landsat imagery for
  multiple years (1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024).
- **Phase 2**: Random Forest classification using ESA WorldCover as training
  labels, validation with confusion matrices.
- **Phase 3**: Extract spatial drivers (slope, elevation, population density,
  distance to roads, distance to city center, water exclusion layer).
- **Phase 4**: VIF testing for multicollinearity, MLR analysis to identify
  dominant drivers of urban expansion.
- **Phase 5**: Genetic Algorithm optimization of CA parameters, then CA
  simulation for future prediction.
- **Phase 6**: Multi-scenario analysis (19 scenarios with varying parameters)
  and spatial metric computation.
- **Phase 7**: Export colored GeoTIFFs for visualization in GeoServer.

---

## 7. What is the Google Cloud Project?

### Short Answer

The "cloud project" in the code is a **Google Cloud Platform (GCP) project** that
acts as a billing and API container for Google Earth Engine requests.

### Detailed Explanation

Google Earth Engine (GEE) is a cloud-based geospatial processing platform.
Starting from late 2023, GEE requires every user to associate their usage with a
GCP project. This project is used for:

- Tracking your API usage and quotas
- Enabling the Earth Engine API under that project
- (Optionally) linking a billing account for heavy commercial usage; academic
  and research use is typically free

In the notebook, this line specifies the project:

```python
ee.Initialize(project='urban-growth-si')
```

The string `'urban-growth-si'` is the **project ID** of the original author's
GCP project. This is NOT a shared project. Every user needs their own project.

### The Error Explained

The error your friends are seeing:

```
EEException: Google Earth Engine API has not been used in project
urban-growth-si-489507 before or it is disabled.
```

This means one of two things:

1. They are trying to use the original author's project ID, which they do not
   have permission to access, OR
2. They created their own project but have not yet enabled the Earth Engine API
   on it.

---

## 8. Do You Need Pre-existing Files?

### For Initial Cells (Cells 0 through 14): NO

The first half of the notebook generates everything from scratch using GEE. All
satellite imagery, classification results, and driver layers are computed
on-the-fly from GEE datasets. No local files are needed.

### For Later Cells (Cells 23 onward): YES

Starting from the MLR/GA/CA phases, the notebook saves intermediate results to
Google Drive and loads them back in later cells. These files include:

| File | Created By | Used By |
|------|-----------|---------|
| `mlr_model_hyderabad.pkl` | Phase 2B (MLR cell) | Phase 3B, 3C, 5 |
| `ga_results_hyderabad.json` | Phase 3B (GA cell) | Phase 3C, 5 |
| `slope_export.tif` | GEE export cell | Phase 5 |
| `elevation_export.tif` | GEE export cell | Phase 5 |
| `population_2020_export.tif` | GEE export cell | Phase 5 |
| `distance_to_center_export.tif` | GEE export cell | Phase 5 |
| `lulc_2020_export.tif` | GEE export cell | Phase 5 |
| `exclusion_export.tif` | GEE export cell | Phase 5 |
| `distance_roads_raster.tif` | Roads cell (local) | Phase 5 |

**Key rule**: You must run cells sequentially. Skipping cells will cause
`NameError` or `FileNotFoundError` because variables and files from earlier cells
are needed by later ones.

---

## 9. Project Initialization Explained

The initialization happens across the first three cells of the notebook. Here is
what each does and why:

### Cell 0: Install Libraries

```python
!pip install earthengine-api --upgrade
!pip install --upgrade geemap
!pip install rasterio
```

This installs (or upgrades) the required Python packages in your Colab runtime.
`earthengine-api` is the Python client for GEE. `geemap` is a higher-level
wrapper for interactive map visualization. `rasterio` handles GeoTIFF
reading/writing locally.

### Cell 1: Authenticate

```python
ee.Authenticate()
```

This opens a browser-based OAuth2 flow. You sign in with the Google account that
has Earth Engine access. It generates a token stored in your Colab session. This
token proves to Google that you are authorized to use GEE.

**Important**: The Google account you authenticate with must have:

- An Earth Engine account (register at
  [signup.earthengine.google.com](https://signup.earthengine.google.com))
- A GCP project with the Earth Engine API enabled

### Cell 2: Initialize

```python
ee.Initialize(project='urban-growth-si')
```

This tells the GEE Python client which GCP project to bill API calls against.
All subsequent `ee.Image(...)`, `ee.ImageCollection(...)`, etc. calls go through
this project.

---

## 10. Step-by-Step Setup for New Users

Follow these steps carefully before running the notebook:

### Step 1: Register for Google Earth Engine

Go to [https://signup.earthengine.google.com](https://signup.earthengine.google.com)
and register using your Google account. If you have an institutional (.edu)
email linked to your Google account, use that. Approval is usually instant for
academic users.

### Step 2: Create a GCP Project

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com).
2. Sign in with the same Google account.
3. Click the project dropdown at the top of the page.
4. Click "New Project".
5. Give it a name (e.g., `my-urban-growth`). Note the **Project ID** that
   Google assigns (it may differ from the name).
6. Click "Create".

### Step 3: Enable the Earth Engine API

1. In the GCP Console, select your new project from the dropdown.
2. Go to "APIs & Services" then "Library".
3. Search for "Google Earth Engine API".
4. Click on it and press "Enable".
5. Wait 1 to 2 minutes for propagation.

### Step 4: Modify the Notebook

Change the project ID in Cell 2:

```python
# CHANGE THIS to your own project ID
ee.Initialize(project='YOUR-PROJECT-ID-HERE')
```

For example, if your GCP project ID is `my-urban-growth-2024`, write:

```python
ee.Initialize(project='my-urban-growth-2024')
```

### Step 5: Run the Notebook

1. Run Cell 0 (installs).
2. Run Cell 1 (authentication). Follow the OAuth flow in the popup window. Copy
   the authorization code back into Colab.
3. Run Cell 2 (initialization). If it prints the success message, you are set.

---

## 11. Common Errors and Fixes

### Error 1: "PERMISSION_DENIED" / "API has not been used in project"

```
EEException: Google Earth Engine API has not been used in project
urban-growth-si-489507 before or it is disabled.
```

**Cause**: You are using someone else's project ID, or the Earth Engine API is
not enabled on your own project.

**Fix**: Follow Steps 2 and 3 in Section 10 above. Then change the
`ee.Initialize(project=...)` line.

### Error 2: "Please authorize access to your Earth Engine account"

**Cause**: You skipped the authentication cell or the token expired.

**Fix**: Re-run `ee.Authenticate()` (Cell 1) and complete the OAuth flow again.

### Error 3: "No images found" or empty ImageCollection

**Cause**: The study area or date range does not intersect with available
Landsat data for that year/season. Could also happen if the study area geometry
is malformed.

**Fix**: Verify that `city_center_coords` and `study_area_radius` in Cell 3 are
correct. The default is `[78.4867, 17.3850]` with a 25 km radius around
Hyderabad.

### Error 4: NameError for `study_area`, `lulc_rf`, `images`, etc.

**Cause**: You ran a later cell without running earlier cells first. Variables
defined in earlier cells are not available.

**Fix**: Run all cells sequentially from the top. Use "Runtime > Run all" or
run each cell in order.

### Error 5: FileNotFoundError for .pkl, .json, or .tif files

**Cause**: The intermediate files have not been generated yet, or Google Drive
is not mounted.

**Fix**: Ensure Google Drive is mounted (`drive.mount('/content/drive')` in
Cell 23). Then run all preceding cells so that the pickle/JSON/GeoTIFF files
are created before the cells that load them.

### Error 6: GEE Export Tasks Never Complete

**Cause**: GEE export tasks (Cells 31 to 35) run asynchronously on Google's
servers. They can take 5 to 30 minutes depending on region size and server
load.

**Fix**: After starting exports, repeatedly run the task status check cell
until all tasks show `COMPLETED`. Only then proceed to cells that load those
exported GeoTIFFs.

### Error 7: "ModuleNotFoundError: No module named 'geemap'"

**Cause**: Cell 0 (library installation) was not run, or Colab runtime was
restarted after installation.

**Fix**: Re-run Cell 0. If the issue persists, restart the runtime
("Runtime > Restart runtime") and run Cell 0 again.

### Error 8: Google Drive Path Mismatch

**Cause**: The notebook writes to
`/content/drive/MyDrive/urban_growth_hyderabad` and
`/content/drive/MyDrive/hyderabad_drivers`. If your Drive structure is
different or you renamed folders, file paths will break.

**Fix**: See Section 13 below.

---

## 12. Parts of the Code You MUST Change

Here is a summary of every line that references user-specific or
environment-specific values:

### 12.1 Earth Engine Project ID (Cell 2) -- MANDATORY

```python
# Original:
ee.Initialize(project='urban-growth-si')

# Change to YOUR project:
ee.Initialize(project='YOUR-PROJECT-ID')
```

### 12.2 Study Area Coordinates (Cell 3) -- Only if Studying a Different City

```python
# Default is Hyderabad
city_center_coords = [78.4867, 17.3850]
```

If you are studying Hyderabad, leave this unchanged.

### 12.3 Google Drive Paths (Cells 23, 31-35, and later)

```python
# The code uses these paths:
project_folder = '/content/drive/MyDrive/urban_growth_hyderabad'
driver_folder  = '/content/drive/MyDrive/hyderabad_drivers'
```

These folders are created automatically. But if you have renamed or moved
them in Drive, update these strings.

### 12.4 GEE Export Folder Names (Cells 31-35)

```python
folder='hyderabad_drivers'
```

This is the folder name inside your Google Drive where GeoTIFFs are exported.
It must match the `driver_folder` path used later when loading files.

### 12.5 Multi-Scenario Paths (Cells 48 onward)

```python
SUBSET_LOCAL = '/content/subset'
PREDICTIONS_LOCAL = '/content/predictions'
PREDICTIONS_DRIVE = '/content/drive/MyDrive/task2_scenarios/predictions'
```

These are created automatically. No change needed unless you want a custom
location.

---

## 13. Google Drive and File Path Changes

The notebook saves and loads files from Google Drive in multiple places. Here
is the complete map of file I/O:

### Files Written to Google Drive

| Cell(s) | Path | Contents |
|---------|------|----------|
| 23 | `.../urban_growth_hyderabad/` | MLR model (.pkl), GA results (.json), CA outputs |
| 31-35 | `.../hyderabad_drivers/` | GeoTIFF exports of slope, elevation, population, distance layers |
| 51 | `.../task2_scenarios/predictions/` | Multi-scenario .npy prediction arrays |
| 53 | `.../task2_scenarios/metrics/` | Metrics CSV files |

### Files Read from Google Drive

| Cell(s) | Path | Contents |
|---------|------|----------|
| 29 | `.../urban_growth_hyderabad/mlr_model_hyderabad.pkl` | Trained MLR model |
| 30 | `.../urban_growth_hyderabad/ga_results_hyderabad.json` | GA-optimized parameters |
| 36 | `.../hyderabad_drivers/*.tif` | All exported driver GeoTIFFs |

**Rule**: If you change ANY write path, you must also change the corresponding
read path.

---

## 14. Troubleshooting Checklist

Before asking for help, go through this checklist:

- [ ] I have a Google Earth Engine account (registered at
      signup.earthengine.google.com)
- [ ] I have created my own GCP project at console.cloud.google.com
- [ ] I have enabled the "Google Earth Engine API" on my GCP project
- [ ] I have changed `ee.Initialize(project='...')` to my own project ID
- [ ] I ran `ee.Authenticate()` and completed the OAuth flow
- [ ] I am running cells in order from top to bottom
- [ ] Google Drive is mounted before cells that save/load files
- [ ] GEE export tasks have completed before I try to load the exported files
- [ ] I have not modified variable names or function signatures
- [ ] I have stable internet (GEE calls require connectivity)

---

## Quick Reference: Runtime Expectations

| Phase | Approximate Time | Notes |
|-------|-----------------|-------|
| Cell 0 (Install) | 1 to 2 min | One-time per session |
| Cell 1 (Auth) | 1 min | Interactive; follow the prompts |
| Cell 2 (Init) | Seconds | Must succeed before anything else |
| Cells 3-9 (Imagery) | 5 to 10 min | Loads 8 years of Landsat composites |
| Cell 11 (RF Classification) | 10 to 20 min | Training + classification for all years |
| Cells 16-21 (Drivers) | 5 to 15 min | Terrain, population, roads |
| Cells 31-35 (GEE Exports) | 10 to 30 min | Asynchronous; check task status |
| Cell 28 (GA) | 20 to 60 min | Depends on population size and generations |
| Cell 30 (CA Simulation) | 5 to 15 min | Full-resolution spatial simulation |
| Cells 48-56 (Scenarios) | 30 to 60 min | 19 scenarios, each takes a few minutes |
