#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
import sys
from strippers.contour import ContourStripper
from strippers.ocr_only import OcrOnlyStripper

if len(sys.argv) < 2:
    print("Usage: python . input_image [algo]")
    print("\tValid algos: contour ocr")
    sys.exit()

input = sys.argv[1]

algo = None
if len(sys.argv) > 2:
    algo = sys.argv[2]

if algo == "ocr":
    OcrOnlyStripper(input).strip()
else:
    ContourStripper(input).strip()
