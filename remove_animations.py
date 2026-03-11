import re

filepath = r"c:\Users\touvo\Desktop\Site\Bvati\index3.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Nettoyer les classes 'reveal' de la section '#services'
html = html.replace('<div class="section-label reveal" style="color:var(--gold)">Prestations & Services</div>', '<div class="section-label" style="color:var(--gold)">Prestations & Services</div>')
html = html.replace('<h2 class="section-title reveal" style="color:var(--gold)">Notre<br>Expertise</h2>', '<h2 class="section-title" style="color:var(--gold)">Notre<br>Expertise</h2>')

html = html.replace('<div class="service-card reveal">', '<div class="service-card">')
html = html.replace('<div class="service-card reveal reveal-delay-1">', '<div class="service-card">')
html = html.replace('<div class="service-card reveal reveal-delay-2">', '<div class="service-card">')

# 2. Nettoyer les classes 'reveal' de la section '#values'
html = html.replace('<div class="section-label reveal">Notre ADN</div>', '<div class="section-label">Notre ADN</div>')
html = html.replace('<h2 class="section-title reveal">Mission, Vision<br><span style="color:var(--gold)">& Valeurs</span></h2>', '<h2 class="section-title">Mission, Vision<br><span style="color:var(--gold)">& Valeurs</span></h2>')

html = html.replace('<div class="value-card reveal">', '<div class="value-card">')
html = html.replace('<div class="value-card reveal reveal-delay-1">', '<div class="value-card">')
html = html.replace('<div class="value-card reveal reveal-delay-2">', '<div class="value-card">')


# 3. Supprimer le code GSAP qui anime progressivement l'apparition des 'service-card'
# On remplace ce bloc par rien, MAIS on garde l'effet magnet (Tilt 3D) si l'utilisateur ne parlait QUE de l'apparition.
# "les animations qui font que les élements s'affichent progessivement"
# L'animation d'apparition est : gsap.fromTo(card, { opacity: ...
appear_animation = """                // Appear animation
                gsap.fromTo(card,
                    { opacity: 0, y: 100, rotationY: 15 },
                    {
                        opacity: 1, y: 0, rotationY: 0,
                        duration: 1,
                        ease: "power3.out",
                        delay: i * 0.2,
                        scrollTrigger: {
                            trigger: ".services-grid",
                            start: "top 75%",
                            toggleActions: "play none none reverse"
                        }
                    }
                );"""

html = html.replace(appear_animation, "")

# Remove the line `card.classList.remove('reveal');` next to it as well, or we can just leave it, it won't hurt.
html = html.replace("                // Remove generic reveal to avoid conflict\n                card.classList.remove('reveal');", "")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
