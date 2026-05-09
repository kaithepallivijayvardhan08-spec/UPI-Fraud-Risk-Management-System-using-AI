// Authentication Module for SafePay

function checkAuth() {
    const user = getCurrentUser();
    if (!user) {
        showLogin();
        return false;
    }
    return true;
}

function requireAuth(callback) {
    if (checkAuth()) {
        callback();
    } else {
        showLogin();
    }
}

// Password hashing (simple - in production use proper hashing)
function hashPassword(password) {
    let hash = 0;
    for (let i = 0; i < password.length; i++) {
        hash = ((hash << 5) - hash) + password.charCodeAt(i);
        hash |= 0;
    }
    return hash.toString();
}

// Session management
function startSession(user) {
    sessionStorage.setItem('safepay_session', JSON.stringify({
        userId: user.email,
        startTime: new Date().toISOString()
    }));
}

function endSession() {
    sessionStorage.removeItem('safepay_session');
}

function isSessionValid() {
    const session = sessionStorage.getItem('safepay_session');
    if (!session) return false;
    
    const sessionData = JSON.parse(session);
    const startTime = new Date(sessionData.startTime);
    const now = new Date();
    const hoursDiff = (now - startTime) / (1000 * 60 * 60);
    
    return hoursDiff < 24; // Session valid for 24 hours
}