"""編輯器共用的標準輸入介面；不執行來源碼。"""
import json
import sys

from senran.codec import encode_names, unpack, decode_source, to_python, MARKER
from senran.transcriber import 化雅
from senran.agent import 轉西文
from senran.formatter import 賦體, 解賦


def is_packet(code):
    metadata = None
    try:
        if code.startswith(MARKER):
            metadata = json.loads(code.split('\n', 1)[0][len(MARKER):])
    except ValueError:
        pass
    return (isinstance(metadata, dict) and metadata.get('mode') in {'names', 'runtime'}
            and {'source_hash', 'body_hash'} <= set(metadata))


def convert(mode, code):
    if mode in {'transcribe', 'zhpy'}:
        original = decode_source(code) if is_packet(code) else code
        return encode_names(original, style='zhpy' if mode == 'zhpy' else 'senran')
    if mode == 'proxy':
        return 化雅(code)
    if mode == 'reverse':
        return to_python(code) if is_packet(code) else 轉西文(code)
    if mode == 'format':
        sealed = is_packet(code)
        if sealed:
            unpack(code)
        return 賦體(code if sealed else encode_names(code))
    if mode == 'unformat':
        return 解賦(code)
    if mode == 'markdown-reverse':
        return convert('reverse', 解賦(code))
    raise ValueError('未知轉換方向。')


def main():
    try:
        request = json.load(sys.stdin)
        result = convert(request['mode'], request['code'])
        json.dump({'result': result}, sys.stdout, ensure_ascii=False)
    except Exception as error:
        sys.stderr.write(str(error) + '\n')
        sys.exit(1)


if __name__ == '__main__':
    main()
