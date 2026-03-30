document.addEventListener('DOMContentLoaded', function () {
    const deleteBtn = document.getElementById('post-delete-btn');
    const modal = document.getElementById('post-delete-modal');
    const confirmBtn = document.getElementById('confirm-post-delete');
    const cancelBtn = document.getElementById('cancel-post-delete');
    const form = document.getElementById('post-delete-form');

    if (!deleteBtn || !modal) return;

    deleteBtn.addEventListener('click', function () {
        modal.style.display = 'flex';
    });

    cancelBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    confirmBtn.addEventListener('click', function () {
        form.submit();
    });

});