// Mobile optimizations
document.addEventListener('DOMContentLoaded', function() {
    // Améliorer les tables sur mobile
    const tables = document.querySelectorAll('.table-responsive table');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            cells.forEach((cell, index) => {
                if (headers[index]) {
                    cell.setAttribute('data-label', headers[index].textContent.trim());
                }
            });
        });
    });
    
    // Améliorer les dropdowns sur mobile
    if (window.innerWidth <= 576) {
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            dropdown.classList.add('position-static', 'w-100', 'border-0', 'shadow-none');
        });
    }
    
    // Gérer l'orientation mobile
    function handleOrientationChange() {
        // Forcer un reflow après changement d'orientation
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 100);
    }
    
    window.addEventListener('orientationchange', handleOrientationChange);
    
    // Optimiser les cartes sur mobile
    if (window.innerWidth <= 768) {
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.add('mb-3');
        });
    }
    
    // Améliorer les boutons sur mobile
    const buttons = document.querySelectorAll('.btn:not(.btn-group .btn)');
    if (window.innerWidth <= 576) {
        buttons.forEach(btn => {
            if (!btn.closest('.btn-group') && !btn.classList.contains('btn-sm') && !btn.classList.contains('btn-xs')) {
                btn.classList.add('w-mobile-100');
            }
        });
    }
});

// Fonction pour détecter si on est sur mobile
function isMobile() {
    return window.innerWidth <= 768;
}

// Fonction pour adapter les modals sur mobile
function adaptModalsForMobile() {
    if (isMobile()) {
        const modals = document.querySelectorAll('.modal-dialog');
        modals.forEach(modal => {
            modal.classList.add('modal-fullscreen-sm-down');
        });
    }
}

// Appeler au chargement et au redimensionnement
window.addEventListener('load', adaptModalsForMobile);
window.addEventListener('resize', adaptModalsForMobile);