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
      if (data.error) {
        container.innerHTML = `<p>에러: ${data.error}</p>`;
        return;
      }

      const listItems = data.map((row) => `<li>${row.value}</li>`).join('');
      container.innerHTML = `
        <h3>${sensorName} Sensor History</h3>
        <ul>${listItems}</ul>
      `;
    })
    .catch(err => {
      const container = document.getElementById('history-container');
      container.innerHTML = `<p>에러: ${err.message}</p>`;
      console.error("이력 조회 실패:", err);
    });
}
