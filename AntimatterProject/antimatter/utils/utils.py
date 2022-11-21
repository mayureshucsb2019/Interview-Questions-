import hashlib
from os import listdir, readlink
from os.path import isfile, join, islink
from model.entity import Entity


def get_file_hash(filepath: str) -> str:
    """
    Takes input as filepath and outputs hash if file exits, else outputs ""
    """
    try:
        with open(filepath, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest()
    except FileNotFoundError:
        return ""
    return readable_hash


def is_file_readable(filepath: str) -> bool:
    """
    Function takes filepath as input and returns true if file is readable, else false.
    """
    try:
        with open(filepath, "r") as f:
            isReadable = f.readable()
    except FileNotFoundError:
        return False
    return isReadable


def check_file_readability_get_entities(folder: Entity) -> tuple[list:Entity, list:Entity, list:Entity]:
    """
    Takes as input entity representation of a folder and outputs list of entities of folders, files, symlinks
    """
    folders = []
    files = []
    symlinks = []
    try:
        entries = listdir(folder.path)
    except Exception:
        folder.readable = False
        return folders, files, symlinks

    for name in entries:
        name_path = join(folder.path, name)
        if islink(name_path):
            link_entity = Entity(name_path, "symlink",
                                 readable=readlink(name_path))
            symlinks.append(link_entity)
        elif isfile(name_path):
            file_hash = get_file_hash(name_path)
            file_entity = Entity(name_path, "file", file_hash)
            if (not is_file_readable(name_path)):
                file_entity.readable = False
            files.append(file_entity)
        else:
            folder_entity = Entity(name_path, "folder")
            folders.append(folder_entity)
    return folders, files, symlinks
