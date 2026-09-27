"""整庫四界搬卷；非 Python 資料逐位元組保留，不執行外邦程式。"""
import hashlib
import io
import json
import os
import shutil
import stat
import tempfile
import tokenize
from pathlib import Path, PurePosixPath

from senran.codec import encode_names, decode_source
from senran.formatter import 賦體, 解賦

MANIFEST = '.senran-manifest.json'
STAGES = {'format': 'encode', 'unformat': 'format', 'decode': 'unformat'}


def file_hash(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or not path.parts or '\\' in name or path.as_posix() != name:
        raise ValueError('封卷含不安全路徑：' + name)
    return Path(*path.parts)


def convert_repository(source, destination, mode, style='senran'):
    """encode → format → unformat → decode；目的地必須不存在。"""
    source = Path(source).resolve(strict=True)
    destination = Path(destination).absolute()
    resolved_destination = destination.resolve()
    if source == resolved_destination or source in resolved_destination.parents or resolved_destination in source.parents:
        raise ValueError('來源與目的地不得重疊。')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(str(destination))
    if mode not in {'encode', 'format', 'unformat', 'decode'}:
        raise ValueError('未知轉換方向。')
    if not source.is_dir():
        raise ValueError('來源必須是目錄。')
    if mode == 'encode':
        if (source / MANIFEST).exists() or (source / MANIFEST).is_symlink():
            raise ValueError('來源已有森蚺封卷清冊。')
        manifest = {'version': 1, 'stage': mode, 'style': style, 'python': []}
    else:
        manifest_path = source / MANIFEST
        if manifest_path.is_symlink():
            raise ValueError('封卷清冊不得是連結。')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest.get('version') != 1 or manifest.get('stage') != STAGES[mode]:
            raise ValueError('封卷階段不符，請依 encode、format、unformat、decode 順序。')
    entries = {}
    outputs = set()
    for entry in manifest['python']:
        key = entry['current']
        safe_path(key)
        safe_path(entry['original'])
        if key in entries or entry['original'] in outputs or entry['original'] == MANIFEST:
            raise ValueError('封卷清冊含重複或保留路徑。')
        entries[key] = entry
        outputs.add(entry['original'])
    paths = {}
    for current, directories, files in os.walk(source, followlinks=False):
        directories[:] = [name for name in directories if name != '.git']
        for name in list(directories) + files:
            path = Path(current) / name
            key = path.relative_to(source).as_posix()
            if key != MANIFEST:
                paths[key] = path
            if path.is_symlink() and name in directories:
                directories.remove(name)
    if mode != 'encode' and not set(entries) <= set(paths):
        raise ValueError('封卷碼卷遺失。')
    planned = {}
    output_paths = set()
    occupied = set(paths)
    for key in sorted(paths):
        output = key
        if key in entries:
            if mode == 'format':
                output += '.md'
                while output in occupied:
                    output += '.md'
                occupied.add(output)
            else:
                output = entries[key]['original']
        if output in output_paths:
            raise ValueError('目的路徑相撞：' + output)
        output_paths.add(output)
        planned[key] = output
    links = {planned[key] for key, path in paths.items() if path.is_symlink()}
    for output in planned.values():
        if any(parent.as_posix() in links for parent in PurePosixPath(output).parents):
            raise ValueError('封卷目的地不得穿越連結：' + output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.senran-', dir=str(destination.parent)))
    try:
        seen = set()
        for current, directories, files in os.walk(source, followlinks=False):
            relative = Path(current).relative_to(source)
            directories[:] = [name for name in directories if name != '.git']
            target_dir = temporary / relative
            target_dir.mkdir(exist_ok=True)
            for name in list(directories):
                path = Path(current) / name
                if path.is_symlink():
                    (target_dir / name).symlink_to(os.readlink(path), target_is_directory=True)
                    directories.remove(name)
            for name in files:
                path = Path(current) / name
                key = (relative / name).as_posix()
                if key == MANIFEST:
                    continue
                target = target_dir / name
                if target.exists() or target.is_symlink():
                    raise ValueError('目的檔名相撞：' + key)
                if path.is_symlink():
                    if key in entries:
                        raise ValueError('碼卷不得換成連結：' + key)
                    target.symlink_to(os.readlink(path))
                    continue
                if not stat.S_ISREG(path.stat().st_mode):
                    raise ValueError('只支援一般檔案與連結：' + key)
                if mode == 'encode' and path.suffix == '.py':
                    data = path.read_bytes()
                    text_only = False
                    try:
                        encoding, _ = tokenize.detect_encoding(io.BytesIO(data).readline)
                        text = data.decode(encoding)
                    except (SyntaxError, UnicodeError, LookupError):
                        # CPython 含故意錯誤的編碼素材，逐位元組對應搬卷。
                        encoding, text, text_only = 'latin-1', data.decode('latin-1'), True
                    if text.encode(encoding) != data:
                        raise ValueError('編碼不能逐位元組往返：' + key)
                    encoded = encode_names(text, style=style).encode('utf-8')
                    entry = {'original': key, 'current': key, 'encoding': encoding,
                             'text_only': text_only,
                             'original_hash': file_hash(data), 'current_hash': file_hash(encoded)}
                    manifest['python'].append(entry)
                    target.write_bytes(encoded)
                elif key in entries:
                    entry = entries[key]
                    seen.add(key)
                    data = path.read_bytes()
                    if file_hash(data) != entry['current_hash']:
                        raise ValueError('碼卷已變更：' + key)
                    text = data.decode('utf-8')
                    if mode == 'format':
                        target = temporary / safe_path(planned[key])
                        result = 賦體(text).encode('utf-8')
                        entry['current'] = planned[key]
                    else:
                        target = temporary / safe_path(entry['original'])
                        if temporary not in target.resolve().parents:
                            raise ValueError('封卷目的地經連結越界：' + entry['original'])
                        result = (解賦(text).encode('utf-8') if mode == 'unformat'
                                  else decode_source(text).encode(entry['encoding']))
                        entry['current'] = entry['original']
                        if mode == 'decode' and file_hash(result) != entry['original_hash']:
                            raise ValueError('原碼位元組校驗不符：' + key)
                    if target.exists() or target.is_symlink():
                        raise ValueError('目的檔名相撞：' + str(target.relative_to(temporary)))
                    target.write_bytes(result)
                    entry['current_hash'] = file_hash(result)
                else:
                    shutil.copyfile(path, target)
                shutil.copymode(path, target)
        if mode != 'encode' and seen != set(entries):
            raise ValueError('封卷碼卷遺失：' + ', '.join(sorted(set(entries) - seen)))
        if mode != 'decode':
            manifest['stage'] = mode
            (temporary / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # 目錄權限最後補回，避免唯讀原目錄妨礙寫入。
        for current, directories, _ in os.walk(source, followlinks=False):
            directories[:] = [name for name in directories if name != '.git' and not (Path(current) / name).is_symlink()]
            shutil.copymode(current, temporary / Path(current).relative_to(source))
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(str(destination))
        temporary.rename(destination)
        return {'python_files': len(manifest['python']), 'stage': mode, 'destination': str(destination)}
    finally:
        if temporary.exists():
            for current, directories, _ in os.walk(temporary, followlinks=False):
                os.chmod(current, 0o700)
                directories[:] = [name for name in directories if not (Path(current) / name).is_symlink()]
            shutil.rmtree(temporary)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='整庫無損四界轉錄（不執行專案）')
    parser.add_argument('mode', choices=['encode', 'encode-zhpy', 'format', 'unformat', 'decode'])
    parser.add_argument('source')
    parser.add_argument('destination')
    args = parser.parse_args()
    report = convert_repository(args.source, args.destination,
                                'encode' if args.mode == 'encode-zhpy' else args.mode,
                                style='zhpy' if args.mode == 'encode-zhpy' else 'senran')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
