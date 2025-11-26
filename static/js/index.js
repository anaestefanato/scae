document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    const animateElements = document.querySelectorAll('.card, .feature-icon, h2, .lead');
    animateElements.forEach(el => {
        el.classList.add('animate-on-scroll');
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    let scrollTimeout;
    let ticking = false;
    
    window.addEventListener('scroll', function () {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                const logo = document.querySelector('.logo-rotativa');
                if (logo) {
                    const rotation = window.scrollY / 5;
                    logo.style.setProperty('--rotation', `${rotation}deg`);
                    
                    // Adiciona classe durante scroll
                    logo.classList.add('scrolling');
                    
                    // Remove classe após parar de rolar
                    clearTimeout(scrollTimeout);
                    scrollTimeout = setTimeout(() => {
                        logo.classList.remove('scrolling');
                    }, 150);
                }
                ticking = false;
            });
            ticking = true;
        }
    });
});
