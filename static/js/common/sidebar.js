document.addEventListener("DOMContentLoaded", () => {
    const menuBtn = document.querySelector('.menu-btn');
    const sidebar = document.querySelector('.sidebar');

    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        sidebar.classList.toggle('collapsed');
    });

    document.addEventListener('click', (e) => {
        const isClickInsideSidebar = sidebar.contains(e.target);
        const isClickOnMenuBtn = menuBtn.contains(e.target);

        if (!isClickInsideSidebar && !isClickOnMenuBtn && !sidebar.classList.contains('collapsed')) {
            sidebar.classList.add('collapsed');
        }
    });

    sidebar.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});