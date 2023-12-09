// Minio Configuration
const minioClient = new Minio.Client({
    endPoint: 'minio',
    port: 9000,
    useSSL: false,
    accessKey: 'rootuser',
    secretKey: 'rootpass123',
});

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

// Function to fetch data from Minio and update the chart
async function fetchDataAndUpdateChart() {
    try {
        // Replace 'your-bucket' and 'your-object' with your Minio bucket and object details
        const dataStream = await minioClient.getObject('output', 'a9c9fc2fdb3b4b058e0fe0a062a8eba5_diarization.json');

        let data = '';
        dataStream.on('data', (chunk) => {
            data += chunk;
        });

        dataStream.on('end', () => {
            // Parse the data (adjust accordingly based on your data format)
            const parsedData = JSON.parse(data);
            // parsedData template 
            // {
            //     '1': 
            //     {
            //         'start_times': [20, 130], 
            //         'end_times': [20, 160], 
            //         'words': ['okay', 'red', "let's", 'get', 'the', 'black', 'one'], 
            //         'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            //     }, 
            //     '2': 
            //     {
            //         'start_times': [20, 180], 
            //         'end_times': [130, 300], 
            //         'words': ["I'm", 'here', 'hi', "I'd", 'like', 'to', 'buy', 'a', 'Chromecast', 'and', 'I', 'was', 'wondering', 'whether', 'you', 'could', 'help', 'me', 'with', 'that', 'certainly', 'which', 'color', 'would', 'you', 'like', 'we', 'have', 'blue', 'black', 'and', 'okay', 'great', 'would', 'you', 'like', 'the', 'new', 'Chromecast', 'Ultra', 'model', 'or', 'the', 'regular', 'Chromecast', 'regular', 'Chromecast', 'is', 'fine', 'okay', 'sure', 'would', 'you', 'like'], 
            //         'emotion': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0]
            //     }
            // }
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
        });
    } catch (error) {
        console.error('Error fetching data from Minio:', error);
    }
}

// Fetch and update data initially
fetchDataAndUpdateChart();

// Optionally, set up an interval to periodically update the chart
// setInterval(fetchDataAndUpdateChart, 60000); // Update every minute (adjust as needed)
