document.addEventListener("DOMContentLoaded", () => {
  const sensors = ["P1", "P2", "P3", "P4", "P5"];
  sensors.forEach(sensor => {
    const button = document.getElementById(sensor);
    if (button) {
      button.addEventListener("click", () => showHistory(sensor));
    }
  });
});

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

      // 텍스트 목록 출력
      const listItems = data.map((row, idx) => `<li>${row.value}</li>`).join('');
      container.innerHTML = `<h3>${sensorName} Sensor History</h3><ul>${listItems}</ul>`;

      // Plotly 그래프 출력
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
        xaxis: { title: 'Index' },
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
