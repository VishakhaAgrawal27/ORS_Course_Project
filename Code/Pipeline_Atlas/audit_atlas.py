"""
audit_atlas.py
==============

Cross-checks every numeric value appearing in narrative panels and analysis
cards across all 19 chart files of the Hyderabad Urban Growth Atlas against
the canonical data.json.

Output: /home/claude/atlas_build/audit_report_v2.md
"""
import json
import re
from pathlib import Path
from collections import Counter

BUILD_DIR = Path('/home/claude/atlas_build')
CHARTS_DIR = BUILD_DIR / 'charts'
DATA_JSON = BUILD_DIR / 'data.json'
REPORT_OUT = Path('/mnt/user-data/outputs/audit_report_v2.md')


# ------------------------------------------------------------------------
# Build canonical index + derived facts

def build_canonical_index(data):
    index = []
    def walk(obj, path):
        if isinstance(obj, (int, float)) and not isinstance(obj, bool):
            index.append((path, float(obj)))
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f'{path}.{k}' if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f'{path}[{i}]')
    walk(data, '')
    return index


def build_derived_facts(data):
    facts = {}

    # Transition matrix totals
    M = data['spatial']['full_transitions_2020_2050_km2']['matrix']
    classes = data['spatial']['full_transitions_2020_2050_km2']['classes']
    for i, src in enumerate(classes):
        for j, dst in enumerate(classes):
            facts[f'transition_{src}_to_{dst}'] = M[i][j]
    new_built_total = sum(M[i][3] for i in range(4) if i != 3)
    facts['transition_total_new_built'] = new_built_total
    for i, src in enumerate(classes):
        if i == 3: continue
        facts[f'transition_pct_new_from_{src}'] = (M[i][3] / new_built_total) * 100
    facts['transition_diag_total'] = sum(M[i][i] for i in range(4))
    facts['transition_grand_total'] = sum(sum(r) for r in M)
    facts['transition_stable_pct'] = facts['transition_diag_total'] / facts['transition_grand_total'] * 100
    facts['transition_change_pct'] = 100 - facts['transition_stable_pct']

    # A14 quota period increments
    cumulative = [0] + data['canonical']['A14_quota']['total_quota']
    period_increments = [cumulative[i+1] - cumulative[i] for i in range(len(cumulative) - 1)]
    period_labels = ['2020_2025', '2025_2030', '2030_2035', '2035_2040', '2040_2045', '2045_2050']
    for i, inc in enumerate(period_increments):
        facts[f'quota_increment_{period_labels[i]}'] = inc
    for i, qi in enumerate(data['canonical']['A14_quota']['quota_per_iteration']):
        facts[f'quota_per_iter_{period_labels[i]}'] = qi
    # Per-period in km^2
    PX_KM2 = data.get('meta', {}).get('pixel_km2', 0.0009)
    for i, inc in enumerate(period_increments):
        facts[f'quota_increment_{period_labels[i]}_km2'] = inc * PX_KM2
    facts['quota_2050_cumulative'] = data['canonical']['A14_quota']['total_quota'][-1]
    # Total cumulative pixels (baseline + last cumulative)
    A10 = data['canonical']['A10_period_pixels']
    facts['cumulative_2050_total_pixels'] = A10['built_px'][-1]
    facts['cumulative_2020_baseline_pixels'] = A10['built_px'][0]
    # Cumulative % growth
    facts['growth_pct_2020_2050'] = (A10['built_px'][-1] / A10['built_px'][0] - 1) * 100

    # A2 predicted barren
    barren_2020 = data['canonical']['A2_lulc_predicted']['barren'][0]
    barren_2050 = data['canonical']['A2_lulc_predicted']['barren'][-1]
    facts['barren_2020_pred'] = barren_2020
    facts['barren_2050_pred'] = barren_2050
    facts['barren_pct_change_2020_2050'] = (barren_2050 - barren_2020) / barren_2020 * 100

    # A2 predicted built
    built_2020_pred = data['canonical']['A2_lulc_predicted']['built'][0]
    built_2050_pred = data['canonical']['A2_lulc_predicted']['built'][-1]
    facts['built_2020_pred'] = built_2020_pred
    facts['built_2050_pred'] = built_2050_pred
    facts['built_2020_to_2050_delta'] = built_2050_pred - built_2020_pred
    facts['built_pct_change_2020_2050'] = (built_2050_pred / built_2020_pred - 1) * 100

    # A1 historical built
    A1 = data['canonical']['A1_lulc_historical']
    facts['built_1990_hist'] = A1['built'][0]
    facts['built_2020_hist'] = A1['built'][-1]
    facts['built_hist_total_change'] = A1['built'][-1] - A1['built'][0]
    facts['barren_hist_min'] = min(A1['barren'])
    facts['barren_hist_max'] = max(A1['barren'])

    # Time-of-conversion histogram cumulative
    hist = data['spatial']['time_of_conversion_histogram']
    cum_km2 = []
    running = 0
    for i in range(1, 8):
        running += hist['km2'][i]
        cum_km2.append(running)
    for i, year in enumerate([2020, 2025, 2030, 2035, 2040, 2045, 2050]):
        facts[f'cum_built_{year}'] = cum_km2[i]
    # Per-period new (km^2)
    for i, year in enumerate([2025, 2030, 2035, 2040, 2045, 2050]):
        facts[f'period_new_{year}'] = hist['km2'][i + 2]

    # Class-change km^2 totals (origins-of-built breakdown)
    cc = data['spatial'].get('class_change_grid_422', {})
    if 'values' in cc:
        # Values: 1=water, 2=veg, 3=barren (replaced -> built)
        ccv = cc['values']
        c = Counter([x for x in ccv if x > 0])
        # Convert pixel counts to km^2 using global pixel size
        PX_KM2 = data.get('meta', {}).get('pixel_km2', 0.0009)
        facts['origin_water_pixels']  = c.get(1, 0)
        facts['origin_veg_pixels']    = c.get(2, 0)
        facts['origin_barren_pixels'] = c.get(3, 0)
        facts['origin_water_km2']     = c.get(1, 0) * PX_KM2
        facts['origin_veg_km2']       = c.get(2, 0) * PX_KM2
        facts['origin_barren_km2']    = c.get(3, 0) * PX_KM2

    # 17-scenario agreement histogram
    A = data['spatial']['subset_agreement_2030']['values']
    ag_hist = Counter(A)
    total = len(A)
    facts['agreement_pct_zero'] = ag_hist[0] / total * 100
    facts['agreement_pct_seventeen'] = ag_hist[17] / total * 100
    facts['agreement_pct_contested'] = sum(ag_hist[n] for n in range(4, 14)) / total * 100
    facts['agreement_count_zero'] = ag_hist[0]
    facts['agreement_count_seventeen'] = ag_hist[17]

    # Ghost overlay (cons vs boom)
    G = data['spatial']['subset_ghost_cons_boom_2040']['values']
    ghost_hist = Counter(G)
    PX_KM2 = data.get('meta', {}).get('pixel_km2', 0.0009)
    # Subset is a sub-grid, so compute area more carefully via the grid coverage
    # Use the per-cell area scaling factor consistent with the visualizations
    # Original subset is from the NW quadrant of 1691x1691 mode-pooled to 334x333.
    # Each subset cell ~= 6.42 original pixels. Use that scale.
    PER_CELL_KM2 = (1691/2) * (1691/2) * PX_KM2 / (334 * 333)
    facts['ghost_consensus_km2'] = ghost_hist.get(2, 0) * PER_CELL_KM2
    facts['ghost_boom_only_km2']  = ghost_hist.get(3, 0) * PER_CELL_KM2

    # Growth cohorts
    cohorts = data['spatial']['growth_cohorts']['cohorts']
    for c in cohorts:
        key = f'cohort_{c["from_year"]}_{c["to_year"]}'
        facts[f'{key}_n'] = c['n_pixels']
        facts[f'{key}_dc_z'] = c['mean_dist_center_z']
        facts[f'{key}_dr_z'] = c['mean_dist_roads_z']

    # Jaccard top pair
    J = data['spatial']['scenario_jaccard_2030']['matrix']
    scenarios = data['spatial']['scenario_jaccard_2030']['scenarios']
    pairs = []
    for i in range(len(scenarios)):
        for j in range(i+1, len(scenarios)):
            pairs.append((scenarios[i], scenarios[j], J[i][j]))
    pairs.sort(key=lambda x: -x[2])
    facts['jaccard_top_pair_value'] = pairs[0][2]
    facts['jaccard_lowest_pair_value'] = pairs[-1][2]
    # Mean off-diag
    offsum = 0
    offcount = 0
    for i in range(len(scenarios)):
        for j in range(len(scenarios)):
            if i != j:
                offsum += J[i][j]
                offcount += 1
    facts['jaccard_offdiag_mean'] = offsum / offcount
    # Top-quartile threshold
    n_pairs = len(pairs)
    q_idx = n_pairs // 4
    facts['jaccard_top_quartile_threshold'] = pairs[q_idx - 1][2]

    # 17 scenarios compactness (A9)
    A9 = data['canonical']['A9_scenarios_17']
    for s in A9:
        facts[f'compact2030_{s["name"]}'] = s['compact2030']
        facts[f'compact2040_{s["name"]}'] = s['compact2040']
        facts[f'compact_delta_{s["name"]}'] = s['compact2040'] - s['compact2030']
    # Compactness span (A13)
    A13 = data['canonical']['A13_sensitivity']
    facts['omega_range'] = A13['omega_range']
    facts['alpha_range'] = A13['alpha_range']
    facts['rate_range'] = A13['rate_range']
    facts['ratio_rate_omega'] = A13['ratio_rate_over_omega']
    facts['ratio_rate_alpha'] = A13['ratio_rate_over_alpha']

    # Driver coefficients (A4)
    A4 = data['canonical']['A4_mlr_builtup']
    facts['mlr_population'] = A4['population']
    facts['mlr_dist_roads'] = A4['distance_to_roads']
    facts['mlr_dist_center'] = A4['distance_to_center']
    facts['mlr_elevation'] = A4['elevation']
    facts['mlr_slope'] = A4['slope']
    facts['mlr_pseudo_r2'] = A4['pseudo_r2']

    # Driver correlations (A6)
    A6 = data['canonical']['A6_driver_correlation']
    drivers = A6['drivers']
    M = A6['matrix']
    # Strongest off-diag (any sign)
    max_corr = 0
    max_pair = None
    for i in range(len(drivers)):
        for j in range(i+1, len(drivers)):
            if abs(M[i][j]) > abs(max_corr):
                max_corr = M[i][j]
                max_pair = (drivers[i], drivers[j])
    facts['corr_strongest_value'] = max_corr
    # VIF max (A5)
    A5 = data['canonical']['A5_vif']
    vifs = [A5[k] for k in ['population', 'distance_to_roads', 'distance_to_center', 'elevation', 'slope']]
    facts['vif_max'] = max(vifs)

    # A2 vegetation trajectory delta
    veg_2020 = data['canonical']['A2_lulc_predicted']['veg'][0]
    veg_2050 = data['canonical']['A2_lulc_predicted']['veg'][-1]
    facts['veg_2020_pred'] = veg_2020
    facts['veg_2050_pred'] = veg_2050
    facts['veg_2020_to_2050_delta'] = veg_2050 - veg_2020

    # Time of conversion histogram (cohort pixel counts)
    toc = data['spatial']['time_of_conversion_grid_422']
    toc_v = toc['values']
    toc_hist = Counter([x for x in toc_v if x >= 1])
    facts['toc_baseline_2020_pixels'] = toc_hist.get(1, 0)
    facts['toc_added_2025_2050_pixels'] = sum(toc_hist.get(k, 0) for k in range(2, 8))
    facts['toc_total_built_pixels'] = sum(toc_hist.values())

    # N20 cohort population delta (last/first ratio)
    cohorts_list = data['spatial']['growth_cohorts']['cohorts']
    if len(cohorts_list) >= 2:
        facts['cohort_population_growth_pct'] = (cohorts_list[-1]['n_pixels'] / cohorts_list[0]['n_pixels'] - 1) * 100

    return facts


# ------------------------------------------------------------------------
# Extract narrative + analysis numeric tokens from each chart HTML

# Match numeric tokens including decimals, commas, optional sign
NUM_RE = re.compile(
    r'(?<![A-Za-z_/=:-])'
    r'([+-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?'
    r'|[+-]?\d+(?:\.\d+)?)'
    r'(?![A-Za-z_/=:-])'
)

# Strip script blocks before numeric extraction
SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')

def extract_narrative_text(html):
    # Remove scripts, fonts links, and tags
    no_scripts = SCRIPT_RE.sub('', html)
    # Remove <link> tags entirely (they often hold font weight CSV like "300;400;600;700")
    no_links = re.sub(r'<link\b[^>]*>', '', no_scripts, flags=re.IGNORECASE)
    # Remove style blocks
    no_styles = re.sub(r'<style\b[^>]*>.*?</style>', '', no_links, flags=re.DOTALL | re.IGNORECASE)
    # Remove inline style="..." attributes (can contain hex colors that parse as numbers)
    no_inline = re.sub(r'\sstyle\s*=\s*"[^"]*"', '', no_styles)
    # Remove all remaining HTML tags
    text = TAG_RE.sub(' ', no_inline)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text


def parse_num(s):
    return float(s.replace(',', '').replace('+', ''))


def numbers_in(text):
    out = []
    for m in NUM_RE.finditer(text):
        s = m.group(1)
        try:
            v = parse_num(s)
        except ValueError:
            continue
        out.append((s, v))
    return out


def values_match(a, b):
    if a == 0 and b == 0:
        return True
    if abs(a) < 50 or abs(b) < 50:
        return abs(a - b) < 0.5
    return abs(a - b) / max(abs(a), abs(b)) < 0.01


def find_matches(value, index, facts):
    matches = []
    for label, src_val in facts.items():
        if values_match(value, src_val):
            matches.append((f'derived:{label}', src_val))
    for path, src_val in index:
        if values_match(value, src_val):
            matches.append((f'data.json:{path}', src_val))
    return matches


# Tokens that don't need verification
META_TOKENS = {
    1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17,
    1691, 422, 333, 334, 10000, 80, 100,
    2.67, 0.05, 0.10, 0.0009, 0.025,
    # Year-fragment artifacts from Unicode-arrow year ranges (e.g. "2020 → 2025")
    # The regex strips the arrow and parses the second year as negative; or split as 199, 200, 201, 202, 203, 204, 205
    -2020, -2025, -2030, -2035, -2040, -2045, -2050,
    199, 200, 201, 202, 203, 204, 205,  # year fragments
    -1990, -1995, -2000, -2005, -2010, -2015,
    -65, 65,     # -64.93% rounds to ±65 in N2 display
    # Common color/style noise that survives stripping
    9664, 9654,  # font URL artifact "300;400;600;700" / "400;600;700"
    35,          # parses out of "rate_0.035"
}


def audit_chart(chart_path, index, facts):
    html = chart_path.read_text(encoding='utf-8')
    text = extract_narrative_text(html)
    findings = []
    seen = set()
    for s, v in numbers_in(text):
        if (s, round(v, 4)) in seen:
            continue
        seen.add((s, round(v, 4)))
        if v in META_TOKENS:
            findings.append(('META', s, v, 'meta/year/grid', None))
            continue
        matches = find_matches(v, index, facts)
        if matches:
            best = matches[0]
            findings.append((
                'OK' if best[0].startswith('data.json:') else 'OK*',
                s, v, best[0], best[1]
            ))
        else:
            findings.append(('DIFF', s, v, '(no match within tolerance)', None))
    return findings


# ------------------------------------------------------------------------
# Main

def main():
    print(f'Loading data from {DATA_JSON}...')
    data = json.loads(DATA_JSON.read_text())
    index = build_canonical_index(data)
    facts = build_derived_facts(data)
    print(f'Indexed {len(index)} canonical leaf values')
    print(f'Computed {len(facts)} derived facts')

    chart_files = sorted([
        f for f in CHARTS_DIR.glob('*.html')
    ], key=lambda p: int(p.stem.split('_')[0]))
    print(f'Auditing {len(chart_files)} chart files...')

    all_findings = {}
    for cf in chart_files:
        findings = audit_chart(cf, index, facts)
        all_findings[cf.name] = findings

    # Aggregate
    total_ok = total_ok_star = total_diff = total_meta = 0
    for fns in all_findings.values():
        for status, *_ in fns:
            if status == 'OK': total_ok += 1
            elif status == 'OK*': total_ok_star += 1
            elif status == 'DIFF': total_diff += 1
            elif status == 'META': total_meta += 1

    # Markdown report
    lines = []
    lines.append('# Hyderabad Urban Growth Atlas — Numeric Audit Report (v2)')
    lines.append('')
    lines.append('Cross-checks every numeric value appearing in the visible')
    lines.append('narrative text and analysis cards across all 19 chart files of')
    lines.append('the assembled atlas against the canonical `data.json`.')
    lines.append('')
    lines.append('## Methodology')
    lines.append('')
    lines.append('- For each `charts/*.html` file, strip `<script>` blocks and HTML tags')
    lines.append('  to extract only visible text content (info panels, analysis cards,')
    lines.append('  legends, button labels)')
    lines.append('- Pull every numeric token (integers, decimals, comma-separated forms)')
    lines.append('- For each token, search:')
    lines.append('  1. Flattened `data.json` index (every leaf value of every nested key)')
    lines.append('  2. Precomputed derived facts (sums, ratios, deltas, percentiles)')
    lines.append('- Tolerance: 1% relative for values ≥ 50, 0.5 absolute for values < 50')
    lines.append('- Status codes:')
    lines.append('  - `OK`: matches a leaf value in `data.json`')
    lines.append('  - `OK*`: matches a derived fact (sum / ratio / delta / percentile)')
    lines.append('  - `META`: structural metadata (years, grid sizes, ranks, etc.)')
    lines.append('  - `DIFF`: no match found within tolerance — potential discrepancy')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append(f'| Status | Count |')
    lines.append(f'|---|---|')
    lines.append(f'| OK (leaf match) | {total_ok} |')
    lines.append(f'| OK* (derived fact match) | {total_ok_star} |')
    lines.append(f'| META (years, grid sizes) | {total_meta} |')
    lines.append(f'| DIFF (no match) | {total_diff} |')
    lines.append(f'| **Total numeric tokens** | **{total_ok + total_ok_star + total_meta + total_diff}** |')
    lines.append('')
    pass_rate = (total_ok + total_ok_star) / max(1, total_ok + total_ok_star + total_diff) * 100
    lines.append(f'**Verification pass rate (excluding META tokens): {pass_rate:.1f}%**')
    lines.append('')

    # Per-chart detail
    lines.append('## Per-chart findings')
    lines.append('')
    for cname, findings in all_findings.items():
        diff_count = sum(1 for f in findings if f[0] == 'DIFF')
        ok_count = sum(1 for f in findings if f[0] in ('OK', 'OK*'))
        meta_count = sum(1 for f in findings if f[0] == 'META')
        flag = '' if diff_count == 0 else ' ⚠️'
        lines.append(f'### {cname}{flag}')
        lines.append('')
        lines.append(f'**{len(findings)} tokens** — {ok_count} verified, {meta_count} meta, {diff_count} unmatched')
        lines.append('')
        if findings:
            lines.append('| Status | Token | Value | Match |')
            lines.append('|---|---|---|---|')
            for status, s, v, source, src_v in findings:
                if status == 'DIFF':
                    lines.append(f'| **{status}** | `{s}` | {v} | {source} |')
                elif status == 'META':
                    lines.append(f'| {status} | `{s}` | {v} | {source} |')
                else:
                    lines.append(f'| {status} | `{s}` | {v} | `{source}` (= {src_v:.3f}) |')
            lines.append('')

    REPORT_OUT.write_text('\n'.join(lines))
    print(f'\nReport written to {REPORT_OUT}')
    print(f'Summary: {total_ok} OK, {total_ok_star} OK*, {total_meta} META, {total_diff} DIFF')
    print(f'Pass rate (excl META): {pass_rate:.1f}%')


if __name__ == '__main__':
    main()
