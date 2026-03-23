document.addEventListener('DOMContentLoaded', function() {
    const deleteBtn = document.getElementById('delete-btn');
    const modal = document.getElementById('delete-modal');
    const confirmBtn = document.getElementById('confirm-delete');
    const cancelBtn = document.getElementById('cancel-delete');
    const form = document.querySelector('.delete-group-form');

    if (deleteBtn && modal && confirmBtn && cancelBtn && form) {
        deleteBtn.addEventListener('click', () => modal.style.display = 'block');
        cancelBtn.addEventListener('click', () => modal.style.display = 'none');
        confirmBtn.addEventListener('click', () => form.submit());
    }

    const params = new URLSearchParams(window.location.search);
    const tab = params.get("tab") || "gallery";

    showTab(tab);
});