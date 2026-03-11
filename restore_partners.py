import re

filepath = r"c:\Users\touvo\Desktop\Site\Bvati\index3.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Restore HTML
html_start = '<div class="reveal" style="overflow: hidden;">'
html_end = '</section>'
match = re.search(re.escape(html_start) + r'.*?' + re.escape(html_end), html, flags=re.DOTALL)

if match:
    correct_html = """<div class="reveal" style="overflow: hidden;">
            <div class="partners-track">
                <!-- First set -->
                <div class="partner-card"><img src="DAFANI.webp" alt="Dafani"></div>
                <div class="partner-card"><img src="RTB.jpeg" alt="RTB"></div>
                <div class="partner-card"><span class="partner-card-text">UNFPA</span></div>
                <div class="partner-card"><img src="rgph.jpeg" alt="SP/RGPH"></div>
                <div class="partner-card"><img src="orange.png" alt="Orange"></div>
                <div class="partner-card"><img src="cimburkina.jpeg" alt="CimBurkina"></div>
                <div class="partner-card"><img src="giz.jpeg" alt="GIZ"></div>
                <div class="partner-card"><img src="gilda.jpeg" alt="Gilda"></div>
                <div class="partner-card"><span class="partner-card-text">INTERACTIVE</span></div>
                <!-- Duplicate set for seamless loop -->
                <div class="partner-card"><img src="DAFANI.webp" alt="Dafani"></div>
                <div class="partner-card"><img src="RTB.jpeg" alt="RTB"></div>
                <div class="partner-card"><span class="partner-card-text">UNFPA</span></div>
                <div class="partner-card"><img src="rgph.jpeg" alt="SP/RGPH"></div>
                <div class="partner-card"><img src="orange.png" alt="Orange"></div>
                <div class="partner-card"><img src="cimburkina.jpeg" alt="CimBurkina"></div>
                <div class="partner-card"><img src="giz.jpeg" alt="GIZ"></div>
                <div class="partner-card"><img src="gilda.jpeg" alt="Gilda"></div>
                <div class="partner-card"><span class="partner-card-text">INTERACTIVE</span></div>
            </div>
        </div>
    </section>"""
    html = html.replace(match.group(0), correct_html)

# 2. Restore JS
js_start = '// Hover Pause\n                let partnerTween'
js_end = '// Acceleration effect on scroll'
match2 = re.search(re.escape('// Hover Pause') + r'.*?' + re.escape('// Acceleration effect on scroll'), html, flags=re.DOTALL)
if match2:
    correct_js = """// Acceleration effect on scroll
                // A bit advanced: we speed up timescale when scrolling.
                let partnerTween = gsap.getTweensOf(partnersTrack)[0];"""
    html = html.replace(match2.group(0), correct_js)

# 3. Add back the CSS
css_target = """.partners-track {
                display: flex;
                gap: 40px;

                width: max-content;
                align-items: center;
                margin-top: 50px;
            }"""

css_replace = """.partners-track {
                display: flex;
                gap: 40px;

                width: max-content;
                align-items: center;
                margin-top: 50px;
            }

            .partners-track:hover {
                animation-play-state: paused;
            }"""
html = html.replace(css_target, css_replace)


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
