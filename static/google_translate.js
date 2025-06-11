function loadGoogleTranslateScript() {
    if (window.google && google.translate) {
        loadGoogleTranslate();
        return;
    }

    const script = document.createElement("script");
    script.src = "//translate.google.com/translate_a/element.js?cb=loadGoogleTranslate";
    script.async = true;
    document.head.appendChild(script);
}

// Load Google Translate widget
function loadGoogleTranslate() {
    new google.translate.TranslateElement({
        pageLanguage: 'fr',
        includedLanguages: 'fr,ar',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');

    // Wait for the widget to render, then style it
    waitAndStyleDropdown();
}

// Wait for the select to appear, then style it
function waitAndStyleDropdown() {
    const interval = setInterval(() => {
        const select = document.querySelector('#google_translate_element select');
        if (select) {
            styleGoogleTranslateDropdown(select);
            clearInterval(interval);
        }
    }, 200);
}

// Apply custom styles
function styleGoogleTranslateDropdown(select) {
    select.style.padding = '6px 18px';
    select.style.borderRadius = '8px';
    select.style.fontSize = '15px';
    select.style.border = '1.5px solid #1ABC9C';
    select.style.background = '#f4f8fb';
    select.style.color = '#1ABC9C';
    select.style.fontWeight = '600';
    select.style.boxShadow = '0 2px 8px rgba(44,62,80,0.07)';
    select.style.cursor = 'pointer';
    select.style.transition = 'all 0.2s';
}

// Replace top menu "Langue" link with the widget
function replaceLangLink() {
    const langLink = Array.from(document.querySelectorAll(".nav-item a")).find(
        a => a.textContent.trim() === "Langue"
    );
    if (langLink) {
        const container = document.createElement("div");
        container.id = "google_translate_element";
        langLink.parentElement.replaceChild(container, langLink);
        loadGoogleTranslateScript();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    replaceLangLink();
});
