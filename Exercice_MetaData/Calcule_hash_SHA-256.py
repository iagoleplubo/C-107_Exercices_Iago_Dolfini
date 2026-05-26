from reportlab.pdfgen import canvas
import hashlib


# NOM DU FICHIER PDF

pdf_filename = "hello_iago.pdf"


# CREATION DU PDF

c = canvas.Canvas(pdf_filename)

c.drawString(100, 750, "Hello from Iago to blockchain")

c.save()

print("PDF créé :", pdf_filename)


# HASH SHA-256 DU PDF

sha256_hash = hashlib.sha256()

with open(pdf_filename, "rb") as f:
    for block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(block)

file_hash = sha256_hash.hexdigest()

print("SHA-256 :", file_hash)