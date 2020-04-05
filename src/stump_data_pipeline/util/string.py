def camel_to_snake(s):
    return s[0] + ''.join([
        '_' + s[i].lower() if s[i-1].islower() and s[i].isupper() else s[i]
        for i in range(1, len(s))
    ])