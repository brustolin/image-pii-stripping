import os
from base64 import b64encode
from flask import Flask, request, render_template

from pii_stripper.ocr_only import OcrOnlyStripper


UPLOAD_FOLDER = "./uploads"
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def shame():
    error = None
    input_img = None
    output_img = None

    if request.method == "POST":
        if "image_upload" in request.files:
            file = request.files["image_upload"]
            if file.filename:
                input_bytes = file.read()
                output_bytes = OcrOnlyStripper(input_bytes, flask=True).strip()
                input_img = b64encode(input_bytes).decode("utf-8")
                output_img = b64encode(output_bytes).decode("utf-8")
            else:
                error = "No file"
        else:
            error = "No file"

    return render_template("shame.html", error=error, input_img=input_img, output_img=output_img)


if __name__ == "__main__":
    app.run()
