import unittest
import pathlib
from os import readlink
from model.entity import Entity
from utils.utils import get_file_hash, is_file_readable, check_file_readability_get_entities
from inventory_tool.inventory_tool import InventoryTool

cwd = str(pathlib.Path().absolute())
relative_directory_path = "/tests/test_files/"


def checkEqualityOfEntity(obj1: Entity, obj2: Entity) -> bool:
    return obj1.path == obj2.path and obj1.type == obj2.type and obj1.hash == obj2.hash and obj1.readable == obj2.readable and obj1.link == obj2.link


class TestGetFileHash(unittest.TestCase):
    def test_get_file_hash_success(self):
        expected = get_file_hash(cwd+relative_directory_path+"test_file.txt")
        self.assertEqual(
            "4798a09d73aa1288a84163b06004ec0e4f933418fd945809c546f8f1e5f02e3e", str(expected))

    def test_get_file_hash_None(self):
        expected = get_file_hash(
            cwd+relative_directory_path+"test_file_non_existant.txt")
        self.assertEqual("", expected)


class TestIdFileReadable(unittest.TestCase):
    def test_is_file_readable_success(self):
        expected = is_file_readable(
            cwd+relative_directory_path+"test_file.txt")
        self.assertEqual(True, expected)

    def test_is_file_readable_file_nonexistant(self):
        expected = is_file_readable(
            cwd+relative_directory_path+"test_file_non_existant.txt")
        self.assertEqual(False, expected)

    def test_is_file_readable_file_nonreadable(self):
        expected = is_file_readable(
            cwd+relative_directory_path+"test_file_non_existant.txt")
        self.assertEqual(False, expected)


class TestCheckFileReadailityGetEntities(unittest.TestCase):

    def test_check_file_readability_get_entities_success(self):
        folder_path = "."+relative_directory_path
        folder_entity = Entity(folder_path+"test_empty_folder", "folder")
        filesNames = [{"name": "test_file_link", "type": "symlink"}, {
            "name": "test_file.txt", "type": "file"}, {"name": "unreadable_file.txt", "type": "file"}]
        expected_symlinks = []
        expected_files = []
        for x in filesNames:
            path = folder_path+f"{x['name']}"
            if x["type"] == "symlink":
                expected_symlinks.append(
                    Entity(path, "symlink", readable=readlink(path)))
            else:
                expected_files.append(
                    Entity(path, "file", get_file_hash(path)))

        actual_folders, actual_files, actual_symlinks = check_file_readability_get_entities(
            Entity(folder_path, "folder"))

        self.assertTrue(checkEqualityOfEntity(folder_entity, actual_folders[0]))
        self.assertTrue(checkEqualityOfEntity(expected_symlinks[0], actual_symlinks[0]))
        self.assertTrue(checkEqualityOfEntity(expected_files[0], actual_files[0]))
        self.assertTrue(checkEqualityOfEntity(expected_files[1], actual_files[1]))

    def test_check_file_readability_get_entities_wrong_directory(self):
        folder_path = "./fake_directory"
        folder_entity = Entity(folder_path, "folder")

        actual_folders, actual_files, actual_symlinks = check_file_readability_get_entities(folder_entity)
        self.assertEqual(len(actual_files),0)
        self.assertEqual(len(actual_symlinks),0)
        self.assertEqual(len(actual_folders),0)
    

class TestCompareReports(unittest.TestCase):
    def test_check_file_readability_get_entities_success(self):
        folder_path = cwd+"/tests/test_captures"
        tool = InventoryTool()
        expected_output = ['File ./README.md is different\ncapture1 hash: 5779f026afd93091a16f091e39698e9ae94f58343bd97cdc9bf01433c5281aa4\ncapture2 hash: 33ce2feeb372b8708fee0313d56ef959781362835f4adf04172ac555ea975389\n', 'File ./capture1 exists in capture2 but not capture1\n', 'Folder ./extra_folder exists in capture2 but not capture1\n']
        actual_output = tool.compare_reports(folder_path+"/capture1", folder_path+"/capture2")
        self.assertEqual(actual_output, expected_output)

    def test_generate_folder_report_success(self):
        folder_path = "./tests/test_files"
        tool = InventoryTool()
        expected_output = ["./tests/test_files", "./tests/test_files/test_empty_folder", "./tests/test_files/test_file.txt", "./tests/test_files/unreadable_file.txt"]
        actual_output = tool.generate_folder_report(folder_path, cwd+"/tests/test_captures/capture3")
        for i in range(len(actual_output)):
            self.assertEqual(actual_output[i].path, expected_output[i])

if __name__ == '__main__':
    unittest.main()
