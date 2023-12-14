// document.getElementById('fileInput').addEventListener('change', handleFileSelect);


// function handleFileSelect(event) {
//     const file = event.target.files[0];

//     if (!file) {
//         console.error('No file selected');
//         return;
//     }

//     const reader = new FileReader();

//     reader.onload = function (e) {
//         const jsonData = JSON.parse(e.target.result);
//         console.log(jsonData);
//         plotData(jsonData);
//     };

//     reader.readAsText(file);
// }

function fetchDataFromBackend() {
    fetch('http://34.133.166.127/visualization') // Replace with the actual URL of your Python backend endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(jsonData => {
            // Assuming the backend response follows the structure mentioned in the backend code
            // The 'plotData' function should be defined to handle the processed data
            handleVisualizationResponse(jsonData);
            // plotData(jsonData);
        })
        .catch(error => console.error('Error fetching or processing data:', error.message));
}

function handleVisualizationResponse(visData) {
    // Check for the presence of the 'error' property in the response
    if ('error' in visData) {
        // Handle the case where an error occurred on the server
        console.error('Server error:', visData.error);
    } else {
        // Assuming the 'plotData' function is defined to handle the visualization data
        console.log(visData);
        plotData(visData);
    }
}

// Chart Configuration
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [],
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

borderColors = [
    `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`,
    `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`,
]; // Random border color for each segment





function plotData(parsedData) {
    const segmentKeys = Object.keys(parsedData);
    console.log(segmentKeys)
    // Ensure there are always two speakers
    const speaker1 = segmentKeys.includes('1') ? '1' : '0';
    const speaker2 = segmentKeys.includes('2') ? '2' : '0';

    // Create an array of chart data for both speakers
    // const chartData = [
    //     parsedData[speaker1] ? parsedData[speaker1].emotion : Array.from({ length: parsedData[speaker2].emotion.length }).fill(0),
    //     parsedData[speaker2] ? parsedData[speaker2].emotion : Array.from({ length: parsedData[speaker1].emotion.length }).fill(0),
    // ];
    const chartData = [
        parsedData[speaker1] ? parsedData[speaker1].emotion : Array.from({ length: Object.values(parsedData)[0].emotion.length }).fill(0),
        parsedData[speaker2] ? parsedData[speaker2].emotion : Array.from({ length: Object.values(parsedData)[0].emotion.length }).fill(0),
    ];
    console.log(chartData);
    // const fileInput = document.getElementById('fileInput');
    // const fileName = fileInput.value.split('\\').pop().split('/').pop();
    const fileName = parsedData['filename'];
    // const checkIndex = fileName.indexOf('check');
    const checkNumber = parseInt(fileName.substring( 5));
    console.log(checkNumber);
    const chartLabels = Array.from({ length: chartData[0].length }, (_, index) => (index + checkNumber).toString());
    console.log(chartLabels);
    const chartDatasets = [
        {
            label: `Speaker ${speaker1}`,
            data: chartData[0],
            borderColor: borderColors[0],
            borderWidth: 2,
            fill: false,
        },
        {
            label: `Speaker ${speaker2}`,
            data: chartData[1],
            borderColor: borderColors[1],
            borderWidth: 2,
            fill: false,
        },
    ];

    myChart.data.labels.push(...chartLabels);

    chartDatasets.forEach((newDataset, index) => {
        if (myChart.data.datasets.length <= index) {
            // If the dataset doesn't exist yet, create it
            myChart.data.datasets.push({ data: newDataset.data, label: newDataset.label, borderColor: newDataset.borderColor, borderWidth: newDataset.borderWidth, fill: newDataset.fill });
        } else {
            // If the dataset exists, append to it
            myChart.data.datasets[index].data.push(...newDataset.data);
        }
    });

    // Update the chart
    myChart.update();
    
    
    console.log(myChart.data.labels);
    console.log(myChart.data.datasets);
    // Update the chart
    myChart.update();
    
}

fetchDataFromBackend();
setInterval(fetchDataFromBackend, 30000);
