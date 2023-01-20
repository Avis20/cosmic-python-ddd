# ./tests/etc/test_sync.py

from pathlib import Path
from tempfile import mkdtemp
from shutil import rmtree

from src.etc.sync import determine_action, sync


class FakeFileSystem:
    def __init__(self, path_hashes):
        self.path_hashes = path_hashes
        self.actions = []

    def read(self, path):
        return self.path_hashes.get(path)

    def copy(self, src, dest):
        self.actions.append(["COPY", src, dest])

    def move(self, src, dest):
        self.actions.append(["MOVE", src, dest])

    def delete(self, src):
        self.actions.append(["DELETE", src])


class TestWithFakeFileSystem:
    @staticmethod
    def test_fake_copy():
        fake_fs = FakeFileSystem({"/src/": {"hash1": "file1"}, "/dest/": {}})
        sync("/src/", "/dest/", file_system=fake_fs)
        assert fake_fs.actions == [["COPY", Path("/src/file1"), Path("/dest/file1")]]

    @staticmethod
    def test_fake_move():
        fake_fs = FakeFileSystem(
            {
                '/src/': {'hash1': 'file1'},
                '/dest/': {'hash1': 'file2'},
            }
        )
        sync("/src/", "/dest/", file_system=fake_fs)
        assert fake_fs.actions == [["MOVE", Path("/dest/file2"), Path("/dest/file1")]]

    @staticmethod
    def test_fake_remove():
        fake_fs = FakeFileSystem(
            {
                '/src/': {'hash1': 'file1'},
                '/dest/': {'hash1': 'file1', 'hash2': 'file2'},
            }
        )
        sync("/src/", "/dest/", file_system=fake_fs)
        assert fake_fs.actions == [["DELETE", Path("/dest/file2")]]


class TestDetermineAction:
    @staticmethod
    def test_determine_action_copy():
        source_hashes = {"hash1": "file1"}
        dest_hashes = {}
        actions = determine_action(source_hashes, dest_hashes, "/src", "/dest")
        assert list(actions) == [("COPY", Path("/src/file1"), Path("/dest/file1"))]

    @staticmethod
    def test_determine_action_delete():
        source_hashes = {"hash1": "file1"}
        dest_hashes = {"hash1": "file1", "hash2": "file2"}
        actions = determine_action(source_hashes, dest_hashes, "/src", "/dest")
        assert list(actions) == [("DELETE", Path("/dest/file2"))]

    @staticmethod
    def test_determine_action_copy_and_delete():
        source_hashes = {"hash1": "file1"}
        dest_hashes = {"hash2": "file2"}
        actions = determine_action(source_hashes, dest_hashes, "/src", "/dest")
        assert list(actions) == [
            ("COPY", Path("/src/file1"), Path("/dest/file1")),
            ("DELETE", Path("/dest/file2")),
        ]

    @staticmethod
    def test_determine_action_move():
        source_hashes = {"hash1": "file1"}
        dest_hashes = {"hash1": "file2"}
        actions = determine_action(source_hashes, dest_hashes, "/src", "/dest")
        assert list(actions) == [("MOVE", Path("/dest/file2"), Path("/dest/file1"))]


class TestE2E:
    @staticmethod
    def test_create_file_in_dist():
        try:
            source = mkdtemp()
            dest = mkdtemp()

            content = "Hello, World!"
            source_file = Path(source) / "hello.txt"
            source_file.write_text(content)

            sync(source, dest)

            dest_file = Path(dest) / "hello.txt"
            assert dest_file.exists()
            assert dest_file.read_text() == content

        finally:
            rmtree(source)
            rmtree(dest)

    @staticmethod
    def test_when_file_renamed():
        try:
            source = mkdtemp()
            dest = mkdtemp()

            content = "Я - файл который переименовали"
            source_file = Path(source) / "source.txt"
            source_file.write_text(content)

            old_dest_file = Path(dest) / "old-dest.txt"
            old_dest_file.write_text(content)

            sync(source, dest)

            dest_file = Path(dest) / "source.txt"
            assert old_dest_file.exists() is False
            assert dest_file.exists()
            assert dest_file.read_text() == content

        finally:
            rmtree(source)
            rmtree(dest)
