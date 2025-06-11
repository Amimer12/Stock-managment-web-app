function loadGoogleTranslate() {
    console.log("[GT] loadGoogleTranslate() called");
    new google.translate.TranslateElement({
        pageLanguage: 'fr',
        includedLanguages: 'fr,ar',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
}

function loadGoogleTranslateScript() {
    if (window.google && google.translate && typeof google.translate.TranslateElement === 'function') {
        console.log("[GT] Google Translate already loaded");
        loadGoogleTranslate();
        return;
    }

    console.log("[GT] Injecting Google Translate script...");
    const script = document.createElement("script");
    script.src = "//translate.google.com/translate_a/element.js?cb=loadGoogleTranslate";
    script.async = true;
    document.head.appendChild(script);
}

function replaceLangLink() {
    console.log("[GT] Waiting for 'Langue' link...");
    const interval = setInterval(() => {
        const langLink = Array.from(document.querySelectorAll(".nav-item a")).find(
            a => a.textContent.trim().toLowerCase().includes("langue")
        );

        if (langLink) {
            console.log("[GT] Found 'Langue' link, replacing with Translate widget");

            const container = document.createElement("div");
            container.id = "google_translate_element";

            // Replace link with widget
            langLink.parentElement.replaceChild(container, langLink);

            loadGoogleTranslateScript();
            clearInterval(interval);
        }
    }, 300);
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("[GT] DOMContentLoaded: initializing...");
    replaceLangLink();
});
