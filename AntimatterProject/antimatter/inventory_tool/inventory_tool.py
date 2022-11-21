import pickle
from collections import deque
from model.entity import Entity
from utils.utils import check_file_readability_get_entities

class InventoryTool:
    def __init__(self):
        print("Inventory Tool object initialized")

    def generate_folder_report(self, path: str, out_filename: str) -> None:
        file_folder_list = [Entity(path, "folder")]
        files_count = 0
        symlinks_count = 0
        
        stack = deque([Entity(path, "folder")])
        while len(stack) != 0:
            folder = stack.popleft()
            new_folders, new_files, symlinks = check_file_readability_get_entities(
                folder)
            stack.extend(new_folders)
            file_folder_list += new_folders + new_files
            # Count files and symlinks
            files_count += len(new_files)
            symlinks_count += len(symlinks)
        # Write report log
        print(f"{files_count} files captured\n")
        print(f"{symlinks_count} symlinks captured\n")
        file_folder_list.sort()

        for entity in file_folder_list:
            if (entity.type == "folder" and entity.readable == False):
                print(f"could not traverse into:\n\t{entity.path}\n")
            elif (entity.type == "file" and entity.readable == False):
                print(f"could not read:\n\t{entity.path}\n")
        try:
            report_file = open(out_filename, "wb")
        except IOError:
            print(
                "Could not open file! Please retry afer checking memory requirements.")
            return
        pickle.dump(file_folder_list, report_file)
        report_file.close()
        return file_folder_list

    def compare_reports(self, report_path_1: str, report_path_2: str) -> list:
        output = []
        with open(report_path_1, "rb") as report_1:
            list_1 = pickle.load(report_1)

        with open(report_path_2, "rb") as report_2:
            list_2 = pickle.load(report_2)

        len_1 = len(list_1)
        len_2 = len(list_2)
        counter_1 = 0
        counter_2 = 0
        while counter_1 < len_1 and counter_2 < len_2:
            elm_1 = list_1[counter_1]
            elm_2 = list_2[counter_2]
            if (elm_1.path == elm_2.path):
                # If files have changed
                if (elm_1.type == elm_2.type and elm_1.type == "file" and elm_1.hash != elm_2.hash):
                    msg = f"File {elm_1.path} is different\ncapture1 hash: {elm_1.hash}\ncapture2 hash: {elm_2.hash}\n"
                    output.append(msg)
                    print(msg)
                # If symlinks have changed
                elif (elm_1.type == elm_2.type and elm_1.type == "symlink" and elm_1.link != elm_2.link):
                    msg = f"Symlink {elm_1.path} is different\ncapture1 target: {elm_1.link}\ncapture2 hash: {elm_2.link}\n"
                    output.append(msg)
                    print(msg)                
                counter_1 += 1
                counter_2 += 1
            elif (elm_1.path > elm_2.path):
                msg = f"{elm_2.type.capitalize()} {elm_2.path} exists in capture2 but not capture1\n"
                output.append(msg)
                print(msg)
                counter_2 += 1
            else:
                msg = f"{elm_1.type.capitalize()} {elm_1.path} exists in capture1 but not capture2\n"
                output.append(msg)
                print(msg)
                counter_1 += 1

        while counter_1 < len_1:
            elm_1 = list_1[counter_1]
            msg = f"{elm_1.type.capitalize()} {elm_1.path} exists in capture1 but not capture2\n"
            output.append(msg)
            print(msg)
            counter_1 += 1

        while counter_2 < len_2:
            elm_2 = list_2[counter_2]
            msg = f"{elm_2.type.capitalize()} {elm_2.path} exists in capture2 but not capture1\n"
            output.append(msg)
            print(msg)
            counter_2 += 1
        
        return output
