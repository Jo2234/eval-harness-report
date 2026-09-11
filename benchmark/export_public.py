"""Export measured scores without reproducing extractive source/response prose.

Original captures stay local and unchanged. Public hashes commit to those originals;
redacted public data cannot independently rescore answer text.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

TEXT_KEYS = {'answer', 'excerpt', 'key_points', 'content', 'text'}
NOTE = '[Response text omitted from public export; original fingerprint in answer_sha256]'


def digest(value):
    return hashlib.sha256(value).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def redact(value):
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items() if key not in TEXT_KEYS}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--captured', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--harness', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit('Choose a new public export directory; never overwrite original captures')
    args.out.mkdir(parents=True)
    sys.path.insert(0, str(args.harness.resolve()))
    from fin_eval.runner import artifact_manifest, cases_jsonl, failures_csv, html_report, markdown_report, metrics_csv

    for name in ['config.json', 'sources.json', 'ingestion.json', 'document-map.json', 'REVIEW.md']:
        if name != 'REVIEW.md' or (args.captured / name).exists():
            shutil.copyfile(args.captured / name, args.out / name)
    shutil.copyfile(args.captured / 'SHA256SUMS.json', args.out / 'ORIGINAL_SHA256SUMS.json')
    exported = []
    for line in (args.captured / 'captures.jsonl').read_text().splitlines():
        row = json.loads(line)
        raw = row['raw_response']
        row['public_export'] = {'redacted': True, 'answer_sha256': digest(raw['answer'].encode()),
                                'answer_characters': len(raw['answer']),
                                'original_response_sha256': row['response_sha256']}
        row['raw_response'] = redact(raw)
        row['public_response_sha256'] = digest(json.dumps(row['raw_response'], sort_keys=True).encode())
        exported.append(row)
    (args.out / 'captures.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in exported))
    for name in ['copilot-local', 'lexical-baseline']:
        source = args.captured / name / 'results.json'
        original = json.loads(source.read_text())
        payload = copy.deepcopy(original)
        payload['metadata']['public_export'] = {
            'redacted': True, 'original_results_sha256': digest(source.read_bytes()),
            'note': 'Scores unchanged. Response prose and source excerpts omitted; original/newly reproduced captures are required to rescore text.'}
        for row in payload['results']:
            row['answer_sha256'] = digest(row['answer'].encode())
            row['answer_characters'] = len(row['answer'])
            row['answer'] = NOTE
            row['citations'] = redact(row['citations'])
            row['raw_response'] = redact(row['raw_response'])
        assert payload['summary'] == original['summary'] and payload['gate'] == original['gate']
        out = args.out / name
        out.mkdir()
        dump(out / 'results.json', payload)
        (out / 'summary.md').write_text('> Public redacted export: response prose omitted; scores unchanged.\n\n' + markdown_report(payload))
        (out / 'report.html').write_text(html_report(payload).replace('<body>', '<body><p>Public redacted export: response prose and source excerpts omitted; scores unchanged.</p>', 1))
        (out / 'failures.csv').write_text(failures_csv(payload['results']))
        (out / 'metrics.csv').write_text(metrics_csv(payload))
        (out / 'cases.jsonl').write_text(cases_jsonl(payload['results']))
        dump(out / 'manifest.json', artifact_manifest(out))
    dump(args.out / 'PUBLIC_EXPORT.json', {
        'policy': 'Original full captures retained locally. All extractive answers, key points and source-excerpt fields omitted from public target payloads, including filings and transcripts.',
        'original_capture_file_sha256': digest((args.captured / 'captures.jsonl').read_bytes()),
        'original_inventory_sha256': digest((args.captured / 'SHA256SUMS.json').read_bytes()),
        'export_script_sha256': digest(Path(__file__).read_bytes()),
        'original_hash_file': 'ORIGINAL_SHA256SUMS.json',
        'public_hash_file': 'SHA256SUMS.json',
        'scores_changed': False,
        'rescore_limitation': 'Public redacted records cannot independently rescore answer text. Original local or newly reproduced captures are required.',
        'retained': 'Questions, curator-authored case targets/rubrics, short source locators, citation IDs/metadata, measured metrics/diagnostics, execution/config/source provenance, original response/answer hashes.'})
    # REVIEW and rendered pages are editorial derivatives, outside capture inventories.
    inventory = {str(path.relative_to(args.out)): digest(path.read_bytes()) for path in args.out.rglob('*')
                 if path.is_file() and path.name != 'REVIEW.md'}
    dump(args.out / 'SHA256SUMS.json', inventory)
    print('Created explicit public redacted export at', args.out)


if __name__ == '__main__':
    main()
