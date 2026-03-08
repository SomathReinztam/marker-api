import requests
import os
import sys

API_URL = "http://localhost:8000/convert"


def convert_pdf(pdf_path):

    if not os.path.exists(pdf_path):
        print("PDF no encontrado")
        return

    with open(pdf_path, "rb") as f:
        files = {
            "pdf_file": (os.path.basename(pdf_path), f, "application/pdf")
        }

        response = requests.post(API_URL, files=files)

    if response.status_code != 200:
        print("Error:", response.text)
        return

    data = response.json()

    markdown = data["markdown"]

    output_file = pdf_path.replace(".pdf", ".md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print("Markdown guardado en:", output_file)


if __name__ == "__main__":
    pdf_file = sys.argv[1]
    convert_pdf(pdf_file)