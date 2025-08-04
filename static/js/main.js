// Main JavaScript for Professional Community Platform

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize Application
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Setup form enhancements
    setupFormEnhancements();
    
    // Setup navigation enhancements
    setupNavigationEnhancements();
    
    // Setup post interactions
    setupPostInteractions();
    
    // Setup responsive utilities
    setupResponsiveUtilities();
    
    console.log('ProCommunity application initialized successfully');
}

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form Enhancement Functions
function setupFormEnhancements() {
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
        
        // Initial resize
        autoResizeTextarea(textarea);
    });
    
    // Enhanced form validation feedback
    const forms = document.querySelectorAll('.needs-validation, form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                }
            }
            
            form.classList.add('was-validated');
        });
    });
}

// Auto-resize textarea function
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

// Navigation Enhancements
function setupNavigationEnhancements() {
    // Highlight active navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Mobile menu auto-close
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navbarCollapse.contains(event.target) || 
                                   navbarToggler.contains(event.target);
            
            if (!isClickInsideNav && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    }
}

// Post Interaction Functions
function setupPostInteractions() {
    // Smooth scroll for post actions
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(card => {
        card.addEventListener('click', function(event) {
            // Only handle clicks on the card itself, not buttons
            if (event.target === card || event.target.closest('.card-body') === card.querySelector('.card-body')) {
                // Optional: Add click interaction for post cards
            }
        });
    });
    
    // Enhanced button feedback
    const actionButtons = document.querySelectorAll('.post-actions .btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

// Responsive Utilities
function setupResponsiveUtilities() {
    // Handle window resize
    window.addEventListener('resize', function() {
        // Auto-resize textareas on window resize
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(autoResizeTextarea);
    });
    
    // Touch device optimizations
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // Enhanced touch interactions for buttons
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('touchstart', function() {
                this.classList.add('active');
            });
            
            button.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('active');
                }, 150);
            });
        });
    }
}

// Utility Functions
function showLoading(element, loadingText = 'Loading...') {
    if (element) {
        element.disabled = true;
        element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${loadingText}`;
    }
}

function hideLoading(element, originalText) {
    if (element) {
        element.disabled = false;
        element.innerHTML = originalText;
    }
}

function showToast(message, type = 'info') {
    // Create toast element
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${getToastIcon(type)} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-triangle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

// Character count utility
function setupCharacterCount(textareaId, counterId, maxLength = null) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    
    if (textarea && counter) {
        textarea.addEventListener('input', function() {
            const count = this.value.length;
            counter.textContent = count + (maxLength ? ` / ${maxLength}` : '') + ' characters';
            
            if (maxLength && count > maxLength) {
                counter.classList.add('text-danger');
                textarea.classList.add('is-invalid');
            } else {
                counter.classList.remove('text-danger');
                textarea.classList.remove('is-invalid');
            }
        });
    }
}

// Form validation utilities
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 8;
}

function validatePasswordMatch(password, confirmPassword) {
    return password === confirmPassword;
}

// Local storage utilities
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

function getFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return null;
    }
}

// Animation utilities
function fadeIn(element, duration = 300) {
    element.style.opacity = '0';
    element.style.display = 'block';
    
    let opacity = 0;
    const timer = setInterval(function() {
        opacity += 50 / duration;
        if (opacity >= 1) {
            clearInterval(timer);
            opacity = 1;
        }
        element.style.opacity = opacity;
    }, 50);
}

function fadeOut(element, duration = 300) {
    let opacity = 1;
    const timer = setInterval(function() {
        opacity -= 50 / duration;
        if (opacity <= 0) {
            clearInterval(timer);
            opacity = 0;
            element.style.display = 'none';
        }
        element.style.opacity = opacity;
    }, 50);
}

// Debounce utility for performance
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

// Export functions for use in other scripts
window.ProCommunity = {
    showLoading,
    hideLoading,
    showToast,
    setupCharacterCount,
    validateEmail,
    validatePassword,
    validatePasswordMatch,
    saveToLocalStorage,
    getFromLocalStorage,
    fadeIn,
    fadeOut,
    debounce
};
