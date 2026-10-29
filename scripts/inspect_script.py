with open(r"c:\Users\manpr\Documents\42 Kalidasa\website\index.html", "r", encoding="utf-8") as f:
    text = f.read()

script_idx = text.find('<script>')
print(text[script_idx:])

