import re

filepath = 'c:/Users/touvo/Desktop/Site/Bvati/index3.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any base64 image source with Logo.png
new_content = re.sub(r'src="data:image/[^"]+"', 'src="Logo.png"', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Replaced data images with Logo.png")
