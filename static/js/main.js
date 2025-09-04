// Main JavaScript for CivicBlogs

document.addEventListener('DOMContentLoaded', function() {
    
    // Newsletter subscription functionality
    const newsletterForms = document.querySelectorAll('#newsletter-form, #sidebar-newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-2"></span> กำลังส่ง...';
            
            try {
                const response = await fetch('/newsletter/subscribe/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showAlert('success', 'สมัครรับข้อมูลข่าวสารเรียบร้อยแล้ว!');
                    form.reset();
                } else {
                    let errorMessage = 'เกิดข้อผิดพลาด กรุณาลองใหม่';
                    if (data.errors && data.errors.email) {
                        errorMessage = data.errors.email[0];
                    }
                    showAlert('error', errorMessage);
                }
            } catch (error) {
                showAlert('error', 'เกิดข้อผิดพลาดในการเชื่อมต่อ');
                console.error('Error:', error);
            } finally {
                // Reset button
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
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
    
    // Copy to clipboard functionality for social sharing
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            showAlert('success', 'คัดลอกลิงก์แล้ว!');
        }, function(err) {
            console.error('Could not copy text: ', err);
            showAlert('danger', 'ไม่สามารถคัดลอกได้');
        });
    }
    
    // Add copy link button if needed
    const socialShare = document.querySelector('.social-share');
    if (socialShare) {
        const copyButton = document.createElement('button');
        copyButton.className = 'inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-yellow-300 transition-colors';
        copyButton.innerHTML = '<i class="fas fa-link"></i>คัดลอกลิงก์';
        copyButton.onclick = () => copyToClipboard(window.location.href);
        socialShare.querySelector('.flex').appendChild(copyButton);
    }
    
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
    
    // Search functionality enhancement
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(function() {
                // Could implement search suggestions here
            }, 300));
        }
    }
    
    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    backToTopButton.className = 'fixed bottom-5 right-5 z-50 w-12 h-12 bg-yellow-500 hover:bg-yellow-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 hidden items-center justify-center';
    backToTopButton.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
    document.body.appendChild(backToTopButton);
    
    // Show/hide back to top button
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.remove('hidden');
            backToTopButton.classList.add('flex');
        } else {
            backToTopButton.classList.add('hidden');
            backToTopButton.classList.remove('flex');
        }
    });
    
    // Comment form validation
    const commentForm = document.querySelector('.comment-form form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            const name = this.querySelector('input[name="name"]').value.trim();
            const email = this.querySelector('input[name="email"]').value.trim();
            const content = this.querySelector('textarea[name="content"]').value.trim();
            
            if (!name || !email || !content) {
                e.preventDefault();
                showAlert('warning', 'กรุณากรอกข้อมูลให้ครบถ้วน');
                return false;
            }
            
            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showAlert('warning', 'กรุณากรอกอีเมลให้ถูกต้อง');
                return false;
            }
        });
    }
});

// Utility functions
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    let bgColor = 'bg-blue-50 border-blue-400 text-blue-700';
    let iconClass = 'fas fa-info-circle';
    
    if (type === 'success') {
        bgColor = 'bg-green-50 border-green-400 text-green-700';
        iconClass = 'fas fa-check-circle';
    } else if (type === 'error' || type === 'danger') {
        bgColor = 'bg-red-50 border-red-400 text-red-700';
        iconClass = 'fas fa-exclamation-circle';
    } else if (type === 'warning') {
        bgColor = 'bg-yellow-50 border-yellow-400 text-yellow-700';
        iconClass = 'fas fa-exclamation-triangle';
    }
    
    alertDiv.className = `fixed top-5 right-5 z-50 min-w-80 max-w-md p-4 border-l-4 rounded-lg shadow-lg ${bgColor} animate-slide-in`;
    alertDiv.innerHTML = `
        <div class="flex items-start">
            <div class="flex-shrink-0">
                <i class="${iconClass}"></i>
            </div>
            <div class="ml-3 flex-1">
                <p class="text-sm font-medium">${message}</p>
            </div>
            <div class="flex-shrink-0 ml-4">
                <button type="button" class="text-current hover:opacity-70 focus:outline-none" onclick="this.parentElement.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}

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

// Mobile menu toggle functionality
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

// Dark mode toggle (if needed in the future)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}