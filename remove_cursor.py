import re

filepath = r"c:\Users\touvo\Desktop\Site\Bvati\index3.html"

with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS
html = html.replace("""        /* Custom Cursor */
        @media (pointer: fine) {
            body { cursor: none; }
            a, button, .service-card, .prod-item, .tab { cursor: none; }
            .custom-cursor { position: fixed; top: 0; left: 0; width: 8px; height: 8px; background: var(--gold); border-radius: 50%; pointer-events: none; z-index: 9999; transform: translate(-50%, -50%); transition: width 0.2s, height 0.2s, background 0.2s; }
            .custom-cursor-follower { position: fixed; top: 0; left: 0; width: 40px; height: 40px; border: 1px solid rgba(201, 168, 76, 0.4); border-radius: 50%; pointer-events: none; z-index: 9998; transform: translate(-50%, -50%); transition: width 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), height 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), background 0.3s, border-color 0.3s; }
            .cursor-hover .custom-cursor { background: transparent; }
            .cursor-hover .custom-cursor-follower { width: 70px; height: 70px; background: rgba(201, 168, 76, 0.1); border-color: var(--gold); backdrop-filter: blur(2px); }
        }""", "")

# 2. HTML
html = html.replace("""    <!-- CURSOR & FX -->
    <div class="scanlines"></div>
    <div class="custom-cursor"></div>
    <div class="custom-cursor-follower"></div>""", """    <!-- FX -->
    <div class="scanlines"></div>""")

# 3. JS
custom_cursor_js = """            // Custom Cursor Logic
            const cursor = document.querySelector('.custom-cursor');
            const follower = document.querySelector('.custom-cursor-follower');
            let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
            let followerX = mouseX, followerY = mouseY;
            
            document.addEventListener('mousemove', (e) => {
                mouseX = e.clientX;
                mouseY = e.clientY;
                if(cursor) {
                    cursor.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
                }
            });

            // Follower animation loop
            gsap.ticker.add(() => {
                followerX += (mouseX - followerX) * 0.15;
                followerY += (mouseY - followerY) * 0.15;
                if(follower) {
                    follower.style.transform = `translate(${followerX}px, ${followerY}px) translate(-50%, -50%)`;
                }
            });

            // Hover effects for cursor
            const interactiveElements = document.querySelectorAll('a, button, .service-card, .prod-item, .tab');
            interactiveElements.forEach(el => {
                el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
                el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
            });"""

html = html.replace(custom_cursor_js, "")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)
