from PyPDF2 import PdfReader
from pathlib import Path

import codecs


def clean_pdf_field(value):
    if isinstance(value, str):
        # Handle UTF-16-encoded values
        if value.startswith(r"/\376\377"):
            try:
                # Remove the leading slash
                raw = value[1:]
                # Convert escaped unicode into actual bytes
                raw_bytes = codecs.decode(
                    raw.encode("latin1"), "unicode_escape"
                ).encode("latin1")
                # Decode UTF-16-BE
                decoded = codecs.decode(raw_bytes, "utf-16")
                return decoded.strip()
            except Exception as e:
                print("Decode error:", e)
                return value
        elif value.startswith("/"):
            stripped = value[1:]
            if stripped.lower() == "yes":
                return True
            elif stripped.lower() == "off":
                return False
            return stripped

    return value


def analysePDF(filePath: Path, OutputClass=None):
    reader = PdfReader(filePath)
    fields = reader.get_fields()

    data = {}
    for field in fields:
        valueRaw = fields[field].get("/V")
        value = clean_pdf_field(valueRaw)
        print(f"{field}: {value} {type(value)}")
        data[field] = value

    if OutputClass:
        return OutputClass(**data)

    return data
