const list_input = document.getElementById('list_input');
const list_btn = document.getElementById('list_btn');
const search_input = document.getElementById('search_input');
const search_btn = document.getElementById('search_btn');
const specific_input = document.getElementById('specific_input');
const specific_btn = document.getElementById('specific_btn');
const episodes_input = document.getElementById('episodes_input');
const episodes_btn = document.getElementById('episodes_btn');


list_btn.addEventListener('click', function () {
    window.open(list_input.value, '_blank');
});

search_btn.addEventListener('click', function () {
    window.open(search_input.value, '_blank')
});

specific_btn.addEventListener('click', function () {
    window.open(specific_input.value, '_blank')
});

episodes_btn.addEventListener('click', function () {
    window.open(episodes_input.value, '_blank')
});