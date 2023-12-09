document.getElementById('fileInput').addEventListener('change', handleFileSelect);

const inputFileName = 'test.json';
// {
//     '1': 
//     {
//         'start_times': [0, 16, 25], 
//         'end_times': [1, 19, 27], 
//         'words': ["let's", 'get', 'the', 'black', 'Express', 'Express', 'please', 'thank', 'you', 'bye'], 
//         'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0]
//     }, 
//     '2': 
//     {
//         'start_times': [1, 21], 
//         'end_times': [16, 24], 
//         'words': ['one', 'okay', 'great', 'would', 'you', 'like', 'the', 'new', 'Chromecast', 'Ultra', 'model', 'or', 'the', 'regular', 'Chromecast', 'regular', 'Chromecast', 'is', 'fine', 'okay', 'sure', 'would', 'you', 'like', 'to', 'ship', 'it', 'regular', 'or', 'terrific', "it's", 'on', 'the', 'way', 'thank', 'you', 'very', 'much'], 
//         'emotion': [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
//     }
// }

// Trigger file handling on page load
window.onload = function () {
    handleFileSelect(inputFileName);
};

function handleFileSelect(fileName) {
    fetch(fileName)
        .then(response => response.json())
        .then(data => plotData(data))
        .catch(error => console.error('Error reading the file:', error));
}

// Chart Configuration
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Minio Data',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false,
        }],
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
            },
            y: {
                type: 'linear',
                position: 'left',
            },
        },
    },
});

function plotData(parsedData) {
    const segmentKeys = Object.keys(parsedData);
    const chartData = segmentKeys.map(key => parsedData[key].emotion);
        
    // TODO :Update chart labels  with 1 and 2 and data with emotion
    const chartLabels = Array.from({ length: chartData.length }, (_, index) => index.toString());

    const chartDatasets = segmentKeys.map(key => ({
        label: `Segment ${key}`,
        data: parsedData[key].emotion,
        borderColor: `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`, // Random border color for each segment
        borderWidth: 2,
        fill: false,
    }));

    myChart.data.labels = chartLabels;
    myChart.data.datasets = chartDatasets;
    // Update the chart
    myChart.update();
    
}
