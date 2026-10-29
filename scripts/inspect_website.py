import os
from html.parser import HTMLParser

with open(r"c:\Users\manpr\Documents\42 Kalidasa\website\index.html", "r", encoding="utf-8") as f:
    text = f.read()

main_start = text.find('<main class="narrative-container">')
script_idx = text.find('<script>')
print("=== MAIN CONTENT ===")
print(text[main_start:script_idx])
print("=== SCRIPT CONTENT (FIRST 500 CHARS) ===")
print(text[script_idx:script_idx+500])

