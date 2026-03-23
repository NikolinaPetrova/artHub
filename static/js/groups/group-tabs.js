function showTab(tabId) {
    const tabs = document.querySelectorAll(".tab");

    tabs.forEach(tab => {
        tab.style.display = "none";
    });

    const activeTab = document.getElementById(tabId);
    activeTab.style.display = "block";

    const url = new URL(window.location);
    url.searchParams.set("tab", tabId);
    window.history.replaceState({}, "", url);
}