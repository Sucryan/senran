"""下載參考庫並考校四界往返；不安裝、不匯入、不執行參考庫。"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from senran.repository import convert_repository

REPOSITORIES = [
    'encode/httpx', 'psf/requests', 'pallets/flask', 'fastapi/fastapi',
    'encode/starlette', 'pallets/click', 'psf/black', 'MagicStack/uvloop',
    'python/cpython', 'karpathy/minGPT', 'karpathy/nanoGPT', 'vwxyzjn/cleanrl',
]


def snapshot(root):
    result = {}
    for current, directories, files in os.walk(root, followlinks=False):
        directories[:] = [name for name in directories if name != '.git']
        for name in list(directories) + files:
            path = Path(current) / name
            key = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[key] = ['link', os.readlink(path)]
                if name in directories:
                    directories.remove(name)
            elif path.is_dir():
                result[key] = ['directory', path.stat().st_mode & 0o777]
            else:
                result[key] = ['file', path.stat().st_mode & 0o777,
                               hashlib.sha256(path.read_bytes()).hexdigest()]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--style', choices=['senran', 'zhpy'], default='senran')
    parser.add_argument('repositories', nargs='*')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    reports = []
    version = hashlib.sha256(b''.join((root / 'senran' / name).read_bytes()
                                     for name in ['codec.py', 'formatter.py', 'repository.py', 'zhpy_keywords.py'])).hexdigest()[:12] + '-' + args.style
    for repo in args.repositories or REPOSITORIES:
        if repo not in REPOSITORIES:
            raise ValueError('參考庫不在清單內：' + repo)
        name = repo.split('/')[-1]
        source = root / 'examples' / 'upstream' / name
        if not source.exists() and args.fetch:
            source.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/' + repo + '.git', str(source)], check=True)
        commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
        if subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain', '--untracked-files=all'], text=True).strip():
            raise ValueError('參考庫已修改，不能用原提交標示考校：' + repo)
        original = snapshot(source)
        output = root / 'examples' / 'roundtrip' / name / commit / version
        output.mkdir(parents=True, exist_ok=True)
        previous = source
        for mode in ['encode', 'format', 'unformat', 'decode']:
            destination = output / mode
            # 既有結果也必須比對，絕不覆蓋。
            if not destination.exists():
                convert_repository(previous, destination, mode, style=args.style)
            previous = destination
        restored = snapshot(previous)
        mismatches = sorted(key for key in set(original) | set(restored) if original.get(key) != restored.get(key))
        report = {'repository': repo, 'style': args.style, 'commit': commit, 'entries': len(original),
                  'python_files': sum(key.endswith('.py') and value[0] == 'file' for key, value in original.items()),
                  'mismatches': mismatches, 'restored': str(previous)}
        print(json.dumps(report, ensure_ascii=False), flush=True)
        reports.append(report)
        if mismatches:
            raise AssertionError('往返有差異：' + repo)
    report_name = 'report.json' if args.style == 'senran' else 'zhpy-report.json'
    (root / 'examples' / 'roundtrip' / report_name).write_text(json.dumps(reports, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
