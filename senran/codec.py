"""不重排原文的轉錄法：符節定位、可逆更名、校驗封卷。"""
import ast
import hashlib
import io
import json
import keyword
import re
import bisect
import warnings
import tokenize

from senran.dictionary import ALL_LEXICON

MARKER = '# senran-source-v1 '
BUILTINS = {
    'print': '書', 'len': '計', 'range': '疇', 'sum': '總',
    'open': '啟', 'input': '問', 'sorted': '序', 'reversed': '反',
    'type': '審', 'isinstance': '係', 'list': '錄', 'dict': '譜',
    'int': '整', 'float': '浮', 'str': '文', 'bytes': '節',
    'set': '集', 'tuple': '偶', 'max': '極大', 'min': '極小',
    'enumerate': '枚', 'zip': '並',
}
CONSTANTS = {'True': '真', 'False': '假', 'None': '空'}
ALIASES = {'requests': '求', 'httpx': '疾求', 'torch': '神算',
           'numpy': '算矩', 'pandas': '史冊', 'math': '算術',
           'json': '法書', 'sqlite3': '庫', 'flask': '法宴',
           'fastapi': '急驛', 'click': '號令'}
VOCABULARY = {english: chinese for chinese, english in ALL_LEXICON.items()}
VOCABULARY.update(BUILTINS)
VOCABULARY.update(CONSTANTS)
VOCABULARY.update({'self': '己', 'Dog': '犬', 'Cat': '貓', 'User': '客',
                   'get': '得', 'json': '譜', 'forward': '前向',
                   'status_code': '格', 'tensor': '量', 'grad': '勢',
                   'backward': '反溯', 'zero_grad': '清勢'})
HEX_DIGITS = '〇一二三四五六七八九甲乙丙丁戊己'
CANONICAL = {}
for _name in list(BUILTINS) + list(CONSTANTS) + sorted(VOCABULARY):
    if _name in VOCABULARY:
        CANONICAL.setdefault(VOCABULARY[_name], _name)


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def tokens(source):
    """收錄實際位置，保留每一空格；容許新版本尚未能解析的語法。"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SyntaxWarning)
            return list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError, SystemError):
        # Black、CPython 的故意錯誤素材仍須原樣往返。此路徑是文字更名，
        # 不宣稱錯誤素材具有 Python 語義；字串與註解仍保持原文。
        pattern = re.compile(
            r'''\#[^\r\n]*|(?:[rRuUbBfFtT]{0,2})(?:''' +
            r'''\x27\x27\x27[\s\S]*?(?:\x27\x27\x27|\Z)|"""[\s\S]*?(?:"""|\Z)|''' +
            r'''\x27(?:\\[\s\S]|[^\x27\\\r\n])*(?:\x27|(?=\r?\n)|\Z)|"(?:\\[\s\S]|[^"\\\r\n])*(?:"|(?=\r?\n)|\Z))|''' +
            tokenize.Number + r'''|(?:[^\W\d]|_)\w*'''
        )
        positions = offsets(source)
        result = []
        for match in pattern.finditer(source):
            name = match.group()
            if not name.isidentifier():
                continue
            start_row = bisect.bisect_right(positions, match.start())
            end_row = bisect.bisect_right(positions, match.end())
            result.append(tokenize.TokenInfo(tokenize.NAME, name,
                          (start_row, match.start() - positions[start_row - 1]),
                          (end_row, match.end() - positions[end_row - 1]), ''))
        return result


def offsets(source):
    result = [0]
    for match in re.finditer('\n', source):
        result.append(match.end())
    if result[-1] != len(source):
        result.append(len(source))
    return result


def patch(source, edits):
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source


def seal(body, metadata):
    metadata['body_hash'] = digest(body)
    return MARKER + json.dumps(metadata, ensure_ascii=True, separators=(',', ':')) + '\n' + body


def unpack(source):
    if not source.startswith(MARKER):
        return None, source
    line, separator, body = source.partition('\n')
    if not separator:
        raise ValueError('森蚺封卷不完整。')
    metadata = json.loads(line[len(MARKER):])
    if metadata.get('body_hash') != digest(body):
        raise ValueError('森蚺碼已變更，不能聲稱逐字還原；請保留完整封卷。')
    return metadata, body


def encode_names(source):
    """整庫閱覽模式；更名所有非保留字，絕不保存原碼副本。"""
    positions = offsets(source)
    mapping = {}
    edits = []
    reserved = set(keyword.kwlist) | set(getattr(keyword, 'softkwlist', ()))
    for token in tokens(source):
        name = token.string
        if token.type != tokenize.NAME or name in reserved or (name.startswith('__') and name.endswith('__')):
            continue
        if name not in mapping:
            # 原名的 UTF-8 十六進位拼寫轉為漢字，名稱跨檔穩定且不相撞。
            suffix = ''.join(HEX_DIGITS[int(digit, 16)] for digit in name.encode('utf-8').hex())
            base = VOCABULARY.get(name, '名')
            mapping[name] = base if CANONICAL.get(base) == name else base + '之' + suffix
        edits.append((positions[token.start[0] - 1] + token.start[1],
                      positions[token.end[0] - 1] + token.end[1], mapping[name]))
    body = patch(source, edits)
    ordered = list(mapping)
    indexes = {mapping[name]: index for index, name in enumerate(ordered)}
    spans = []
    shift = 0
    for start, end, replacement in sorted(edits):
        spans.append([start + shift, indexes[replacement]])
        shift += len(replacement) - (end - start)
    return seal(body, {'mode': 'names', 'names': {value: key for key, value in mapping.items()},
                       'spans': spans, 'source_hash': digest(source)})


def encode_runtime(source):
    """沿用代理體的小程式入口；可逆記錄每項改動，字串註解不動。"""
    tree = ast.parse(source)
    positions = offsets(source)
    stream = tokens(source)
    edits = []
    aliases = {}
    import_ranges = []
    bound = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del))}
    bound.update(node.arg for node in ast.walk(tree) if isinstance(node, ast.arg))
    bound.update(node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    bound.update(alias.asname or alias.name.split('.')[0]
                 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
                 for alias in node.names)
    occupied = {token.string for token in stream if token.type == tokenize.NAME}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # AST 的欄位是 UTF-8 位元組，不是字元。
            lines = source.splitlines(keepends=True) if '\f' not in source else [source[a:b] for a, b in zip(positions, positions[1:])]
            start = positions[node.lineno - 1] + len(lines[node.lineno - 1].encode('utf-8')[:node.col_offset].decode('utf-8'))
            end = positions[node.end_lineno - 1] + len(lines[node.end_lineno - 1].encode('utf-8')[:node.end_col_offset].decode('utf-8'))
            import_ranges.append((start, end))
            if isinstance(node, ast.Import) and all('.' not in alias.name or alias.asname for alias in node.names):
                parts = []
                for alias in node.names:
                    old = alias.asname or alias.name
                    new = old if alias.asname else ALIASES.get(old, old)
                    if new != old and new in occupied:
                        new = old
                    aliases[old] = new
                    parts.append("%s = 引入(%r)" % (new, alias.name))
                edits.append((start, end, '; '.join(parts)))
    proxies = set(aliases)
    for _ in range(len(tree.body) + 1):
        before = set(proxies)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                function = node.value.func
                returns_proxy = (isinstance(function, ast.Name) and function.id in {'open', 'range', 'sorted', 'reversed'} and function.id not in bound)
                returns_proxy |= (isinstance(function, ast.Attribute) and isinstance(function.value, ast.Name)
                                  and function.value.id in proxies and function.attr not in {'read', 'item', 'sqrt', 'sin', 'cos', 'score'})
                if returns_proxy:
                    proxies.update(target.id for target in node.targets if isinstance(target, ast.Name))
        if proxies == before:
            break
    proxy_attributes = set()
    source_lines = [source[a:b] for a, b in zip(positions, positions[1:])]
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in proxies:
            end = positions[node.end_lineno - 1] + len(source_lines[node.end_lineno - 1].encode('utf-8')[:node.end_col_offset].decode('utf-8'))
            proxy_attributes.add(end - len(node.attr))
    previous = None
    for token in stream:
        start = positions[token.start[0] - 1] + token.start[1]
        end = positions[token.end[0] - 1] + token.end[1]
        if token.type == tokenize.NAME and not any(a <= start < b for a, b in import_ranges):
            name = token.string
            replacement = name
            if previous and previous.string == '.':
                if start in proxy_attributes:
                    replacement = VOCABULARY.get(name, name)
            elif name in aliases:
                replacement = aliases[name]
            elif name in CONSTANTS:
                replacement = CONSTANTS[name]
            elif name in BUILTINS and name not in bound:
                replacement = BUILTINS[name]
            if replacement != name and replacement not in occupied:
                edits.append((start, end, replacement))
        if token.type not in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
            previous = token
    # 插入於模組說明與 future imports 之後，以免破壞 Python 法度。
    insertion = 0
    for index, node in enumerate(tree.body):
        if (index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)) or (isinstance(node, ast.ImportFrom) and node.module == '__future__'):
            insertion = positions[node.end_lineno]
        else:
            break
    imported = {replacement for _, _, replacement in edits if replacement in set(BUILTINS.values()) | set(CONSTANTS.values())}
    if aliases:
        imported.add('引入')
    header = 'from senran import ' + ', '.join(sorted(imported)) + '\n' if imported else ''
    if insertion and source[insertion - 1:insertion] != '\n':
        header = '\n' + header
    edits.append((insertion, insertion, header))
    ledger = []
    shift = 0
    for start, end, replacement in sorted(edits):
        ledger.append([start + shift, replacement, source[start:end]])
        shift += len(replacement) - (end - start)
    body = patch(source, edits)
    return seal(body, {'mode': 'runtime', 'edits': ledger, 'source_hash': digest(source)})


def decode_source(source):
    metadata, body = unpack(source)
    if metadata is None:
        return None
    if metadata.get('mode') == 'runtime':
        edits = [(start, start + len(changed), original) for start, changed, original in metadata['edits']]
    elif metadata.get('mode') == 'names':
        names = metadata['names']
        ordered = list(names)
        if 'spans' in metadata:
            edits = [(start, start + len(ordered[index]), names[ordered[index]])
                     for start, index in metadata['spans']]
        else:
            positions = offsets(body)
            edits = [(positions[t.start[0] - 1] + t.start[1], positions[t.end[0] - 1] + t.end[1], names[t.string])
                     for t in tokens(body) if t.type == tokenize.NAME and t.string in names]
    else:
        raise ValueError('未知森蚺封卷版本。')
    original = patch(body, edits)
    if digest(original) != metadata.get('source_hash'):
        raise ValueError('森蚺名稱對照已損壞，還原校驗不符。')
    return original
