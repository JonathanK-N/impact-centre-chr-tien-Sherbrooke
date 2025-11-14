// PWA Installation et notifications
let deferredPrompt;

// Écouter l'événement beforeinstallprompt
window.addEventListener('beforeinstallprompt', (e) => {
    // Empêcher l'affichage automatique de la bannière d'installation
    e.preventDefault();
    // Stocker l'événement pour l'utiliser plus tard
    deferredPrompt = e;
    // Afficher le bouton d'installation personnalisé
    showInstallButton();
});

// Fonction pour afficher le bouton d'installation
function showInstallButton() {
    const installButton = document.getElementById('install-button');
    if (installButton) {
        installButton.style.display = 'block';
        installButton.addEventListener('click', installApp);
    } else {
        // Créer dynamiquement le bouton d'installation
        createInstallButton();
    }
}

// Créer le bouton d'installation
function createInstallButton() {
    const button = document.createElement('button');
    button.id = 'install-button';
    button.className = 'btn btn-primary position-fixed';
    button.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50px; padding: 10px 20px;';
    button.innerHTML = '<i class="bi bi-download me-1"></i>Installer l\'app';
    button.addEventListener('click', installApp);
    document.body.appendChild(button);
}

// Fonction d'installation de l'app
function installApp() {
    const installButton = document.getElementById('install-button');
    if (installButton) {
        installButton.style.display = 'none';
    }
    
    if (deferredPrompt) {
        // Afficher la boîte de dialogue d'installation
        deferredPrompt.prompt();
        // Attendre la réponse de l'utilisateur
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('L\'utilisateur a accepté l\'installation');
            } else {
                console.log('L\'utilisateur a refusé l\'installation');
            }
            deferredPrompt = null;
        });
    }
}

// Écouter l'événement appinstalled
window.addEventListener('appinstalled', (evt) => {
    console.log('PWA installée avec succès');
    // Masquer le bouton d'installation
    const installButton = document.getElementById('install-button');
    if (installButton) {
        installButton.remove();
    }
});

// Vérifier si l'app est déjà installée
function isAppInstalled() {
    return window.matchMedia('(display-mode: standalone)').matches || 
           window.navigator.standalone === true;
}

// Masquer le bouton si l'app est déjà installée
if (isAppInstalled()) {
    const installButton = document.getElementById('install-button');
    if (installButton) {
        installButton.style.display = 'none';
    }
}