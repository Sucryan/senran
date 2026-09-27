"""編輯器實際呼叫共用轉錄介面的考校。"""
import json
import shutil
import subprocess
import unittest
from pathlib import Path


class ExtensionTests(unittest.TestCase):
    def test_format_does_not_reseal_modified_packet(self):
        from senran.bridge import convert
        encoded = convert('transcribe', 'x = 1\n')
        with self.assertRaises(ValueError):
            convert('format', encoded.replace(' = 1', ' = 2'))

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
                         {'senran.transcribe', 'senran.toStandardPy', 'senran.formatPianwen'})
