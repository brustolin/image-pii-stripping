import boto3
import cv2

from .pii import is_pii, is_name_or_address

class AWSStripper:
    def __init__(self, input, output=None):
        self.input = input
        self.output = output or f"outputs/redacted-aws-{input.split('/')[-1]}"
        self.input_img = cv2.imread(input)
        self.output_img = self.input_img.copy()
        f = open(".env", "r")
        key_secret = f.read().split("=")
        self.key = key_secret[0]
        self.secret = key_secret[1]

    def strip(self):
        with open(self.input, 'rb') as document:
            imageBytes = bytearray(document.read())

        # Amazon Textract client
        textract = boto3.client('textract', region_name = 'us-east-2',aws_access_key_id=self.key, aws_secret_access_key=self.secret)

        # Call Amazon Textract
        response = textract.detect_document_text(Document={'Bytes': imageBytes})

        img_height = self.input_img.shape[0]
        img_width = self.input_img.shape[1]

        # Print detected text
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text = item["Text"]
                if (
                    is_pii(text)
                    or is_name_or_address(text)
                ):
                    rect = item["Geometry"]["BoundingBox"]
                    x = int(rect["Left"] * img_width)
                    y = int(rect["Top"] * img_height)
                    w = int(rect["Width"] * img_width)
                    h = int(rect["Height"] * img_height)

                    cv2.rectangle(self.output_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

        cv2.imwrite(self.output, self.output_img)
                