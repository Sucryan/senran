"""編輯器共用的標準輸入介面；不執行來源碼。"""
import json
import sys

from senran.codec import encode_names, unpack, decode_source, to_python, MARKER, digest, source_language
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
    # 編輯後視為新稿；原稿的逐字還原仍由嚴格 decode_source 守護。
    if mode in {'transcribe', 'zhpy', 'reverse', 'format'} and is_packet(code):
        metadata, body = unpack(code, verify_body=False)
        if metadata['body_hash'] != digest(body):
            code = to_python(code, editable=True)
            if mode == 'reverse':
                return code
    if mode in {'transcribe', 'zhpy'}:
        original = decode_source(code) if is_packet(code) else code
        return encode_names(original, style='zhpy' if mode == 'zhpy' else 'senran')
    if mode == 'proxy':
        return 化雅(code)
    if mode == 'reverse':
        if is_packet(code):
            return to_python(code)
        return code if source_language(code) == 'python' else 轉西文(code)
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
