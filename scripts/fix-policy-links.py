#!/usr/bin/env python3
import os
import glob

TARGET_DIR = "/Users/fernandavitorino/metrixmidia-site"

def main():
    print("Replacing policy links safely...")
    pattern = os.path.join(TARGET_DIR, "**/*.html")
    for f in glob.glob(pattern, recursive=True):
        if os.path.basename(f) == "politica-de-privacidade.html":
            continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        new_content = content.replace('href="/politica-de-privacidade"', 'href="/politica-de-privacidade.html"')
        
        if new_content != content:
            print(f"  Updated links in: {os.path.relpath(f, TARGET_DIR)}")
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)

if __name__ == "__main__":
    main()
