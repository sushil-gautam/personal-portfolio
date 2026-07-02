document.addEventListener('DOMContentLoaded', () => {
    
    // Intersection Observer for fade-in animations on scroll
    const faders = document.querySelectorAll('.fade-in');
    
    const appearOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('appear');
                observer.unobserve(entry.target);
            }
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });

    // Make the first elements appear immediately without scrolling
    setTimeout(() => {
        const initialFaders = document.querySelectorAll('.hero .fade-in, .about .fade-in');
        initialFaders.forEach(fader => {
            const rect = fader.getBoundingClientRect();
            if(rect.top < window.innerHeight) {
                fader.classList.add('appear');
            }
        });
    }, 100);

    // Navbar background opacity on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 15, 0.9)';
            navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(10, 10, 15, 0.7)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Handle Contact Form Submission
    const contactForm = document.getElementById('contactForm');
    const successDialog = document.getElementById('successDialog');
    
    if(contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent page reload/redirect
            
            const formData = new FormData(contactForm);
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerText;
            
            submitBtn.innerText = 'Sending...';
            submitBtn.disabled = true;

            fetch(contactForm.action, {
                method: "POST",
                body: new URLSearchParams(formData),
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            })
            .then(response => {
                // Show the success dialog box
                successDialog.classList.add('show');
                contactForm.reset();
                
                // Reset button
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;
                
                // Hide dialog after 5 seconds
                setTimeout(() => {
                    successDialog.classList.remove('show');
                }, 5000);
            })
            .catch(error => {
                alert("There was an issue sending your message. Please try again.");
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;
            });
        });
    }

});
