import random
import os
from datetime import datetime
from OpenSSL import crypto


def create_ca(root_ca_path, key_path, common_name, email_address):
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 4096)

    ca_cert = crypto.X509()
    ca_cert.set_version(2)
    ca_cert.set_serial_number(random.randint(50000000, 100000000))

    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = common_name
    ca_subj.emailAddress = email_address

    ca_cert.set_issuer(ca_subj)
    ca_cert.set_pubkey(ca_key)

    ca_cert.add_extensions([
        crypto.X509Extension(b"subjectKeyIdentifier",
                             False, b"hash", subject=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension(b"authorityKeyIdentifier",
                             False, b"keyid:always,issuer", issuer=ca_cert),
    ])

    ca_cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
    ])

    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(10*365*24*60*60)

    ca_cert.sign(ca_key, 'sha256')

    # Save certificate
    with open(root_ca_path, "wt") as f:
        f.write(crypto.dump_certificate(
            crypto.FILETYPE_PEM, ca_cert).decode("utf-8"))

    # Save private key
    with open(key_path, "wt") as f:
        f.write(crypto.dump_privatekey(
            crypto.FILETYPE_PEM, ca_key).decode("utf-8"))


def load_ca(root_ca_path, key_path):
    with open(root_ca_path, "r") as f:
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
    with open(key_path, "r") as f:
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
    return ca_cert, ca_key


def verify_ca(ca_cert):
    ca_expiry = datetime.strptime(
        str(ca_cert.get_notAfter(), 'utf-8'), "%Y%m%d%H%M%SZ")
    now = datetime.now()
    validity = (ca_expiry - now).days
    return validity


# Creates client certificate
def create_cert(ca_cert, ca_subj, ca_key, client_cn):
    client_key = crypto.PKey()
    client_key.generate_key(crypto.TYPE_RSA, 4096)

    client_cert = crypto.X509()
    client_cert.set_version(2)
    client_cert.set_serial_number(random.randint(50000000, 100000000))

    client_subj = client_cert.get_subject()
    client_subj.commonName = client_cn

    client_cert.set_issuer(ca_subj)
    client_cert.set_pubkey(client_key)

    client_cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b"authorityKeyIdentifier",
                             False, b"keyid", issuer=ca_cert),
        crypto.X509Extension(
            b"keyUsage", True, b"digitalSignature, keyEncipherment"),
    ])

    client_cert.add_extensions([
        crypto.X509Extension(b"subjectKeyIdentifier", False,
                             b"hash", subject=client_cert),
    ])

    client_cert.gmtime_adj_notBefore(0)
    client_cert.gmtime_adj_notAfter(365*24*60*60)

    client_cert.sign(ca_key, 'sha256')

    with open(client_cn + ".crt", "wt") as f:
        f.write(crypto.dump_certificate(
            crypto.FILETYPE_PEM, client_cert).decode("utf-8"))

    with open(client_cn + ".key", "wt") as f:
        f.write(crypto.dump_privatekey(
            crypto.FILETYPE_PEM, client_key).decode("utf-8"))


def main():
    ca_dir = "ca"

    key_path = "./ca/ca.key"
    root_ca_path = "ca/ca.crt"

    if not os.path.exists(ca_dir):
        os.makedirs(ca_dir)

    common_name = "name"
    email_address = "name@email.com"

    create_ca(root_ca_path, key_path, common_name, email_address)
    ca_cert, ca_key = load_ca(root_ca_path, key_path)
    validity = verify_ca(ca_cert)
    print("CA Certificate valid for {} days".format(validity))

    client_cert_dir = "client"

    if not os.path.exists(client_cert_dir):
        os.makedirs(client_cert_dir)

    client_cn = "client/client"

    subject = ca_cert.get_subject()
    print("subject: ", subject)
    create_cert(ca_cert, subject, ca_key, client_cn)


main()
