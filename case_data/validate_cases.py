from pathlib import Path
import csv, hashlib, json, math

ROOT = Path(__file__).resolve().parent
for line in (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    digest, name = line.split('  ', 1)
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
names = ['single_wave', 'algorithm_comparison', 'joint_two_stage', 'multi_wave', 'deferred_task_reallocation']
books = {}
initial_rows = recovery_rows = 0
for name in names:
    book = json.loads((ROOT / 'json' / (name + '.json')).read_text(encoding='utf-8'))
    books[name] = book
    for s in range(1, 5):
        for row in book['Sheet' + str(s)][2:]:
            if row[0] is None: continue
            p = row[1:6]
            assert all(0 <= x <= 1 for x in p) and math.isclose(sum(p), 1, abs_tol=1e-10)
            initial_rows += 1
    for row in book['Sheet14'][2:]:
        if row[0] is None: continue
        p = row[-5:]
        assert all(0 <= x <= 1 for x in p) and math.isclose(sum(p), 1, abs_tol=1e-10)
        recovery_rows += 1
    for sheet, grid in book.items():
        with (ROOT / 'csv' / name / (sheet + '.csv')).open(encoding='utf-8-sig', newline='') as f:
            exported = list(csv.reader(f))
        assert exported == [['' if x is None else str(x) for x in r] for r in grid], (name, sheet)
for name in names:
    for s in range(1, 15): assert books[name]['Sheet' + str(s)] == books['single_wave']['Sheet' + str(s)]
for name in ['algorithm_comparison', 'joint_two_stage']:
    cfg = json.loads((ROOT / 'config' / (name + '.json')).read_text(encoding='utf-8'))
    assert cfg['num_tasks'] == 40 and cfg['task_ids'] == list(range(1, 41)) and len(cfg['seeds']) == 20
for name in ['multi_wave', 'deferred_task_reallocation']:
    cfg = json.loads((ROOT / 'config' / (name + '.json')).read_text(encoding='utf-8'))
    releases = cfg['wave_releases']
    if isinstance(releases, dict): releases = list(releases.values())
    ids = [x for batch in releases for x in batch]
    assert sorted(ids) == list(range(1, 61)) and len(set(ids)) == 60
cfg = json.loads((ROOT / 'config/weight_sensitivity.json').read_text(encoding='utf-8'))
assert cfg['seeds'] == list(range(9200, 9220))
for scheme in cfg['schemes'].values(): assert math.isclose(sum(scheme['weights']), 1, abs_tol=1e-12)
with (ROOT / 'reported_results/weight_sensitivity_all_runs.csv').open(encoding='utf-8-sig', newline='') as f:
    runs = list(csv.DictReader(f))
assert len(runs) == 100
assert all(int(r['evaluations']) == 10000 and r['feasible'] == 'True' for r in runs)
for scheme in 'ABCDE': assert sorted(int(r['seed']) for r in runs if r['scheme'] == scheme) == cfg['seeds']
print('PASS: checksums, CSV/JSON agreement,', initial_rows, 'initial-state rows,', recovery_rows, 'recovery rows, case subsets, wave releases and 100 weight runs.')
