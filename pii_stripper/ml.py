from doctr.io import DocumentFile

class MLStripper:
    def __init__(self, input, output=None):
        self.input = input
        self.output = output or f"outputs/redacted-ocr-{input.split('/')[-1]}"

    def strip(self):
        # Image
        single_img_doc = DocumentFile.from_images(self.input)

