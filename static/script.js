function showHistory(sensorName) {
  fetch(`/api/pressure/${sensorName}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('history-container');
      const chart = document.getElementById('chart-container');

      if (data.error) {
        container.innerHTML = `<p>에러: ${data.error}</p>`;
        chart.innerHTML = '';
        return;
      }

      const listItems = data.map((row, idx) => `<li>${row.value}</li>`).join('');
      container.innerHTML = ` <h3 style="text-align: center; margin-bottom: 15px;">${sensorName} Sensor History</h3>
                              <ul style="list-style-position: outside; padding-left: 10px; text-align: left; margin: 0;">
      ${listItems} </ul>`;


      const values = data.map(row => row.value);
      const xValues = Array.from({ length: values.length }, (_, i) => i+1);

      const trace = {
        x: xValues,
        y: values,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#2e69cf' },
        name: `${sensorName} Pressure`
      };

      const layout = {
        title: `${sensorName} Sensor Graph`,
        yaxis: { title: 'Pressure' }
      };

      Plotly.newPlot('chart-container', [trace], layout);
    })
    .catch(err => {
      console.error("이력 조회 실패:", err);
    });
}

document.addEventListener('DOMContentLoaded', function () {
  const layout = {
    title: 'Sensor Graph (Select a sensor)',
    xaxis: { visible: false },
    yaxis: { title: 'Pressure' }
  };

  const trace = {
    x: [],
    y: [],
    type: 'scatter',
    mode: 'lines',
    line: { color: '#ccc' },
    name: 'Empty'
  };

  Plotly.newPlot('chart-container', [trace], layout);
});