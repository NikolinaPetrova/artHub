const container = document.getElementById('tag-container');
    document.querySelector('.scroll-btn.left').addEventListener('click', () => {
        container.scrollBy({ left: -150, behavior: 'smooth' });
    });
    document.querySelector('.scroll-btn.right').addEventListener('click', () => {
        container.scrollBy({ left: 150, behavior: 'smooth' });
    });