class CaesarCipher:
    """Encryption & Decryption using Caesar Cipher"""

    def __init__(self, shift_by) -> None:
        """Construct Cipher using give integer shift for rotation"""

        # get ordinal A + shift and then return respective char
        self._fow: str = "".join(
            [chr((i + shift_by) % 26 + ord("A")) for i in range(26)]
        )
        self._back: str = "".join(
            [chr((i - shift_by) % 26 + ord("A")) for i in range(26)]
        )

    def _transform(self, original, code):
        msg = list(original)

        for k in range(len(msg)):
            if msg[k].isupper():
                j = ord(msg[k]) - ord("A")
                msg[k] = code[j]
        return "".join(msg)

    def encrypt(self, message):
        """return encrypted str"""

        return self._transform(message, self._fow)

    def decrypt(self, message):
        """return decrypted str"""

        return self._transform(message, self._back)


if __name__ == "__main__":
    c = CaesarCipher(3)
    print(c._fow)
    print(c._back)
    print(c.encrypt("KANDA"))
    print(c.decrypt("NDQGD"))
    # print(c.encrypt("kanda"))
