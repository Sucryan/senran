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
import builtins

from senran.dictionary import ALL_LEXICON
from senran.zhpy_keywords import ZHPY_ALIASES

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
GRAMMAR = {
    'False': '假', 'None': '空', 'True': '真', 'and': '且', 'as': '作',
    'assert': '驗', 'async': '異步', 'await': '候', 'break': '止',
    'class': '類', 'continue': '續', 'def': '術', 'del': '刪',
    'elif': '若又', 'else': '否則', 'except': '捕', 'finally': '終',
    'for': '遍', 'from': '由', 'global': '全域', 'if': '若',
    'import': '納', 'in': '於', 'is': '乃', 'lambda': '匿名',
    'nonlocal': '外域', 'not': '非', 'or': '或', 'pass': '略',
    'raise': '擲', 'return': '歸', 'try': '試', 'while': '當',
    'with': '偕', 'yield': '產', 'match': '配', 'case': '案',
    'type': '型別宣告', '_': '任',
}
PLAIN_GRAMMAR = dict(GRAMMAR, **{
    'def': '定義', 'class': '類別', 'return': '返回', 'if': '如果',
    'elif': '否則如果', 'for': '取', 'in': '在', 'break': '跳出',
    'continue': '繼續', 'pass': '略過', 'try': '嘗試', 'except': '異常',
    'finally': '最後', 'raise': '引發', 'assert': '申明', 'from': '從',
    'import': '導入', 'as': '作為', 'with': '伴隨', 'yield': '產生',
    'lambda': '方程式', 'is': '是', 'del': '刪除',
})
PLAIN_NAMES = {'self': '我', 'print': '印出', 'input': '輸入', 'len': '長度',
               'range': '範圍', 'sum': '總和', 'list': '列表', 'dict': '字典',
               'str': '字串', 'int': '整數', 'float': '浮點數', 'bool': '布林',
               'tuple': '元組', 'set': '集合', 'open': '打開'}
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


def bindings(tree):
    bound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            bound.add(node.id)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bound.update(alias.asname or alias.name.split('.')[0] for alias in node.names)
    return bound


def source_language(source):
    """原生碼優先；未綁定的中文內建呼叫與中文語法視為方言。"""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SyntaxWarning)
            tree = ast.parse(source)
    except (SyntaxError, ValueError, TypeError, SystemError, RecursionError):
        return 'dialect'
    bound = bindings(tree)
    aliases = dict(ZHPY_ALIASES)
    aliases.update({value: key for key, value in BUILTINS.items()})
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in bound and node.id in aliases and hasattr(builtins, aliases[node.id]):
                return 'dialect'
    return 'python'


def encode_names(source, style='senran'):
    """整庫閱覽模式；文言語法與可逆更名，絕不保存原碼副本。"""
    positions = offsets(source)
    if style not in {'senran', 'zhpy'}:
        raise ValueError('未知中文詞律。')
    grammar_table = PLAIN_GRAMMAR if style == 'zhpy' else GRAMMAR
    mapping = {}
    edits = []
    dialect = {value: key for key, value in GRAMMAR.items()}
    dialect.update(ZHPY_ALIASES)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SyntaxWarning)
            bound = bindings(ast.parse(source))
    except (SyntaxError, ValueError, TypeError, SystemError, RecursionError):
        bound = set()
    importing = False
    previous = ''
    statement_start = True
    for token in tokens(source):
        name = token.string
        native = dialect.get(name, name)
        if token.type == tokenize.NEWLINE or name == ';':
            importing = False
            statement_start = True
        if token.type == tokenize.NAME and native in {'from', 'import'} and statement_start:
            importing = True
        attribute = previous == '.'
        if token.type not in {tokenize.NL, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT}:
            previous = name
            if token.type != tokenize.NEWLINE and name != ';':
                statement_start = False
        if token.type != tokenize.NAME or (name.startswith('__') and name.endswith('__')):
            continue
        if importing or attribute:
            continue
        if name not in mapping:
            grammar = grammar_table.get(native)
            names = PLAIN_NAMES if style == 'zhpy' else dict(BUILTINS, self='己')
            mapping[name] = grammar or (names.get(native, name) if name not in bound or native == 'self' else name)
        if mapping[name] == name:
            continue
        edits.append((positions[token.start[0] - 1] + token.start[1],
                      positions[token.end[0] - 1] + token.end[1], mapping[name]))
    body = patch(source, edits)
    ordered = list(mapping)
    indexes = {name: index for index, name in enumerate(ordered)}
    spans = []
    shift = 0
    for start, end, replacement in sorted(edits):
        spans.append([start + shift, indexes[source[start:end]]])
        shift += len(replacement) - (end - start)
    return seal(body, {'mode': 'names', 'style': style, 'source_language': source_language(source),
                       'symbols': [[mapping[name], name] for name in ordered],
                       'spans': spans, 'source_hash': digest(source)})


def encode_runtime(source):
    """沿用代理體的小程式入口；可逆記錄每項改動，字串註解不動。"""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # 中文語法以可逆閱覽體收錄，不以 Python 解析器硬解。
        ast.parse(to_python(source))
        return encode_names(source)
    positions = offsets(source)
    stream = tokens(source)
    edits = []
    aliases = {}
    import_ranges = []
    rewritten_import_ranges = []
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
                rewritten_import_ranges.append((start, end))
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
        if token.type == tokenize.NAME:
            name = token.string
            if any(a <= start < b for a, b in import_ranges):
                if name in keyword.kwlist and not any(a <= start < b for a, b in rewritten_import_ranges):
                    edits.append((start, end, GRAMMAR[name]))
                previous = token
                continue
            replacement = name
            if name in keyword.kwlist or name in getattr(keyword, 'softkwlist', ()):
                replacement = GRAMMAR[name]
            elif previous and previous.string == '.':
                if start in proxy_attributes:
                    replacement = VOCABULARY.get(name, name)
            elif name in aliases:
                replacement = aliases[name]
            elif name in CONSTANTS:
                replacement = CONSTANTS[name]
            elif name in BUILTINS and name not in bound:
                replacement = BUILTINS[name]
            if replacement != name and (name in GRAMMAR or replacement not in occupied):
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
    header = '由 senran 納 ' + ', '.join(sorted(imported)) + '\n' if imported else ''
    if insertion and source[insertion - 1:insertion] != '\n':
        header = '\n' + header
    edits.append((insertion, insertion, header))
    ledger = []
    shift = 0
    for start, end, replacement in sorted(edits):
        ledger.append([start + shift, replacement, source[start:end]])
        shift += len(replacement) - (end - start)
    body = patch(source, edits)
    return seal(body, {'mode': 'runtime', 'source_language': source_language(source),
                       'edits': ledger, 'source_hash': digest(source)})


def decode_source(source):
    metadata, body = unpack(source)
    if metadata is None:
        return None
    if metadata.get('mode') == 'runtime':
        edits = [(start, start + len(changed), original) for start, changed, original in metadata['edits']]
    elif metadata.get('mode') == 'names':
        if 'symbols' in metadata:
            symbols = metadata['symbols']
            edits = [(start, start + len(symbols[index][0]), symbols[index][1])
                     for start, index in metadata['spans']]
            original = patch(body, edits)
            if digest(original) != metadata.get('source_hash'):
                raise ValueError('森蚺名稱對照已損壞，還原校驗不符。')
            return original
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


def to_python(source):
    """將完整符節的白話／文言語法交還 Python；字串註解不動。"""
    metadata, _ = unpack(source)
    original = decode_source(source)
    if original is not None:
        if metadata.get('source_language', source_language(original)) == 'python':
            return original
        source = original
    bound = set()
    try:
        tree = ast.parse(source)
        bound = bindings(tree)
    except SyntaxError:
        pass
    # 只採語法及現行內建函式；不將周蟒系統／回溯詞表當作語法。
    aliases = {name: target for name, target in ZHPY_ALIASES.items()
               if target in keyword.kwlist or target in {'self', 'not in', 'is not', '==', '!='}
               or hasattr(builtins, target)}
    aliases.update({value: key for key, value in GRAMMAR.items()})
    aliases.update({value: key for key, value in BUILTINS.items()})
    # 周蟒 Python 2 名稱在本庫改循 Python 3；不攜入舊執行器。
    aliases.update({'檔案': 'open', '档案': 'open', '快速範圍': 'range', '快速范围': 'range'})
    positions = offsets(source)
    edits = []
    previous = None
    importing = False
    stream = tokens(source)
    for index, token in enumerate(stream):
        if token.type == tokenize.NEWLINE or token.string == ';':
            importing = False
        if token.type != tokenize.NAME:
            if token.type not in (tokenize.COMMENT, tokenize.NL, tokenize.INDENT, tokenize.DEDENT):
                previous = token
            continue
        name = token.string
        replacement = aliases.get(name, name)
        if name in bound:
            replacement = name
        elif previous and previous.string == '.':
            replacement = name
        elif importing and replacement not in {'as', 'import'}:
            replacement = name
        elif name == '若' and replacement == 'if' and index + 1 < len(stream) and stream[index + 1].string == '(':
            # 若(...) 可為舊式邏輯糖，也可為 if (...)；以閉括號後的冒號辨之。
            depth = 0
            for following_index in range(index + 1, len(stream)):
                following = stream[following_index]
                if following.string in {'(', '[', '{'}:
                    depth += 1
                elif following.string in {')', ']', '}'}:
                    depth -= 1
                    if depth == 0:
                        if following_index + 1 >= len(stream) or stream[following_index + 1].string != ':':
                            replacement = name
                        break
        if replacement == 'import':
            importing = True
        if replacement != name:
            edits.append((positions[token.start[0] - 1] + token.start[1],
                          positions[token.end[0] - 1] + token.end[1], replacement))
        previous = token
    return patch(source, edits)
