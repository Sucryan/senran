"""編輯器實際呼叫共用轉錄介面的考校。"""
import json
import shutil
import subprocess
import unittest
from pathlib import Path


class ExtensionTests(unittest.TestCase):
    def test_four_way_conversion_including_zhpy(self):
        from senran.bridge import convert
        source = 'class Box:\n    def value(self):\n        return True\nprint(Box().value())\n'
        plain = convert('zhpy', source)
        body = plain.split('\n', 1)[1]
        self.assertIn('類別 Box:', body)
        self.assertIn('定義 value(我):', body)
        self.assertIn('返回 真', body)
        self.assertIn('印出(', body)
        self.assertEqual(convert('reverse', plain), source)
        self.assertEqual(convert('markdown-reverse', convert('format', plain)), source)
        classical = convert('transcribe', plain)
        self.assertIn('術 ', classical.split('\n', 1)[1])
        self.assertEqual(convert('reverse', convert('zhpy', classical)), source)
        with self.assertRaises(ValueError):
            convert('zhpy', classical.replace('真', '假'))
    def test_format_does_not_reseal_modified_packet(self):
        from senran.bridge import convert
        encoded = convert('transcribe', 'x = 1\n')
        with self.assertRaises(ValueError):
            convert('format', encoded.replace(' = 1', ' = 2'))

    @unittest.skipUnless(shutil.which('node'), '需要 Node.js 考校擴充介面')
    def test_registered_commands_convert_all_four_targets(self):
        root = Path(__file__).resolve().parents[1]
        script = r'''
const assert = require('node:assert/strict');
const Module = require('module');
const load = Module._load;
const commands = new Map();
const source = 'class Box:\n    def value(self):\n        return 3\n';
const document = {value: source, languageId: 'python', version: 1,
  getText() { return this.value; }, positionAt(n) { return n; }};
const editor = {document, selection: {isEmpty: true},
  async edit(callback) { callback({replace(range, value) { document.value = value; document.version++; }}); }};
let opened;
const vscode = {CompletionItemKind: {}, Range: class {}, ViewColumn: {Beside: 2},
  languages: {registerCompletionItemProvider() {}, registerHoverProvider() {}},
  commands: {registerCommand(name, fn) { commands.set(name, fn); }},
  workspace: {getConfiguration() { return {get() {return 'python3';}}; },
    async openTextDocument(options) { opened = options.content; return options; }},
  window: {activeTextEditor: editor, showWarningMessage() {}, showInformationMessage() {},
    showErrorMessage(message) {throw Error(message);}, async showTextDocument() {}}};
Module._load = function(name, ...args) { return name === 'vscode' ? vscode : load.call(this, name, ...args); };
require('./vscode-extension/extension.js').activate({subscriptions: []});
(async () => {
  await commands.get('senran.toZhpy')();
  assert.match(document.value, /類別 Box:/);
  await commands.get('senran.transcribe')();
  assert.match(document.value, /類 /);
  assert.match(document.value, /術 /);
  await commands.get('senran.formatPianwen')();
  document.value = opened; document.languageId = 'markdown'; document.version++;
  await commands.get('senran.formatPianwen')();
  document.value = opened;
  await commands.get('senran.toStandardPy')();
  assert.equal(document.value, source);
})();
'''
        subprocess.run(['node', '-e', script], cwd=root, check=True, capture_output=True, text=True)

    @unittest.skipUnless(shutil.which('node'), '需要 Node.js 考校擴充介面')
    def test_node_python_roundtrip(self):
        root = Path(__file__).resolve().parents[1]
        script = r'''
const assert = require('node:assert/strict');
const Module = require('module');
const load = Module._load;
Module._load = function(name, ...args) {
  if (name === 'vscode') return { CompletionItemKind: {}, workspace: {
    getConfiguration() { return { get() { return 'python3'; } }; }
  }};
  return load.call(this, name, ...args);
};
const {convertCode} = require('./vscode-extension/extension.js');
(async () => {
  const source = '# print(True)\r\nprint("True", 1)';
  const elegant = await convertCode('transcribe', source);
  const plain = await convertCode('zhpy', elegant);
  assert.equal(await convertCode('reverse', plain), source);
  const poem = await convertCode('format', elegant);
  assert.equal(await convertCode('unformat', poem), elegant);
  assert.equal(await convertCode('markdown-reverse', poem), source);
  await assert.rejects(convertCode('invalid', source));
  await assert.rejects(convertCode('reverse', elegant.replace(' 1)', ' 2)')));
})();
'''
        subprocess.run(['node', '-e', script], cwd=root, check=True, capture_output=True, text=True)

    def test_context_menu_without_title_buttons(self):
        path = Path(__file__).resolve().parents[1] / 'vscode-extension' / 'package.json'
        package = json.loads(path.read_text())
        menus = package['contributes']['menus']
        self.assertNotIn('editor/title', menus)
        self.assertEqual({item['command'] for item in menus['editor/context']},
                         {'senran.toZhpy', 'senran.transcribe', 'senran.toStandardPy', 'senran.formatPianwen'})
