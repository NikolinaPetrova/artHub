document.addEventListener('DOMContentLoaded', () => {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const artworksContainer = document.getElementById('artworks-container');

    if (!loadMoreBtn || !artworksContainer) {
        return;
    }

    loadMoreBtn.addEventListener('click', async () => {
        const page = loadMoreBtn.dataset.page;
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('page', page);
        try {
            loadMoreBtn.disabled = true;
            loadMoreBtn.textContent = 'Loading...';
            const response = await fetch(currentUrl.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to load more artworks.');
            }

            const data = await response.json();
            artworksContainer.insertAdjacentHTML('beforeend', data.html);

            if (data.has_next) {
                loadMoreBtn.dataset.page = data.next_page_number;
                loadMoreBtn.disabled = false;
                loadMoreBtn.textContent = 'Load more';
            } else {
                loadMoreBtn.remove();
            }
        } catch (error) {
            loadMoreBtn.disabled = false;
            loadMoreBtn.textContent = 'Load more';
            console.error(error);
        }
    });
});