const root = 'http://127.0.0.1:8000/api/tv_series/';
const search_bar = document.getElementById('searchbar');
const output = document.getElementById('results_list');

search_bar.oninput = async function () {
    if (this.value.length >=3 ){
        let results = await fetch_search();
        display_results(results);
    } else {
        output.innerHTML = '';
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
        let li = document.createElement('li');
        li.className = 'list-group-item';

        let a = document.createElement('a');
        a.href = create_result_url(results[i]);
        a.text = results[i].title;
        if (results[i].original_title != null){
            a.text += ' (' + results[i].original_title + ')';
        }
        a.className ='pl-3';

        let poster = document.createElement('img');
        poster.src = results[i].poster_url;
        poster.height = 100;

        li.appendChild(poster);
        li.appendChild(a);
        output.appendChild(li);
    }
}

function create_result_url(result){
    return window.location.href.split('?')[0] + result.pk;
}