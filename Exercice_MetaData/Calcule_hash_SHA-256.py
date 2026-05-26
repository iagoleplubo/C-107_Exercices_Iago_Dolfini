from reportlab.pdfgen import canvas
import hashlib
from web3 import Web3
import json
from dotenv import load_dotenv
import os

# ==================================================
# CHARGEMENT .ENV
# ==================================================

load_dotenv()

# ==================================================
# VARIABLES
# ==================================================

RPC_URL = os.getenv("RPC_URL")

sender_address = os.getenv("SENDER_ADDRESS")

private_key = os.getenv("PRIVATE_KEY")

pdf_url = os.getenv("PDF_URL")

# ==================================================
# CONNEXION BLOCKCHAIN
# ==================================================

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ==================================================
# NOM DU FICHIER PDF
# ==================================================

pdf_filename = "hello_iago.pdf"

# ==================================================
# CREATION DU PDF
# ==================================================

c = canvas.Canvas(pdf_filename)

c.drawString(100, 750, "Hello from Iago to blockchain")

c.save()

print("PDF créé :", pdf_filename)

# ==================================================
# HASH SHA-256 DU PDF
# ==================================================

sha256_hash = hashlib.sha256()

with open(pdf_filename, "rb") as f:
    for block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(block)

file_hash = sha256_hash.hexdigest()

print("SHA-256 :", file_hash)

# ==================================================
# METADATA
# ==================================================

metadata = {
    "pdf": pdf_url,
    "hash": file_hash
}

metadata_json = json.dumps(metadata)

metadata_hex = metadata_json.encode().hex()

print("\n=== METADATA ===")
print(metadata)

# ==================================================
# TRANSACTION
# ==================================================

nonce = w3.eth.get_transaction_count(sender_address)

transaction = {
    'from': sender_address,
    'to': "0x0000000000000000000000000000000000000000",
    'value': 0,
    'gas': 200000,
    'gasPrice': w3.to_wei('20', 'gwei'),
    'nonce': nonce,
    'chainId': 32383,
    'data': '0x' + metadata_hex
}

# ==================================================
# SIGNATURE
# ==================================================

signed_txn = w3.eth.account.sign_transaction(
    transaction,
    private_key
)

# ==================================================
# ENVOI TRANSACTION
# ==================================================

tx_hash = w3.eth.send_raw_transaction(
    signed_txn.raw_transaction
)

tx_hash_hex = tx_hash.hex()

print("\n=== TRANSACTION ENVOYEE ===")
print("TX HASH :", tx_hash_hex)

# ==================================================
# RECUPERATION DES DATAS DEPUIS LA BLOCKCHAIN
# ==================================================

tx = w3.eth.get_transaction(tx_hash_hex)

data_hex = tx.input.hex()

decoded_data = bytes.fromhex(data_hex[2:]).decode()

print("\n=== DONNEES RECUPEREES DE LA BLOCKCHAIN ===")
print(decoded_data)

# ==================================================
# VERIFICATION HASH
# ==================================================

verification_hash = hashlib.sha256()

with open(pdf_filename, "rb") as f:
    for block in iter(lambda: f.read(4096), b""):
        verification_hash.update(block)

new_hash = verification_hash.hexdigest()

print("\n=== VERIFICATION ===")

if new_hash == file_hash:
    print("Le fichier est valide.")
else:
    print("Le fichier a été modifié.")