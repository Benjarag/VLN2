// Auto-dismiss alerts after 5 seconds
function setupMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Auto-hide after 5 seconds
        const fadeOutTimer = setTimeout(() => {
            fadeOut(alert);
        }, 5000);  // 5000ms = 5 seconds

        // Manual dismissal
        const closeBtn = alert.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(fadeOutTimer);  // Cancel auto-dismissal
                fadeOut(alert);
            });
        }
    });

    function fadeOut(element) {
        element.style.transition = 'opacity 0.5s ease-out';
        element.style.opacity = '0';
        setTimeout(() => {
            element.remove();
        }, 500);
    }
}

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', setupMessages);