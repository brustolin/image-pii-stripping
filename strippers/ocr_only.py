import cv2
import pytesseract


class OcrOnlyStripper:
    def __init__(self, input, output=None):
        self.input = input
        self.output = output or f"outputs/redacted-ocr-{input.split('/')[-1]}"
        self.input_img = cv2.imread(input)
        self.output_img = self.input_img.copy()

    def strip(self):
        cv2.imwrite(self.output, self.output_img)

