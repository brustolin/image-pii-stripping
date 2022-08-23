import cv2
import pytesseract


class ContourStripper:
    def __init__(self, input, output=None):
        self.input = input
        self.output = output or f"outputs/redacted-contour-{input.split('/')[-1]}"
        self.input_img = cv2.imread(input)
        self.output_img = self.input_img.copy()

    def strip(self):
        # Convert the image to gray scale
        gray = cv2.cvtColor(self.input_img, cv2.COLOR_BGR2GRAY)
        
        #blurried image
        blurried = cv2.blur(self.input_img, (30, 30))

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_NONE)
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then written into the text file
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # Cropping the text block for giving input to OCR
            cropped = self.output_img[y:y + h, x:x + w]

            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)

            if text.strip():
                print(f"{text} = {{{x},{y},{w},{h}}}\n")
                #blurring the text square
                self.output_img[y:y + h, x:x + w] = blurried[y:y + h, x:x + w]

        cv2.imwrite(self.output, self.output_img)

