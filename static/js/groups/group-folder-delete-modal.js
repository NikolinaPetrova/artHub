document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.folder-delete-btn');
    const modal = document.getElementById('folder-delete-modal');
    const confirmBtn = document.getElementById('confirm-folder-delete');
    const cancelBtn = document.getElementById('cancel-folder-delete');
    let currentForm = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            currentForm = this.closest('.folder-delete-form');
            modal.style.display = 'flex';
        });
    });

    confirmBtn.addEventListener('click', function () {
        if (currentForm) {
            currentForm.submit();
        }
    });

    cancelBtn.addEventListener('click', function () {
        modal.style.display = 'none';
        currentForm = null;
    });

});