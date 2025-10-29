/**
 * Style & Grace - Fashion & Lifestyle Blog
 * Main JavaScript for interactive elements and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme if not already set
    if (!localStorage.getItem('theme')) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const initialTheme = prefersDark ? 'dark' : 'light';
        setTheme(initialTheme);
    } else {
        setTheme(localStorage.getItem('theme'));
    }
    
    // Set up theme toggle button if it exists
    const themeToggleBtn = document.getElementById('themeToggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
        
        // Set initial icon
        updateThemeIcon(document.documentElement.getAttribute('data-bs-theme'));
    }
    // Initialize AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        offset: 100
    });

    // Back to Top Button
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            // Show/hide back to top button
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        // Back to top button click handler
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Navbar scroll effect with transparency
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        // Add scrolled class on page load if scrolled
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        }
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
        });
    });

    // Active navigation link highlighting
    const sections = document.querySelectorAll('section[id]');
    
    function highlightNavigation() {
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-link[href*="${sectionId}"]`);
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
                if (navLink) navLink.classList.add('active');
            }
        });
    }
    
    // Run once on page load
    highlightNavigation();
    window.addEventListener('scroll', highlightNavigation);
    
    // Initialize highlight on page load
    highlightNavigation();

    // Newsletter subscription form
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            
            // Simple email validation
            if (!emailInput.value || !emailInput.value.includes('@')) {
                emailInput.classList.add('is-invalid');
                return;
            }
            
            emailInput.classList.remove('is-invalid');
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Subscribing...';
            
            // Simulate API call
            setTimeout(() => {
                // Reset form
                this.reset();
                
                // Show success message
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-success mt-3';
                alertDiv.role = 'alert';
                alertDiv.innerHTML = 'Thank you for subscribing to our newsletter! Check your email for a welcome gift.';
                
                // Insert after form
                this.parentNode.insertBefore(alertDiv, this.nextSibling);
                
                // Remove success message after 5 seconds
                setTimeout(() => {
                    alertDiv.remove();
                }, 5000);
                
                // Reset button
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            }, 1500);
        });
    }
    
    // Blog post interactions
    const likeButtons = document.querySelectorAll('.btn-like');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const icon = this.querySelector('i');
            const count = this.querySelector('.like-count');
            const postId = this.dataset.postId;
            
            // Toggle like state
            const isLiked = this.classList.toggle('active');
            
            // Update icon and count
            if (isLiked) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill', 'text-danger');
                count.textContent = parseInt(count.textContent) + 1;
            } else {
                icon.classList.remove('bi-heart-fill', 'text-danger');
                icon.classList.add('bi-heart');
                count.textContent = Math.max(0, parseInt(count.textContent) - 1);
            }
            
            // In a real app, you would send this to your backend
            // fetch(`/api/posts/${postId}/like`, { method: 'POST' });
        });
    });
    
    // Initialize image lightbox for blog post images (only if not already initialized in post.html)
    if (!document.querySelector('.lightbox-initialized')) {
        const blogImages = document.querySelectorAll('.blog-content img:not([data-lightbox-initialized])');
        blogImages.forEach(img => {
            img.style.cursor = 'zoom-in';
            img.setAttribute('data-lightbox-initialized', 'true');
            img.addEventListener('click', function() {
                const lightbox = document.createElement('div');
                lightbox.className = 'lightbox';
                lightbox.innerHTML = `
                    <div class="lightbox-content">
                        <img src="${this.src}" alt="${this.alt}" class="img-fluid">
                        <button class="btn-close btn-close-white position-absolute top-0 end-0 m-3" aria-label="Close"></button>
                    </div>
                `;
            
            document.body.appendChild(lightbox);
            document.body.style.overflow = 'hidden';
            
            // Close on button click
            lightbox.querySelector('.btn-close').addEventListener('click', () => {
                lightbox.remove();
                document.body.style.overflow = '';
            });
            
            // Close on outside click
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) {
                    lightbox.remove();
                    document.body.style.overflow = '';
                }
            });
            
            // Close on Escape key
            document.addEventListener('keydown', function closeOnEscape(e) {
                if (e.key === 'Escape') {
                    lightbox.remove();
                    document.body.style.overflow = '';
                    document.removeEventListener('keydown', closeOnEscape);
                }
            });
        });
    });

    // Theme switcher
    const themeToggle = document.getElementById('themeToggle');
    const lightIcon = document.getElementById('themeLightIcon');
    const darkIcon = document.getElementById('themeDarkIcon');
    
    // Function to update theme icon based on current theme
    function updateThemeIcon(theme) {
        const lightIcon = document.getElementById('themeLightIcon');
        const darkIcon = document.getElementById('themeDarkIcon');
        
        if (!lightIcon || !darkIcon) return;
        
        if (theme === 'dark') {
            lightIcon.classList.remove('d-none');
            darkIcon.classList.add('d-none');
        } else {
            lightIcon.classList.add('d-none');
            darkIcon.classList.remove('d-none');
        }
    }
    
    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    updateThemeIcon(savedTheme);
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    
    // Toggle theme on button click
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            // Set theme function
            function setTheme(theme) {
                document.documentElement.setAttribute('data-bs-theme', theme);
                localStorage.setItem('theme', theme);
                updateThemeIcon(theme);
            }
            setTheme(newTheme);
        });
    }

    // Save for Later functionality
    const saveButtons = document.querySelectorAll('.save-article');
    saveButtons.forEach(button => {
        const articleId = button.dataset.articleId;
        const savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
        
        // Update button state if article is already saved
        if (savedArticles.includes(articleId)) {
            button.classList.add('active');
            const icon = button.querySelector('i');
            if (icon) {
                icon.classList.remove('bi-bookmark');
                icon.classList.add('bi-bookmark-check-fill');
            }
        }
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const icon = this.querySelector('i');
            const savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
            const articleId = this.dataset.articleId;
            
            if (this.classList.contains('active')) {
                // Remove from saved
                const index = savedArticles.indexOf(articleId);
                if (index > -1) {
                    savedArticles.splice(index, 1);
                }
                this.classList.remove('active');
                if (icon) {
                    icon.classList.remove('bi-bookmark-check-fill');
                    icon.classList.add('bi-bookmark');
                }
                showToast('Article removed from saved items');
            } else {
                // Add to saved
                savedArticles.push(articleId);
                this.classList.add('active');
                if (icon) {
                    icon.classList.remove('bi-bookmark');
                    icon.classList.add('bi-bookmark-check-fill');
                }
                showToast('Article saved for later');
            }
            
            localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
        });
    });
    
    // Print Article functionality
    const printButton = document.getElementById('printArticle');
    if (printButton) {
        printButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    }
    
    // Pin It button for images
    document.querySelectorAll('.pin-it').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const imgSrc = this.dataset.imgSrc;
            const imgAlt = this.dataset.imgAlt || 'Pinned image';
            const pinUrl = `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(window.location.href)}&media=${encodeURIComponent(imgSrc)}&description=${encodeURIComponent(imgAlt)}`;
            
            // Open in a popup
            const width = 750;
            const height = 400;
            const left = (window.screen.width - width) / 2;
            const top = (window.screen.height - height) / 2;
            
            window.open(pinUrl, 'pinterest', `width=${width},height=${height},top=${top},left=${left},toolbar=no,location=no,status=no,menubar=no`);
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover focus',
            placement: 'top',
            container: 'body'
        });
    });
    
    // Add smooth hover effect to blog cards
    const blogCards = document.querySelectorAll('.blog-card, .card');
    blogCards.forEach(card => {
        card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 10px 20px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
        });
    });
    
    // Initialize social share buttons
    const shareButtons = document.querySelectorAll('.btn-share');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;
            const title = this.dataset.title || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(console.error);
            } else {
                // Fallback for browsers that don't support Web Share API
                window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`, '_blank');
            }
        });
    });
    
    // Initialize image hover effect for blog posts
    const postImages = document.querySelectorAll('.post-image-hover');
    postImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.03)';
            this.style.transition = 'transform 0.3s ease';
        });
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Page loader
    const pageLoader = document.querySelector('.page-loader');
    if (pageLoader) {
        // Hide loader when page is fully loaded
        window.addEventListener('load', function() {
            setTimeout(() => {
                pageLoader.classList.add('fade-out');
                setTimeout(() => {
                    pageLoader.style.display = 'none';
                }, 500);
            }, 500);
        });
    }

    // Form validation
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

    // Initialize counter animation
    function initCounterAnimation() {
        const counters = document.querySelectorAll('.counter');
        
        function animateCounter(counter) {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText.replace('+', '');
            const increment = target / 200; // Fixed increment value
            
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(() => animateCounter(counter), 1);
            }
        }
        
        function checkIfInView() {
            counters.forEach(counter => {
                const counterPosition = counter.getBoundingClientRect().top;
                const screenPosition = window.innerHeight / 1.3;
                
                if (counterPosition < screenPosition) {
                    animateCounter(counter);
                }
            });
        }
        
        // Only initialize if counters exist on the page
        if (counters.length > 0) {
            window.addEventListener('scroll', checkIfInView);
            checkIfInView(); // Run once on page load
        }
    }
    
    // Initialize counter animation
    initCounterAnimation();
});
