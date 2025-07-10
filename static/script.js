function showHistory(sensorName) {
  fetch(`/api/pressure/${sensorName}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('history-container');
      if (data.error) {
        container.innerHTML = `<p>에러: ${data.error}</p>`;
        return;
      }

      const listItems = data.map((row, idx) => `<li>${row.value}</li>`).join('');
      container.innerHTML = `<h3>${sensorName} Sensor history</h3><ul>${listItems}</ul>`;
    })
    .catch(err => {
      console.error("이력 조회 실패:", err);
    });
}
