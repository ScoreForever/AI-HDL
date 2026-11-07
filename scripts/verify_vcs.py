#!/usr/bin/env python3
"""Run untouched course Makefiles in a fresh directory and validate real logs."""
import datetime
import hashlib
import json
import pathlib
import re
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]

def main():
    if not shutil.which('vcs'):
        raise SystemExit('VCS is not on PATH. Initialize the course tool/license environment first.')
    manifest = json.loads((ROOT / 'docs/course_manifest.json').read_text())
    for rel, digest in manifest['unmodified_files'].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != digest:
            raise SystemExit(f'Course file changed: {rel}')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = ROOT / 'build' / ('vcs-' + stamp)
    out.mkdir(parents=True, exist_ok=False)
    shutil.copytree(ROOT / 'lab1', out / 'lab1')
    results = []
    for task, expected in [('winograd', 10), ('cordic', 10), ('fsm', 3)]:
        run = out / 'lab1' / task / 'run'
        with (run / 'make.log').open('w') as log:
            proc = subprocess.run(['make', 'rerun'], cwd=run, stdout=log, stderr=subprocess.STDOUT)
        compile_log = run / 'compile.log'
        simulation_log = run / 'simulation.log'
        if proc.returncode or not compile_log.exists() or not simulation_log.exists():
            raise SystemExit(f'{task}: build/run failed; inspect {run}/make.log')
        text = simulation_log.read_text(errors='replace')
        compilation = compile_log.read_text(errors='replace')
        passes = sum('PASS' in line and 'ALL PASS' not in line for line in text.splitlines())
        if passes != expected or 'ALL PASS' not in text or re.search(r'ERROR|FAIL|FATAL', text, re.I) or re.search(r'Error-|Fatal-', compilation):
            raise SystemExit(f'{task}: validation failed; inspect {run}')
        results.append({'task': task, 'passes': passes, 'exit_code': proc.returncode})
        print(f'{task}: {passes} PASS; ALL PASS', flush=True)
    (out / 'summary.json').write_text(json.dumps({'utc': stamp, 'results': results}, indent=2))
    print(f'Validated VCS logs: {out}')

if __name__ == '__main__':
    main()
