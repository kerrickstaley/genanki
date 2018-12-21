import hashlib

BASE91_TABLE = [
  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
  't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4',
  '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':',
  ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']


def guid_for(*values):
  hash_str = '__'.join(str(val) for val in values)

  # get the first 8 bytes of the SHA256 of hash_str as an int
  m = hashlib.sha256()
  m.update(hash_str.encode('utf-8'))
  hash_bytes = m.digest()[:8]
  hash_int = 0
  for b in hash_bytes:
    hash_int <<= 8
    hash_int += b

  # convert to the weird base91 format that Anki uses
  rv_reversed = []
  while hash_int > 0:
    rv_reversed.append(BASE91_TABLE[hash_int % len(BASE91_TABLE)])
    hash_int //= len(BASE91_TABLE)

  return ''.join(reversed(rv_reversed))
