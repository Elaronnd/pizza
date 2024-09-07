document.addEventListener('DOMContentLoaded', function() {
    var checkbox = document.getElementById('confirm-checkbox');
    var deleteButton = document.getElementById('delete-account');

    checkbox.addEventListener('change', function() {
        deleteButton.classList.toggle('disabled', !this.checked);
        deleteButton.style.pointerEvents = this.checked ? 'auto' : 'none';
    });

    window.confirmDelete = function() {
        if (checkbox.checked) {
            return confirm('Ви впевнені, що хочете видалити ваш акаунт?');
        } else {
            alert('Будь ласка, підтвердіть видалення акаунту.');
            return false;
        }
    }
});
