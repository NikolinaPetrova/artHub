document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('dashboard-container');
    const moveUrl = container.dataset.moveUrl;
    const csrfToken = container.dataset.csrf;

    const draggables = document.querySelectorAll('.art-image');
    const folders = document.querySelectorAll('.album-card');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', e => {
            e.dataTransfer.setData('art-id', draggable.dataset.artId);
        });
    });

    folders.forEach(folder => {
        folder.addEventListener('dragover', e => e.preventDefault());

        folder.addEventListener('drop', e => {
            e.preventDefault();
            const artId = e.dataTransfer.getData('art-id');
            const folderId = folder.dataset.folderId;
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = moveUrl;

            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);

            const artInput = document.createElement('input');
            artInput.type = 'hidden';
            artInput.name = 'art_id';
            artInput.value = artId;
            form.appendChild(artInput);

            const folderInput = document.createElement('input');
            folderInput.type = 'hidden';
            folderInput.name = 'folder_id';
            folderInput.value = folderId;
            form.appendChild(folderInput);

            document.body.appendChild(form);
            form.submit();
        });
    });
});