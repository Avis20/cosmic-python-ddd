# ./src/etc/sync.py

import sys
import os
import shutil
import hashlib

from pathlib import Path


class FileSystem:

    BLOCKSIZE = 65536

    def copy(self, src, dest):
        shutil.copy(src, dest)

    def move(self, src, dest):
        shutil.move(src, dest)

    def delete(self, src):
        os.remove(src)

    def read(self, root):
        return self._read_paths_and_hashes(root)

    def _read_paths_and_hashes(self, root):
        """Функция формирования словаря хешей и названий файлов"""
        hashes = {}
        for folder, _, files in os.walk(root):
            for file in files:
                hashes[self._hash_file(Path(folder) / file)] = file
        return hashes

    def _hash_file(self, path: Path):
        """Функция получения хеша файла"""
        hasher = hashlib.sha256()
        with path.open("rb") as file:
            buf = file.read(self.BLOCKSIZE)
            while buf:
                hasher.update(buf)
                buf = file.read(self.BLOCKSIZE)
        return hasher.hexdigest()


def determine_action(
    source_hashes: dict[str, str],
    dest_hashes: dict[str, str],
    source_folder: str,
    dest_folder: str,
):
    """Функция определения действия над файлом: скопировать/перенести/удалить"""
    for src_hash, file_name in source_hashes.items():
        if src_hash not in dest_hashes:
            source_path = Path(source_folder) / file_name
            dest_path = Path(dest_folder) / file_name
            yield "COPY", source_path, dest_path

        elif file_name != dest_hashes[src_hash]:
            old_dest_path = Path(dest_folder) / dest_hashes[src_hash]
            new_dest_path = Path(dest_folder) / file_name
            yield "MOVE", old_dest_path, new_dest_path

    for dst_hash, file_name in dest_hashes.items():
        if dst_hash not in source_hashes:
            yield "DELETE", Path(dest_folder) / file_name


def sync(source, dest, file_system=FileSystem()):

    # 1. Формируем словарь хешей и файлов
    source_hashes = file_system.read(source)
    dest_hashes = file_system.read(dest)

    # 2. Вызываем функциональное ядро - определение действий над файлами
    actions = determine_action(source_hashes, dest_hashes, source, dest)

    # 3. Применить действия над файлами
    for action, *paths in actions:
        if action == "COPY":
            file_system.copy(*paths)
        if action == "MOVE":
            file_system.move(*paths)
        if action == "DELETE":
            file_system.delete(*paths)

if __name__ == '__main__':
    source = sys.argv[1]
    dest = sys.argv[2]
    sync(source, dest)
