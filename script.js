// Enregistrement du plugin GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

document.addEventListener("DOMContentLoaded", () => {
    initThreeJS();
    initGSAP();
    initVanillaEffects();
});

// -------------- THREE.JS BACKGROUND (Particules Cinématiques) --------------
function initThreeJS() {
    const container = document.getElementById('canvas-container');

    const scene = new THREE.Scene();

    // Ajout d'un léger brouillard pour la profondeur
    scene.fog = new THREE.FogExp2(0x05080b, 0.001);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 40;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Création des particules (poussières dans un faisceau de lumière)
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 800; // Nombre de particules

    // Tableau pour stocker les positions (x, y, z)
    const posArray = new Float32Array(particlesCount * 3);
    const speedArray = new Float32Array(particlesCount); // Vitesse individuelle

    for (let i = 0; i < particlesCount * 3; i += 3) {
        // Dispersion aléatoire
        posArray[i] = (Math.random() - 0.5) * 150;      // x
        posArray[i + 1] = (Math.random() - 0.5) * 150;    // y
        posArray[i + 2] = (Math.random() - 0.5) * 100;    // z

        speedArray[i / 3] = Math.random() * 0.02 + 0.005;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    // Texture de particule (optionnelle, ici un rond doux généré par canvas)
    const particleTexture = createCircleTexture();

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.8,
        color: 0xd5a337, // Or/Yellow de BVATI
        map: particleTexture,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Lumière diffuse pour une ambiance (bien que non nécessaire pour les PointsMaterial)
    const ambientLight = new THREE.AmbientLight(0x577d9e, 0.5); // Bleu BVATI
    scene.add(ambientLight);

    // Mouvement de la caméra basé sur la souris (Parallax léger)
    let mouseX = 0;
    let mouseY = 0;
    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX) * 0.05;
        mouseY = (event.clientY - windowHalfY) * 0.05;
    });

    // Animation Loop
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        // Rotation de la scène globale
        particlesMesh.rotation.y = elapsedTime * 0.05;
        particlesMesh.rotation.x = elapsedTime * 0.02;

        // Doux mouvement de caméra
        camera.position.x += (mouseX - camera.position.x) * 0.05;
        camera.position.y += (-mouseY - camera.position.y) * 0.05;
        camera.lookAt(scene.position);

        // Mouvement ascendant des particules (Effet poussière / braises)
        const positions = particlesMesh.geometry.attributes.position.array;
        for (let i = 1; i < particlesCount * 3; i += 3) {
            positions[i] += speedArray[(i - 1) / 3];
            // Si la particule monte trop haut, la remettre en bas
            if (positions[i] > 75) {
                positions[i] = -75;
            }
        }
        particlesMesh.geometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
    }

    animate();

    // Redimensionnement de la fenêtre
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// Fonction utilitaire pour générer une texture ronde pour les particules de poussière
function createCircleTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 32;
    canvas.height = 32;
    const context = canvas.getContext('2d');

    const gradient = context.createRadialGradient(16, 16, 0, 16, 16, 16);
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.2, 'rgba(213,163,55,0.8)');
    gradient.addColorStop(0.5, 'rgba(213,163,55,0.2)');
    gradient.addColorStop(1, 'rgba(0,0,0,0)');

    context.fillStyle = gradient;
    context.fillRect(0, 0, 32, 32);

    const texture = new THREE.Texture(canvas);
    texture.needsUpdate = true;
    return texture;
}


// -------------- GSAP ANIMATIONS --------------
function initGSAP() {
    // 1. Animation d'entrée du Hero
    const tlHero = gsap.timeline();

    tlHero.fromTo(".nav-logo", { y: -50, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: "power3.out" })
        .fromTo(".contact-info-nav", { y: -50, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: "power3.out" }, "-=0.8")
        .fromTo(".main-logo", { scale: 0.8, opacity: 0, filter: "blur(10px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 1.5, ease: "power4.out" }, "-=0.5")
        .fromTo(".hero-title", { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: "power3.out" }, "-=1")
        .fromTo(".scroll-indicator", { opacity: 0 }, { opacity: 1, duration: 1 }, "-=0.5");

    // 2. Animations au défilement (ScrollTrigger)

    // Cartes "About" - Stagger Effect
    gsap.from(".about-card", {
        scrollTrigger: {
            trigger: "#about",
            start: "top 80%",
        },
        y: 80,
        opacity: 0,
        duration: 1,
        stagger: 0.2,
        ease: "power3.out"
    });

    // Mots Services (Cinéma, Publicité, Vidéo)
    gsap.from(".service-word", {
        scrollTrigger: {
            trigger: "#services",
            start: "top 75%",
        },
        x: (index) => index % 2 === 0 ? -100 : 100, // Alterne Gauche / Droite
        opacity: 0,
        duration: 1.2,
        stagger: 0.3,
        ease: "power2.out"
    });

    // Image Services
    gsap.fromTo(".services-image-container",
        { scale: 0.9, opacity: 0 },
        {
            scrollTrigger: {
                trigger: ".services-image-container",
                start: "top 85%",
            },
            scale: 1,
            opacity: 1,
            duration: 1.5,
            ease: "power3.out"
        }
    );

    // Titres de section
    gsap.utils.toArray('.section-heading').forEach(heading => {
        gsap.from(heading, {
            scrollTrigger: {
                trigger: heading,
                start: "top 85%",
            },
            y: 50,
            opacity: 0,
            duration: 1,
            ease: "power3.out"
        });
    });

    // L'image des productions
    gsap.fromTo(".productions-image",
        { y: 100, opacity: 0, rotationX: 15 },
        {
            scrollTrigger: {
                trigger: "#productions",
                start: "top 70%",
            },
            y: 0,
            opacity: 1,
            rotationX: 0,
            duration: 1.5,
            ease: "back.out(1.2)"
        }
    );
}

// -------------- VANILLA JS EFFECTS --------------
function initVanillaEffects() {
    // Navbar change background on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(5, 8, 11, 0.9)';
            navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.5)';
        } else {
            navbar.style.background = 'rgba(5, 8, 11, 0.5)';
            navbar.style.boxShadow = 'none';
        }
    });

    // 3D Tilt Effect on Productions Image
    const tiltCard = document.querySelector('.tilt-effect');
    if (tiltCard) {
        tiltCard.addEventListener('mousemove', (e) => {
            const rect = tiltCard.getBoundingClientRect();
            const x = e.clientX - rect.left; // Position in element X
            const y = e.clientY - rect.top;  // Position in element Y

            // Normalize to -1 to 1 setup
            const xForce = ((x / rect.width) - 0.5) * 2;
            const yForce = ((y / rect.height) - 0.5) * 2;

            // Maximum rotation angle
            const maxTilt = 10;

            const rotateX = -yForce * maxTilt;
            const rotateY = xForce * maxTilt;

            // Apply transform dynamically
            tiltCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        // Reset to normal on mouse leave
        tiltCard.addEventListener('mouseleave', () => {
            tiltCard.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            tiltCard.style.transition = 'transform 0.5s ease';
        });

        // Remove transition during movement for snappy response
        tiltCard.addEventListener('mouseenter', () => {
            tiltCard.style.transition = 'none';
        });
    }
}
