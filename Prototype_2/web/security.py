def hash_string(s):
    mod = 1000000009
    result=0
    for c in s:
        result = (result * 239 + ord(c)) % mod
    return result % mod