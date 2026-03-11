import re

filepath = r"c:\Users\touvo\Desktop\Site\Bvati\index3.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Partner cards to <a> tags
html = html.replace('<div class="partner-card">', '<a href="#" target="_blank" class="partner-card">')
html = html.replace('</div>\n                <div class="partner-card"><img', '</a>\n                <a href="#" target="_blank" class="partner-card"><img')
# There are </span></div> that need to map to </span></a> as well.
html = re.sub(r'(<span class="partner-card-text">.*?</span>)</div>', r'\1</a>', html)
# Let's just do a smarter replace using regex to change the closing tags of partner-card
html = re.sub(r'<div class="partner-card">(.*?)</div>', r'<a href="#" target="_blank" class="partner-card">\1</a>', html)

# 2. Remove CSS hover pause
html = html.replace("""            .partners-track:hover {
                animation-play-state: paused;
            }""", "")

# 3. Add JS hover pause
partner_js_old = """                // Acceleration effect on scroll
                // A bit advanced: we speed up timescale when scrolling.
                let partnerTween = gsap.getTweensOf(partnersTrack)[0];"""

partner_js_new = """                // Hover Pause
                let partnerTween = gsap.getTweensOf(partnersTrack)[0];
                partnersTrack.addEventListener('mouseenter', () => partnerTween.pause());
                partnersTrack.addEventListener('mouseleave', () => partnerTween.play());

                // Acceleration effect on scroll"""
html = html.replace(partner_js_old, partner_js_new)


# 4. Insert Preloader HTML
preloader_html = """<body>
    <!-- PRELOADER -->
    <div id="preloader" style="position: fixed; inset: 0; background: var(--darker); z-index: 10000; display: flex; align-items: center; justify-content: center; flex-direction: column;">
        <div class="clapper-preloader" style="width: 120px;">
            <div class="clapper-top-preloader" style="transform-origin: bottom left; border: 3px solid var(--white); background: repeating-linear-gradient(45deg, #fff, #fff 10px, #000 10px, #000 20px); height: 20px; margin-bottom: 2px;"></div>
            <div class="clapper-bottom-preloader" style="border: 3px solid var(--white); background: #000; height: 80px; display: flex; align-items: center; justify-content: center;">
                <span style="font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; color: var(--white); letter-spacing: 2px;">BVATI</span>
            </div>
        </div>
    </div>

    <!-- FX -->"""
html = html.replace("""<body>
    <!-- FX -->""", preloader_html)


# 5. Wrap Hero Animations in function and add preloader GSAP logic
hero_anim_old = """            // Hero Animations
            const tagline = document.querySelector('.hero-tagline');
            if (tagline) {
                tagline.style.visibility = 'visible';
                const splitTagline = new SplitType(tagline, { types: 'lines, words, chars' });

                const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });

                tl.fromTo(splitTagline.chars,
                    { y: 50, opacity: 0, rotationX: -90 },
                    { y: 0, opacity: 1, rotationX: 0, duration: 1.2, stagger: 0.03, delay: 0.5 }
                )
                    .fromTo(document.querySelector('.hero-sub'),
                        { y: 20, opacity: 0 },
                        { y: 0, opacity: 1, duration: 1 },
                        "-=0.6"
                    )
                    .fromTo(document.querySelector('.hero-cta'),
                        { y: 20, opacity: 0 },
                        { y: 0, opacity: 1, duration: 1 },
                        "-=0.8"
                    )
                    .fromTo(document.querySelector('.scroll-indicator'),
                        { opacity: 0 },
                        { opacity: 1, duration: 1 },
                        "-=0.5"
                    );
            }"""

hero_anim_new = """            // Hero Animations Function
            function startHeroAnimations() {
                const tagline = document.querySelector('.hero-tagline');
                if (tagline) {
                    tagline.style.visibility = 'visible';
                    const splitTagline = new SplitType(tagline, { types: 'lines, words, chars' });

                    const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });

                    tl.fromTo(splitTagline.chars,
                        { y: 50, opacity: 0, rotationX: -90 },
                        { y: 0, opacity: 1, rotationX: 0, duration: 1.2, stagger: 0.03 }
                    )
                        .fromTo(document.querySelector('.hero-sub'),
                            { y: 20, opacity: 0 },
                            { y: 0, opacity: 1, duration: 1 },
                            "-=0.6"
                        )
                        .fromTo(document.querySelector('.hero-cta'),
                            { y: 20, opacity: 0 },
                            { y: 0, opacity: 1, duration: 1 },
                            "-=0.8"
                        )
                        .fromTo(document.querySelector('.scroll-indicator'),
                            { opacity: 0 },
                            { opacity: 1, duration: 1 },
                            "-=0.5"
                        );
                }
            }

            // Preloader Animation
            const preloader = document.getElementById('preloader');
            const clapperTopPre = document.querySelector('.clapper-top-preloader');
            
            if (preloader && clapperTopPre) {
                const masterTl = gsap.timeline({
                    onComplete: () => {
                        gsap.to(preloader, { 
                            yPercent: -100, 
                            duration: 0.6, 
                            ease: "power3.inOut",
                            onComplete: () => {
                                preloader.style.display = 'none';
                            }
                        });
                        startHeroAnimations();
                    }
                });

                masterTl.fromTo(clapperTopPre, 
                    { rotation: -35 }, 
                    { rotation: 0, duration: 0.25, ease: "power4.in" }
                )
                .to(clapperTopPre, { rotation: -10, duration: 0.1, yoyo: true, repeat: 1 })
                .to({}, { duration: 0.1 }); // small pause
            } else {
                startHeroAnimations();
            }"""

html = html.replace(hero_anim_old, hero_anim_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
