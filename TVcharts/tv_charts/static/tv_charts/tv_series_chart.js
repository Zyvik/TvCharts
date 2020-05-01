const root = 'http://127.0.0.1:8000/api/tv_series/';
const chart = document.getElementById('chart').getContext('2d');
const pk = document.getElementById('pk');
const notice = document.getElementById('notice');
const season_colors = [
    'rgba(0, 0, 0 , 0.8)',
    'rgba(255, 255, 255, 0.8)'
];

async function fetch_episodes(pk) {
    const response = await fetch(root + pk.innerHTML + '/episodes');
    const results = await response.json();
    return results;
}

function prepare_data(data){
    let rating = [];
    let labels = [];
    let background_color = [];
    let border_color = [];

    for (let i=0; i<data.length; i++){
        rating.push(parseFloat(data[i].rating));

        labels.push('s'+data[i].season+'e'+data[i].episode_nr + '\n' + data[i].title + '\n' + data[i].air_date + '\nvotes: ' + data[i].votes);
        background_color.push(season_colors[data[i].season % 2]);
        border_color.push('rgba(0, 0, 0, 0.2)');
    }

    let processed_data = {
        rating: rating,
        labels: labels,
        background_color: background_color,
        border_color: border_color,
    };
    return processed_data
}

function find_minimum(data){
    let min = Math.min(...data);
    console.log(data);
    if (min>5){
        min = 5;
    } else if (min <= 1){
        min = 0;
    } else {
        min = Math.floor(min-1);
    }
    return min
}
let myChart = new Chart(chart, {
    type: 'bar',
    data: {
        labels: ['API', 'Error', ':('],
        datasets: [{
            label: ['rating'],
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 2
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: false,
                    min: 0,
                    max: 10,
                    fontColor: "black"
                }
            }],
            xAxes: [{
                display: false
            }]
        }
    }
});

fetch_episodes(pk).then(data => {
    let series_data = prepare_data(data);
   myChart.data.datasets[0].data = series_data.rating;
   myChart.data.datasets[0].backgroundColor = series_data.background_color;
   myChart.data.datasets[0].borderColor = series_data.border_color;
   myChart.data.labels = series_data.labels;
   myChart.options.scales.yAxes[0].ticks.min = find_minimum(series_data.rating);
   myChart.update();

   notice.innerText = 'Notice - scale starts from ' + myChart.options.scales.yAxes[0].ticks.min + '.';
});