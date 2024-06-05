from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Gera a chave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Gera a chave pública
public_key = private_key.public_key()

# Salva a chave privada em um arquivo
with open("private_key.pem", "wb") as private_file:
    private_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Salva a chave pública em um arquivo
with open("public_key.pem", "wb") as public_file:
    public_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Chaves RSA geradas e salvas com sucesso.")
