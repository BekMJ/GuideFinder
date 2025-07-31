// TourGuide Connect - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Dynamic price calculation for booking forms
    const priceElements = document.querySelectorAll('[data-price]');
    const peopleInputs = document.querySelectorAll('[data-people-input]');
    
    function updateTotalPrice() {
        peopleInputs.forEach(input => {
            const priceElement = input.closest('.card').querySelector('[data-price]');
            const peopleCount = parseInt(input.value) || 0;
            const pricePerPerson = parseFloat(priceElement.dataset.price) || 0;
            const totalPrice = peopleCount * pricePerPerson;
            
            const totalElement = input.closest('.card').querySelector('[data-total-price]');
            if (totalElement) {
                totalElement.textContent = `$${totalPrice.toFixed(2)}`;
            }
        });
    }

    peopleInputs.forEach(input => {
        input.addEventListener('input', updateTotalPrice);
    });

    // Search form enhancement
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="location"]');
        const searchButton = searchForm.querySelector('button[type="submit"]');
        
        // Add loading state to search button
        searchForm.addEventListener('submit', function() {
            searchButton.innerHTML = '<span class="loading"></span> Searching...';
            searchButton.disabled = true;
        });
    }

    // Tour card hover effects
    const tourCards = document.querySelectorAll('.tour-card');
    tourCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Rating system enhancement
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    const ratingStars = document.querySelectorAll('.rating-stars');
    
    ratingStars.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                input.value = rating;
                
                // Update visual stars
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.remove('far');
                        s.classList.add('fas');
                    } else {
                        s.classList.remove('fas');
                        s.classList.add('far');
                    }
                });
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.remove('far');
                        s.classList.add('fas');
                    }
                });
            });
            
            star.addEventListener('mouseleave', function() {
                const currentRating = parseInt(input.value) || 0;
                stars.forEach((s, i) => {
                    if (i < currentRating) {
                        s.classList.remove('far');
                        s.classList.add('fas');
                    } else {
                        s.classList.remove('fas');
                        s.classList.add('far');
                    }
                });
            });
        });
    });

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed';
    backToTopButton.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px; display: none;';
    document.body.appendChild(backToTopButton);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Category filter enhancement
    const categoryFilters = document.querySelectorAll('.category-filter');
    const tourItems = document.querySelectorAll('.tour-item');
    
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            
            // Update active filter
            categoryFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            // Filter tours
            tourItems.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.style.display = 'block';
                    item.classList.add('fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Booking date validation
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    
    dateInputs.forEach(input => {
        input.setAttribute('min', today);
        
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            
            if (selectedDate < today) {
                this.setCustomValidity('Please select a future date');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Character counter for text areas
    const textAreas = document.querySelectorAll('textarea[maxlength]');
    textAreas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('div');
        counter.className = 'form-text text-muted';
        counter.textContent = `0 / ${maxLength} characters`;
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            counter.textContent = `${currentLength} / ${maxLength} characters`;
            
            if (currentLength > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
        });
    });

    // Mobile menu enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        const mobileLinks = navbarCollapse.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }

    // Search suggestions (placeholder for future enhancement)
    const searchInput = document.querySelector('input[name="location"]');
    if (searchInput) {
        const popularLocations = ['Paris', 'New York', 'Tokyo', 'London', 'Rome', 'Barcelona', 'Amsterdam', 'Prague'];
        
        searchInput.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const suggestions = popularLocations.filter(location => 
                location.toLowerCase().includes(value)
            );
            
            // This could be enhanced with a dropdown suggestions list
            console.log('Search suggestions:', suggestions);
        });
    }

    // Performance optimization: Debounce search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Apply debouncing to search inputs
    const debouncedInputs = document.querySelectorAll('input[type="search"], input[name="location"]');
    debouncedInputs.forEach(input => {
        input.addEventListener('input', debounce(function() {
            // Handle search input changes
            console.log('Search input changed:', this.value);
        }, 300));
    });

    // Accessibility enhancements
    // Add keyboard navigation for rating stars
    const ratingContainers = document.querySelectorAll('.rating-stars');
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.star');
        let currentFocus = -1;
        
        container.addEventListener('keydown', function(e) {
            switch(e.key) {
                case 'ArrowRight':
                    e.preventDefault();
                    currentFocus = Math.min(currentFocus + 1, stars.length - 1);
                    stars[currentFocus].focus();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    currentFocus = Math.max(currentFocus - 1, 0);
                    stars[currentFocus].focus();
                    break;
                case 'Enter':
                case ' ':
                    e.preventDefault();
                    stars[currentFocus].click();
                    break;
            }
        });
    });

    // Console log for debugging
    console.log('TourGuide Connect JavaScript loaded successfully!');
}); 