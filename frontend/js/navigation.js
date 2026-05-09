// Navigation Module for SafePay

const routes = {
    'login': showLogin,
    'signup': showSignup,
    'banksetup': showBankSetup,
    'dashboard': showDashboard,
    'payment': showSendMoney,
    'history': showHistory,
    'alerts': showAlerts,
    'notifications': showNotifications,
    'settings': showSettings,
    'scanqr': showScanQR,
    'requestmoney': showRequestMoney
};

function navigateTo(screen, params = {}) {
    if (routes[screen]) {
        routes[screen](params);
        updateNavigationActive(screen);
    } else {
        console.error('Screen not found:', screen);
    }
}

function updateNavigationActive(screen) {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
    });
    
    const activeMap = {
        'dashboard': 0,
        'history': 1,
        'alerts': 2,
        'notifications': 3,
        'settings': 4
    };
    
    const index = activeMap[screen];
    if (index !== undefined && navItems[index]) {
        navItems[index].classList.add('active');
    }
}

// Handle back button
window.addEventListener('popstate', (event) => {
    const state = event.state;
    if (state && state.screen) {
        navigateTo(state.screen);
    }
});

function pushState(screen) {
    history.pushState({ screen }, '', `#${screen}`);
}