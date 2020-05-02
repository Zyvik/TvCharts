const arrow_up = document.getElementById('arrow_up');
const arrow_down = document.getElementById('arrow_down');
const filter_header = document.getElementById('filter_header');
const filter_container = document.getElementById('filter_container');

filter_header.addEventListener('click', function () {
    swap_arrows();
});

function swap_arrows() {
    if (arrow_down.style.display === 'none') {
        arrow_down.style.display = 'inline';
        arrow_up.style.display = 'none';
        filter_container.style.display = 'none';
    } else {
        arrow_down.style.display = 'none';
        arrow_up.style.display = 'inline';
        filter_container.style.display = 'block';
    }
}