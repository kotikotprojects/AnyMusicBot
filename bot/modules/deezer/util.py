# https://pypi.org/project/music-helper/

import re
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from attrs import define

from .track_formats import TrackFormat


def clean_query(query):
    query = re.sub(r"/ feat[.]? /g", " ", query)
    query = re.sub(r"/ ft[.]? /g", " ", query)
    query = re.sub(r"/\(feat[.]? /g", " ", query)
    query = re.sub(r"/\(ft[.]? /g", " ", query)
    query = re.sub(r"/&/g", "", query)
    query = re.sub(r"/–/g", "-", query)
    query = re.sub(r"/–/g", "-", query)

    return query


def get_text_md5(text, encoding="UTF-8"):
    return hashlib.md5(str(text).encode(encoding)).hexdigest()


@define
class UrlDecrypter:
    md5_origin: str
    track_id: str
    media_version: str

    def get_url_for(self, track_format: TrackFormat):
        step1 = (f'{self.md5_origin}¤{track_format.code}¤'
                 f'{self.track_id}¤{self.media_version}')
        m = hashlib.md5()
        m.update(bytes([ord(x) for x in step1]))

        step2 = f'{m.hexdigest()}¤{step1}¤'
        step2 = step2.ljust(80, " ")

        cipher = Cipher(
            algorithm=algorithms.AES(
                key=bytes('jo6aey6haid2Teih', 'ascii')
            ),
            mode=modes.ECB(),
            backend=default_backend()
        )

        encryptor = cipher.encryptor()
        step3 = encryptor.update(bytes([ord(x) for x in step2])).hex()

        cdn = self.md5_origin[0]

        return f'https://e-cdns-proxy-{cdn}.dzcdn.net/mobile/1/{step3}'


@define
class ChunkDecrypter:
    cipher: Cipher

    @classmethod
    def from_track_id(cls, track_id: str):
        cipher = Cipher(
            algorithms.Blowfish(get_blowfish_key(track_id)),
            modes.CBC(bytes([i for i in range(8)])),
            default_backend()
        )

        return cls(
            cipher=cipher
        )

    def decrypt_chunk(self, chunk: bytes):
        decryptor = self.cipher.decryptor()
        return decryptor.update(chunk) + decryptor.finalize()


def get_blowfish_key(track_id: str):
    secret = 'g4el58wc0zvf9na1'

    m = hashlib.md5()
    m.update(bytes([ord(x) for x in track_id]))
    id_md5 = m.hexdigest()

    blowfish_key = bytes(
        [(ord(id_md5[i]) ^ ord(id_md5[i + 16]) ^ ord(secret[i])) for i in range(16)]
    )

    return blowfish_key
