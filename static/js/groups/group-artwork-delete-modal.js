document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.artwork-delete-btn');
    const modal = document.getElementById('artwork-delete-modal');
    const confirmBtn = document.getElementById('confirm-artwork-delete');
    const cancelBtn = document.getElementById('cancel-artwork-delete');
    let currentForm = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            currentForm = this.closest('.artwork-delete-form');
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