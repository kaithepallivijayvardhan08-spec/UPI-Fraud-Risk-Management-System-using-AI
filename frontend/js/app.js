// Component loader function
async function loadComponent(componentName, containerId) {
    try {
        const response = await fetch(`components/${componentName}.html`);
        const html = await response.text();
        document.getElementById(containerId).innerHTML = html;
        
        // Execute any scripts in the component
        const scripts = document.getElementById(containerId).getElementsByTagName('script');
        for (let script of scripts) {
            eval(script.textContent);
        }
        
        return true;
    } catch (error) {
        console.error(`Error loading component ${componentName}:`, error);
        return false;
    }
}

// Update show functions to use components
function showLogin() {
    currentScreen = 'login';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('login', 'active-component');
}

function showDashboard() {
    currentScreen = 'dashboard';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('dashboard', 'active-component').then(() => {
        refreshDashboardData();
        updateNotificationBadge();
    });
}

function showSendMoney() {
    currentScreen = 'payment';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('payment', 'active-component').then(() => {
        loadQuickPayees();
    });
}

function showHistory() {
    currentScreen = 'history';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('history', 'active-component').then(() => {
        loadTransactionHistory();
    });
}

function showAlerts() {
    currentScreen = 'alerts';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('alerts', 'active-component').then(() => {
        loadAlertsData();
    });
}

function showSettings() {
    currentScreen = 'settings';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('settings', 'active-component').then(() => {
        loadSettingsData();
    });
}

function showBankSetup() {
    currentScreen = 'banksetup';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('banksetup', 'active-component');
}

function showRequestMoney() {
    currentScreen = 'requestmoney';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('requestmoney', 'active-component').then(() => {
        loadRequestData();
    });
}

function showScanQR() {
    currentScreen = 'scanqr';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('scanqr', 'active-component').then(() => {
        startQRSimulation();
    });
}

function showNotifications() {
    currentScreen = 'notifications';
    const app = document.getElementById('app');
    app.innerHTML = '<div id="active-component"></div>';
    loadComponent('notifications', 'active-component').then(() => {
        loadNotificationsData();
        markAllNotificationsRead();
    });
}

// Global goBack function
function goBack() {
    switch(currentScreen) {
        case 'payment':
        case 'history':
        case 'alerts':
        case 'settings':
        case 'requestmoney':
        case 'scanqr':
        case 'notifications':
            showDashboard();
            break;
        case 'banksetup':
            showLogin();
            break;
        default:
            showDashboard();
    }
}