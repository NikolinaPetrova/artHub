function showTab(tabId) {
    const tabs = document.querySelectorAll(".tab");

    tabs.forEach(tab => {
        tab.style.display = "none";
    });

    const activeTab = document.getElementById(tabId);
    activeTab.style.display = "block";
}