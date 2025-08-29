// Timeline animation
document.addEventListener('DOMContentLoaded', function() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    timelineItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transition = 'opacity 0.5s ease';
    });
    
    const timelineObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                
                // Animar elementos da timeline sequencialmente
                const items = document.querySelectorAll('.timeline-item');
                items.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.opacity = '1';
                    }, index * 200);
                });
            }
        });
    }, { threshold: 0.2 });
    
    const timelineContainer = document.querySelector('.timeline-container');
    if (timelineContainer) {
        timelineObserver.observe(timelineContainer);
    }
});