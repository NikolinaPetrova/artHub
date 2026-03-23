document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.reply-toggle, .edit-toggle').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();

            const actions = button.closest('.comment-actions');
            actions.querySelectorAll('.action-btn').forEach(btn => btn.style.display = 'none');

            if (button.classList.contains('edit-toggle')) {
                const form = actions.querySelector('.edit-form');
                const contentInput = form.querySelector('input[name="content"]');
                const commentIdInput = form.querySelector('input[name="comment_id"]');

                form.style.display = 'flex';
                form.style.gap = '10px';
                contentInput.value = button.dataset.content;
                commentIdInput.value = button.dataset.comment;
                contentInput.focus();

            } else if (button.classList.contains('reply-toggle')) {
                const form = actions.querySelector('.reply-form');
                const parentIdInput = form.querySelector('input[name="parent_id"]');
                const commentIdInput = form.querySelector('input[name="comment_id"]');
                const contentInput = form.querySelector('input[name="content"]');

                form.style.display = 'flex';
                parentIdInput.value = button.dataset.parent;
                commentIdInput.value = '';
                contentInput.value = '';
                contentInput.focus();
            }
        });
    });
    document.addEventListener('click', () => {
        document.querySelectorAll('.comment-actions').forEach(actions => {
            actions.querySelectorAll('.inline-form').forEach(form => form.style.display = 'none');
            actions.querySelectorAll('.action-btn').forEach(btn => btn.style.display = 'inline-block');
        });
    });
    document.querySelectorAll('.inline-form').forEach(form => {
        form.addEventListener('click', e => e.stopPropagation());
    });
});