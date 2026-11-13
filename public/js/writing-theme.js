(function () {
    var systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
    function applyTheme(theme) {
        document.documentElement.dataset.theme = theme;
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.content = theme === 'dark' ? '#16181c' : '#ffffff';
        var toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.setAttribute('aria-checked', String(theme === 'dark'));
            toggle.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
        }
    }
    function followSystem() { applyTheme(systemTheme.matches ? 'dark' : 'light'); }
    followSystem();
    systemTheme.addEventListener('change', followSystem);
    window.addEventListener('pageshow', followSystem);
    document.addEventListener('DOMContentLoaded', function () {
        var toggle = document.getElementById('theme-toggle');
        if (!toggle) return;
        applyTheme(document.documentElement.dataset.theme);
        toggle.addEventListener('click', function () {
            applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
        });
    });
})();
