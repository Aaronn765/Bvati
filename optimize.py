import re

filepath = r"c:\Users\touvo\Desktop\Site\Bvati\index3.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Make all images except the navbar logo lazy loaded
html = re.sub(r'<img src="(.*?)"(.*?)>', r'<img src="\1" loading="lazy" \2>', html)

# Fix the navbar logo specifically (it shouldn't be lazy loaded for LCP)
html = html.replace('<img src="Logo.png" loading="lazy"  alt="BVATI Productions" class="nav-logo">', '<img src="Logo.png" alt="BVATI Productions" class="nav-logo">')
# Actually, let's just reverse the lazy loading on the specific nav logo and footer logo since they are light
html = html.replace('<img src="Logo.png" loading="lazy" alt="BVATI Productions" class="nav-logo">', '<img src="Logo.png" alt="BVATI Productions" class="nav-logo">')
html = html.replace('<img src="Logo.png" loading="lazy" alt="BVATI" class="footer-logo">', '<img src="Logo.png" alt="BVATI" class="footer-logo">')

# Also defer three script
html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" defer></script>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

