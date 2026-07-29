#!/usr/bin/env python3
import os
import sys
import re
import json
import subprocess

TARGET_DIR = "/Users/fernandavitorino/metrixmidia-site"

LEAKED_FILES = [
    "blog/zero-click-marketing-automacao-dms-2026/index.html",
    "blog/google-sge-video-seo-reels-tiktok-buscas/index.html",
    "blog/de-roas-para-poas-mudanca-trafego-pago-2026/index.html",
    "blog/fadiga-criativa-acelerada-meta-ads-advantage-plus/index.html",
    "blog/punicao-google-conteudo-ia-e-e-a-t-2026/index.html",
    "blog/funil-whatsapp-blindado-mudancas-algoritmo-2026/index.html",
    "blog/como-otimizar-marca-recomendacao-ia-geo-2026/index.html"
]

def unescape_and_clean_faq(file_path):
    print(f"Cleaning template leak & FAQ on: {file_path}")
    full_path = os.path.join(TARGET_DIR, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Unescape {{ and }} to { and }
    content = content.replace("{{", "{").replace("}}", "}")

    # 2. Remove the 3rd script block containing FAQPage
    pattern = r'<script\s+type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"FAQPage".*?</script>'
    content, count = re.subn(pattern, '', content, flags=re.DOTALL)
    print(f"  Removed {count} FAQPage JSON-LD blocks")

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def reidentify_metadata(file_path):
    print(f"Re-identifying metadata on: {file_path}")
    full_path = os.path.join(TARGET_DIR, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slug = os.path.basename(os.path.dirname(file_path))
    correct_canonical = f"https://metrixmidia.com.br/blog/{slug}/"

    title_match = re.search(r'<title>(.*?)</title>', content)
    if not title_match:
        print(f"  Warning: Title not found in {file_path}")
        return
    title_val = title_match.group(1).replace(" — Metrix Mídia", "").strip()

    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content)
    if not desc_match:
        print(f"  Warning: Description not found in {file_path}")
        return
    desc_val = desc_match.group(1).strip()

    try:
        git_date = subprocess.check_output(
            ["git", "log", "--diff-filter=A", "--format=%cs", "--", file_path],
            cwd=TARGET_DIR
        ).decode('utf-8').strip().split('\n')[-1]
        if not git_date:
            git_date = "2026-07-29"
    except Exception:
        git_date = "2026-07-29"

    # Fix HTML tags
    content = re.sub(
        r'<link\s+rel="canonical"\s+href=".*?"',
        f'<link rel="canonical" href="{correct_canonical}"',
        content
    )
    content = re.sub(
        r'<meta\s+property="og:title"\s+content=".*?"',
        f'<meta property="og:title" content="{title_val}"',
        content
    )
    content = re.sub(
        r'<meta\s+property="og:description"\s+content=".*?"',
        f'<meta property="og:description" content="{desc_val}"',
        content
    )
    content = re.sub(
        r'<meta\s+property="og:url"\s+content=".*?"',
        f'<meta property="og:url" content="{correct_canonical}"',
        content
    )

    # Now let's parse and rewrite each JSON-LD block structured
    def replace_json_ld(match):
        block_content = match.group(1).strip()
        try:
            data = json.loads(block_content)
            if data.get("@type") == "Article":
                data["headline"] = title_val
                data["description"] = desc_val
                data["mainEntityOfPage"] = correct_canonical
                data["datePublished"] = git_date
                data["dateModified"] = git_date
            elif data.get("@type") == "BreadcrumbList":
                for item in data.get("itemListElement", []):
                    if item.get("position") == 3:
                        item["name"] = title_val
                        item["item"] = correct_canonical
            
            # Format back to string with indent=2
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            lines = [("  " * 3 + line) for line in formatted.split('\n')]
            return '<script type="application/ld+json">\n' + '\n'.join(lines) + '\n  </script>'
        except Exception as e:
            print(f"  Error parsing/manipulating JSON-LD in {file_path}: {e}")
            return match.group(0)

    content = re.sub(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        replace_json_ld,
        content,
        flags=re.DOTALL
    )

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_canonical(file_path):
    full_path = os.path.join(TARGET_DIR, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if file_path == "index.html":
        canonical_url = "https://metrixmidia.com.br/"
    elif file_path.endswith("/index.html"):
        canonical_url = "https://metrixmidia.com.br/" + os.path.dirname(file_path) + "/"
    else:
        canonical_url = "https://metrixmidia.com.br/" + file_path.replace(".html", "") + "/"

    if '<link rel="canonical"' in content:
        return

    # Try to insert after <meta name="description"> or after <title>
    desc_match = re.search(r'(<meta\s+name="description"\s+content=".*?">)', content)
    if desc_match:
        target = desc_match.group(1)
        line_match = re.search(rf'^(\s*){re.escape(target)}', content, re.MULTILINE)
        indent = line_match.group(1) if line_match else "  "
        new_tag = f'\n{indent}<link rel="canonical" href="{canonical_url}">'
        content = content.replace(target, target + new_tag, 1)
    else:
        # Fallback to <title> or <head>
        title_match = re.search(r'(</title>)', content)
        if title_match:
            target = title_match.group(1)
            line_match = re.search(rf'^(\s*).*?{re.escape(target)}', content, re.MULTILINE)
            indent = line_match.group(1) if line_match else "  "
            new_tag = f'\n{indent}<link rel="canonical" href="{canonical_url}">'
            content = content.replace(target, target + new_tag, 1)
        else:
            head_match = re.search(r'(<head>)', content)
            if head_match:
                target = head_match.group(1)
                content = content.replace(target, target + f'\n  <link rel="canonical" href="{canonical_url}">', 1)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_home_meta():
    print("Fixing Home page metadata...")
    full_path = os.path.join(TARGET_DIR, "index.html")
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'name="description"' not in content:
        desc_tag = '  <meta name="description" content="Agência de tráfego pago e conteúdo para pequenas e médias empresas. Nós cuidamos das campanhas e da narrativa da sua marca, com número aberto no relatório.">'
        title_match = re.search(r'(</title>)', content)
        if title_match:
            target = title_match.group(1)
            content = content.replace(target, target + "\n" + desc_tag, 1)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def audit_repo():
    print("--- Running SEO Audit ---")
    errors = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        if any(d in root for d in [".git", ".vercel", "node_modules", "scripts", "interno"]):
            continue
        for file in files:
            if not file.endswith(".html"):
                continue
            rel_path = os.path.relpath(os.path.join(root, file), TARGET_DIR)
            
            is_noindex_page = (rel_path == "pesquisa-satisfacao/index.html")
            is_404_page = (rel_path == "404.html")

            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()

            if "{{" in content:
                print(f"❌ Error: {rel_path} contains leaked template syntax '{{{{'")
                errors += 1

            if not is_404_page and not is_noindex_page:
                canonical_match = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', content)
                if not canonical_match:
                    print(f"❌ Error: {rel_path} is missing a canonical link tag")
                    errors += 1
                else:
                    canonical_url = canonical_match.group(1)
                    expected_canonical = "https://metrixmidia.com.br/"
                    if rel_path != "index.html":
                        if rel_path.endswith("/index.html"):
                            expected_canonical += os.path.dirname(rel_path) + "/"
                        else:
                            expected_canonical += rel_path.replace(".html", "") + "/"
                    
                    if canonical_url != expected_canonical:
                        print(f"❌ Error: {rel_path} canonical URL '{canonical_url}' does not match expected '{expected_canonical}'")
                        errors += 1

            if not is_404_page:
                desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content)
                if not desc_match:
                    print(f"❌ Error: {rel_path} is missing a meta description tag")
                    errors += 1
                elif not desc_match.group(1).strip():
                    print(f"❌ Error: {rel_path} has an empty meta description tag")
                    errors += 1

            json_ld_blocks = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', content, flags=re.DOTALL)
            for block in json_ld_blocks:
                try:
                    json.loads(block.strip())
                except Exception as e:
                    print(f"❌ Error: {rel_path} JSON-LD fails JSON parsing: {e}")
                    errors += 1

            if not is_404_page and not is_noindex_page:
                og_url_match = re.search(r'<meta\s+property="og:url"\s+content="(.*?)"', content)
                canonical_match = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', content)
                if og_url_match and canonical_match:
                    if og_url_match.group(1) != canonical_match.group(1):
                        print(f"❌ Error: {rel_path} og:url '{og_url_match.group(1)}' does not match canonical '{canonical_match.group(1)}'")
                        errors += 1

            noindex_match = 'name="robots" content="noindex"' in content or 'name="robots" content="noindex, nofollow"' in content
            if is_noindex_page or is_404_page:
                if not noindex_match:
                    print(f"❌ Error: {rel_path} should have noindex Robots tag")
                    errors += 1
            else:
                if noindex_match:
                    print(f"❌ Error: {rel_path} has incorrect noindex Robots tag")
                    errors += 1

    if errors == 0:
        print("✅ Audit passed! All files conform to SEO rules.")
        return True
    else:
        print(f"❌ Audit failed with {errors} errors.")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--audit":
        success = audit_repo()
        sys.exit(0 if success else 1)

    # 1. Clean leaked files
    for f in LEAKED_FILES:
        unescape_and_clean_faq(f)
        reidentify_metadata(f)

    # 2. Add description to index.html if missing
    fix_home_meta()

    # 3. Add canonical dynamically to all HTML files (excluding noindex and 404)
    for root, dirs, files in os.walk(TARGET_DIR):
        if any(d in root for d in [".git", ".vercel", "node_modules", "scripts", "interno"]):
            continue
        for file in files:
            if not file.endswith(".html"):
                continue
            rel_path = os.path.relpath(os.path.join(root, file), TARGET_DIR)
            if rel_path == "pesquisa-satisfacao/index.html" or rel_path == "404.html":
                continue
            add_canonical(rel_path)

    print("Remediation complete. Running final audit...")
    success = audit_repo()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
