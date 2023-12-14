// const url = 'http://34.41.169.38/';
// const chunk_size = 1;

// Chart Configuration
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    title: 'Tone Tracking for recordings.',
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Minio Data',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: true,
        }],
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                max: 5
            },
            y: {
                type: 'linear',
                position: 'left',
                max: 10,
            },
        },
    },
});

// Function to fetch data from Minio and update the chart
async function fetchDataAndUpdateChart() {
    try {
        // Replace 'your-bucket' and 'your-object' with your Minio bucket and object details
        user = document.getElementById("uname").value;
        // const dataStream = await fetch(
        //    url,
        //     {
        //         method: 'GET',
        //         headers: {
        //             'prefix': user
        //         }
        //     }
        // ).then(response => {
        //     console.log(response);
        // });

        // let data = '';
        // dataStream.on('data', (chunk) => {
        //     data += chunk;
        // });

        parsedData = {
                    '1': 
                    {
                        'start_times': [20, 130], 
                        'end_times': [20, 160], 
                        'words': ['okay', 'red', "let's", 'get', 'the', 'black', 'one'], 
                        'emotion': [3,4,5]
                        // 'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    }, 
                    '2': 
                    {
                        'start_times': [20, 180], 
                        'end_times': [130, 300], 
                        'words': ["I'm", 'here', 'hi', "I'd", 'like', 'to', 'buy', 'a', 'Chromecast', 'and', 'I', 'was', 'wondering', 'whether', 'you', 'could', 'help', 'me', 'with', 'that', 'certainly', 'which', 'color', 'would', 'you', 'like', 'we', 'have', 'blue', 'black', 'and', 'okay', 'great', 'would', 'you', 'like', 'the', 'new', 'Chromecast', 'Ultra', 'model', 'or', 'the', 'regular', 'Chromecast', 'regular', 'Chromecast', 'is', 'fine', 'okay', 'sure', 'would', 'you', 'like'], 
                        'emotion': [5,0,0]
                        // 'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0]
                    }
        }
        const segmentKeys = Object.keys(parsedData);
        console.log(segmentKeys);
        const chartData = segmentKeys.map(key => parsedData[key].emotion);
        console.log(chartData);

            
        // TODO :Update chart labels  with 1 and 2 and data with emotion
        const chartLabels = Array.from({ length: chartData.length }, (_, index) => index.toString());
        
        const chartDatasets = segmentKeys.map(key => ({
            label: `Segment ${key}`,
            data: {x: [1,2,3], y: parsedData[key].emotion},
            borderColor: `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`, // Random border color for each segment
            borderWidth: 2,
            fill: false,
        }));
        console.log(chartDatasets);
        myChart.data.labels = chartLabels;
        myChart.data.datasets = chartDatasets;
        // myChart.draw();
        // Update the chart
        myChart.update();
        // dataStream.on('end', () => {
        //     // Parse the data (adjust accordingly based on your data format)
        //     const parsedData = JSON.parse(data);
        //     // parsedData template 
        //     // {
        //     //     '1': 
        //     //     {
        //     //         'start_times': [20, 130], 
        //     //         'end_times': [20, 160], 
        //     //         'words': ['okay', 'red', "let's", 'get', 'the', 'black', 'one'], 
        //     //         'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        //     //     }, 
        //     //     '2': 
        //     //     {
        //     //         'start_times': [20, 180], 
        //     //         'end_times': [130, 300], 
        //     //         'words': ["I'm", 'here', 'hi', "I'd", 'like', 'to', 'buy', 'a', 'Chromecast', 'and', 'I', 'was', 'wondering', 'whether', 'you', 'could', 'help', 'me', 'with', 'that', 'certainly', 'which', 'color', 'would', 'you', 'like', 'we', 'have', 'blue', 'black', 'and', 'okay', 'great', 'would', 'you', 'like', 'the', 'new', 'Chromecast', 'Ultra', 'model', 'or', 'the', 'regular', 'Chromecast', 'regular', 'Chromecast', 'is', 'fine', 'okay', 'sure', 'would', 'you', 'like'], 
        //     //         'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0]
        //     //     }
        //     // }
            
        // });
    } catch (error) {
        console.error('Error fetching data from Minio:', error);
    }
}

// Fetch and update data initially
fetchDataAndUpdateChart();

// Optionally, set up an interval to periodically update the chart
// setInterval(fetchDataAndUpdateChart, 60000); // Update every minute (adjust as needed)