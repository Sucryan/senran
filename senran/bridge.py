"""編輯器共用的標準輸入介面；不執行來源碼。"""
import json
import sys

from senran.codec import encode_names, unpack, MARKER
from senran.transcriber import 化雅
from senran.agent import 轉西文
from senran.formatter import 賦體, 解賦


def convert(mode, code):
    if mode == 'transcribe':
        return encode_names(code)
    if mode == 'proxy':
        return 化雅(code)
    if mode == 'reverse':
        return 轉西文(code)
    if mode == 'format':
        metadata = None
        try:
            if code.startswith(MARKER):
                metadata = json.loads(code.split('\n', 1)[0][len(MARKER):])
        except ValueError:
            pass
        sealed = (isinstance(metadata, dict) and metadata.get('mode') in {'names', 'runtime'}
                  and {'source_hash', 'body_hash'} <= set(metadata))
        if sealed:
            unpack(code)
        return 賦體(code if sealed else encode_names(code))
    if mode == 'unformat':
        return 解賦(code)
    if mode == 'markdown-reverse':
        return 轉西文(解賦(code))
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
