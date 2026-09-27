"""整庫搬卷的檔案完整性考校；不執行參考專案。"""
import os
import tempfile
import unittest
from pathlib import Path

from senran.codec import encode_names, decode_source


class RepositoryTests(unittest.TestCase):
    def test_whole_repository_zhpy_roundtrip(self):
        from senran.repository import convert_repository
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            original = b'def f():\r\n    return 3\r\n'
            (source / 'a.py').write_bytes(original)
            previous = source
            for mode in ('encode', 'format', 'unformat', 'decode'):
                destination = root / mode
                convert_repository(previous, destination, mode, style='zhpy')
                previous = destination
                if mode == 'encode':
                    self.assertIn('定義 f():', (destination / 'a.py').read_text())
            self.assertEqual((previous / 'a.py').read_bytes(), original)

    def test_cli_markdown_chain_preserves_newlines(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original, poem, elegant, restored = [root / name for name in ('original.py', 'poem.md', 'elegant.py', 'restored.py')]
            original.write_bytes(b'print(1)\r\n')
            for args in [('format', original, '-o', poem), ('unformat', poem, '-o', elegant),
                         ('to-py', elegant, '-o', restored)]:
                subprocess.run([sys.executable, '-c', 'from senran.transcriber import main; main()', *map(str, args)],
                               check=True, capture_output=True, text=True)
            self.assertEqual(restored.read_bytes(), original.read_bytes())
            run = subprocess.run([sys.executable, '-c', 'from senran.transcriber import main; main()', 'run', str(poem)],
                                 check=True, capture_output=True, text=True)
            self.assertEqual(run.stdout, '1\n')

    def test_marker_shaped_original_comment(self):
        source = '# senran-source-v1 ordinary comment\nvalue = 1\n'
        self.assertEqual(decode_source(encode_names(source)), source)

    def test_manifest_cannot_write_through_symlink(self):
        import json
        from senran.repository import convert_repository, MANIFEST
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            (source / 'a.py').write_text('x = 1\n')
            (source / 'escape').symlink_to(root, target_is_directory=True)
            encoded, formatted = root / 'encode', root / 'format'
            convert_repository(source, encoded, 'encode')
            convert_repository(encoded, formatted, 'format')
            manifest = json.loads((formatted / MANIFEST).read_text())
            manifest['python'][0]['original'] = 'escape/stolen.py'
            (formatted / MANIFEST).write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                convert_repository(formatted, root / 'output', 'unformat')
            self.assertFalse((root / 'stolen.py').exists())

    def test_manifest_collision_does_not_overwrite(self):
        import json
        from senran.repository import convert_repository, MANIFEST
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            (source / 'a.py').write_text('x = 1\n')
            encoded, formatted = root / 'encode', root / 'format'
            convert_repository(source, encoded, 'encode')
            convert_repository(encoded, formatted, 'format')
            (formatted / 'a.py').write_text('keep\n')
            with self.assertRaises(ValueError):
                convert_repository(formatted, root / 'output', 'unformat')
            self.assertFalse((root / 'output').exists())
    def test_deliberately_invalid_python_fixture(self):
        source = 'value = 1\n"unfinished\nafter = 2\n'
        encoded = encode_names(source)
        self.assertEqual(decode_source(encoded), source)
        self.assertNotIn('after', encoded.split('\n', 1)[1])

    def test_form_feeds_are_not_line_breaks(self):
        source = 'before = 1\n\f\nafter = before\n'
        self.assertEqual(decode_source(encode_names(source)), source)

    def test_all_names_are_reversible(self):
        original = 'import abc\nfoo = abc.Bar(foo=1)\nprint(foo)\n'
        encoded = encode_names(original)
        self.assertEqual(decode_source(encoded), original)
        body = encoded.split('\n', 1)[1]
        self.assertNotIn('foo', body)
        self.assertNotIn('abc', body)

    def test_modified_code_is_rejected(self):
        encoded = encode_names('x = 1\n')
        with self.assertRaises(ValueError):
            decode_source(encoded.replace(' = 1', ' = 2'))

    def test_full_tree_roundtrip(self):
        from senran.repository import convert_repository
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source'
            source.mkdir()
            fixtures = {
                'a.py': b'# coding: latin-1\r\nx = "caf\xe9"\r\n',
                'b.py': b'\xef\xbb\xbfprint(1)',
                'bad.py': b'# coding: utf-8\nx = "\xff"\n',
                'a.py.md': b'original markdown\n',
                'data.bin': bytes(range(256)),
                'README.md': b'hello\n',
            }
            for name, data in fixtures.items():
                (source / name).write_bytes(data)
            (source / 'empty').mkdir()
            os.chmod(source / 'b.py', 0o755)
            (source / 'link').symlink_to('a.py')
            for mode, left, right in [('encode', 'source', 'elegant'),
                                      ('format', 'elegant', 'poem'),
                                      ('unformat', 'poem', 'decoded'),
                                      ('decode', 'decoded', 'restored')]:
                convert_repository(root / left, root / right, mode)
            restored = root / 'restored'
            for name, data in fixtures.items():
                self.assertEqual((restored / name).read_bytes(), data)
            self.assertTrue((restored / 'empty').is_dir())
            self.assertEqual(os.readlink(restored / 'link'), 'a.py')
            self.assertEqual((restored / 'b.py').stat().st_mode & 0o777, 0o755)

    def test_destination_cannot_be_source_child(self):
        from senran.repository import convert_repository
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp)
            with self.assertRaises(ValueError):
                convert_repository(source, source / 'output', 'encode')

    def test_existing_destination_is_preserved(self):
        from senran.repository import convert_repository
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'source').mkdir()
            destination = root / 'output'
            destination.mkdir()
            (destination / 'keep').write_text('keep')
            with self.assertRaises(FileExistsError):
                convert_repository(root / 'source', destination, 'encode')
            self.assertEqual((destination / 'keep').read_text(), 'keep')
