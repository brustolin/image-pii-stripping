import cv2
import pytesseract

from .pii import is_pii


class OcrOnlyStripper:
    def __init__(self, input, output=None):
        self.input = input
        self.output = output or f"outputs/redacted-ocr-{input.split('/')[-1]}"
        self.input_img = cv2.imread(input)
        self.output_img = self.input_img.copy()

    def strip(self):
        boxes = pytesseract.image_to_data(self.input_img, output_type="dict")

        for i in range(len(boxes["level"])):
            # level mapping: 1 - page, 2 - block, 3 - paragraph, 4 - line, 5 - word
            # take only words
            if boxes["level"][i] != 5:
                continue

            # filter empty text
            text = boxes["text"][i].strip()
            if not text:
                continue

            # find other words in same line
            line_words = [v for j, v in enumerate(boxes["text"]) if boxes["level"][j] == 5 and
                    boxes["page_num"][j] == boxes["page_num"][j] and
                    boxes["block_num"][j] == boxes["block_num"][i] and
                    boxes["par_num"][j] == boxes["par_num"][i] and
                    boxes["line_num"][j] == boxes["line_num"][i]]

            line_text = "".join(line_words)

            # draw rectangles over pii
            # we check both the word and the reconstructed line that word belongs to for pii
            if is_pii(text) or is_pii(line_text):
                x = boxes["left"][i]
                y = boxes["top"][i]
                w = boxes["width"][i]
                h = boxes["height"][i]

                cv2.rectangle(self.output_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

        cv2.imwrite(self.output, self.output_img)
