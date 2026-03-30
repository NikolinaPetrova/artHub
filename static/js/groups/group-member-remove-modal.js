document.addEventListener('DOMContentLoaded', function () {
    const removeButtons = document.querySelectorAll('.member-remove-btn');
    const modal = document.getElementById('member-remove-modal');
    const confirmBtn = document.getElementById('confirm-member-remove');
    const cancelBtn = document.getElementById('cancel-member-remove');
    let currentForm = null;

    removeButtons.forEach(button => {
        button.addEventListener('click', function () {
            currentForm = this.closest('.member-remove-form');
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