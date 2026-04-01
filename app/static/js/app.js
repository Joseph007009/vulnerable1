// ShopCorp - Frontend JS
// EDUCATIONAL: minimal client-side validation (easily bypassed)
document.addEventListener('DOMContentLoaded', function() {
    var searchForm = document.querySelector('form[method="POST"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            var query = searchForm.querySelector('[name="query"]');
            if (query && query.value.length > 200) {
                e.preventDefault();
                alert('Search query too long');
            }
        });
    }
});
