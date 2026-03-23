document.addEventListener('DOMContentLoaded', function () {
    const addFolderBtn = document.getElementById('add-folder-btn');
    const modal = document.getElementById('folder-modal');
    const cancelBtn = document.getElementById('cancel-folder');

    addFolderBtn.addEventListener('click', function (e) {
        e.preventDefault();
        modal.style.display = 'block';
    });

    cancelBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

});