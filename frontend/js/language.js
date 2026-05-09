// Multi-language Support for SafePay

const translations = {
    en: {
        app_name: 'SafePay',
        login: 'Login',
        signup: 'Sign Up',
        email: 'Email',
        password: 'Password',
        send_money: 'Send Money',
        scan_qr: 'Scan QR',
        request_money: 'Request Money',
        settings: 'Settings',
        history: 'History',
        alerts: 'Alerts',
        notifications: 'Notifications',
        balance: 'Balance',
        risk_score: 'Risk Score',
        low_risk: 'Low Risk',
        medium_risk: 'Medium Risk',
        high_risk: 'High Risk',
        pay_now: 'Pay Now',
        cancel: 'Cancel',
        confirm: 'Confirm',
        success: 'Success',
        failed: 'Failed',
        processing: 'Processing...'
    },
    hi: {
        app_name: 'सेफपे',
        login: 'लॉगिन',
        signup: 'साइन अप',
        email: 'ईमेल',
        password: 'पासवर्ड',
        send_money: 'पैसे भेजें',
        scan_qr: 'क्यूआर स्कैन करें',
        request_money: 'पैसे मांगें',
        settings: 'सेटिंग्स',
        history: 'इतिहास',
        alerts: 'अलर्ट',
        notifications: 'सूचनाएं',
        balance: 'बैलेंस',
        risk_score: 'जोखिम स्कोर',
        low_risk: 'कम जोखिम',
        medium_risk: 'मध्यम जोखिम',
        high_risk: 'उच्च जोखिम',
        pay_now: 'अभी भुगतान करें',
        cancel: 'रद्द करें',
        confirm: 'पुष्टि करें',
        success: 'सफल',
        failed: 'असफल',
        processing: 'प्रोसेसिंग...'
    }
};

let currentLanguage = 'en';

function setLanguage(lang) {
    if (translations[lang]) {
        currentLanguage = lang;
        localStorage.setItem('safepay_language', lang);
        updateAllText();
    }
}

function t(key) {
    return translations[currentLanguage][key] || translations.en[key] || key;
}

function updateAllText() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key);
    });
}

// Initialize language
const savedLang = localStorage.getItem('safepay_language');
if (savedLang && translations[savedLang]) {
    currentLanguage = savedLang;
}