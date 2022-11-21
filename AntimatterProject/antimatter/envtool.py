#!/usr/bin/env python
import argparse
from inventory_tool.inventory_tool import InventoryTool

from sys import argv

def envtool_runner():
    # Parse all the arguments and process to store default values
    parser = argparse.ArgumentParser(description="How to use the script to capture details of folder and compare two captures.",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("action", choices=[
                        'capture', 'compare'], help="capture or compare")

    if (len(argv) <=2 ):
        print("For capture please run as $ python envtool.py capture --outfile capture1")
        print("For compare please run as $ python envtool.py compare ./capture1 ./capture2")

    elif argv[1] == "compare":
        parser.add_argument("capture1", help="file path of first capture file")
        parser.add_argument("capture2", help="file path of second capture file")

    else:
        parser.add_argument("-o", "--outfile",
                        required=True, help="Output filename")

    args = parser.parse_args()
    config = vars(args)

    tool = InventoryTool()

    if config["action"] == "capture":
        tool.generate_folder_report(".", config["outfile"])

    else:
        tool.compare_reports(config["capture1"],config["capture2"])

if __name__ == "__main__":
    """This runs when you execute $python antimatter/envtool"""
    envtool_runner()