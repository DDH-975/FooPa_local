document.addEventListener('DOMContentLoaded', function() {
    const ingredientItems = document.querySelectorAll('.ingredient-item');
    ingredientItems.forEach(item => {
        item.addEventListener('click', function() {
            const checkbox = this.querySelector('input[type="checkbox"]');
            checkbox.checked = !checkbox.checked;
            if (checkbox.checked) {
                this.classList.add('checked');
            } else {
                this.classList.remove('checked');
            }
        });
    });
});
