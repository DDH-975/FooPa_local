// document.addEventListener('DOMContentLoaded', () => {
//   const socket = io();
//
//   socket.on('shopperAlert', (data) => {
//     const alertDiv = document.createElement('div');
//     alertDiv.classList.add('alert');
//     alertDiv.textContent = `New shopper call: ${JSON.stringify(data.items)}`;
//     document.getElementById('alerts').appendChild(alertDiv);
//   });
// });