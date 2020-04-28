const root = 'http://127.0.0.1:8000/api/tv_series/';
const search_bar = document.getElementById('searchbar');
const output = document.getElementById('test');

search_bar.oninput = async function () {
    if (this.value.length >=3 ){
        let results = await fetch_search();
        display_results(results);
    } else {

    }
};

async function fetch_search() {
    const response = await fetch(root+'?search='+search_bar.value);
    const results = await response.json();
    return results;
}

function display_results(results) {
    output.innerHTML = '';
    for (let i=0; i<results.length; i++){
        output.innerHTML += '<a href=\'' + create_result_url(results[i]) +'\'>' +
        results[i].title + ' ' + '</a>';
    }
}

function create_result_url(result){
    return window.location.href+result.pk;
}