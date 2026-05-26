import hashlib

pdf_path = "hello_iago.pdf"

sha256_hash = hashlib.sha256()

with open(pdf_path, "rb") as f:
    for block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(block)

file_hash = sha256_hash.hexdigest()

print("SHA-256:", file_hash)