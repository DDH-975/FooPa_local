// const express = require('express');
// const http = require('http');
// const socketIo = require('socket.io');
//
// const app = express();
// const server = http.createServer(app);
// const io = socketIo(server);
//
// const PORT = process.env.PORT || 3000;
//
// io.on('connection', (socket) => {
//   console.log('New client connected');
//
//   socket.on('callShopper', (data) => {
//     console.log('Shopper called:', data);
//     // Broadcast to all connected shopper clients
//     io.emit('shopperAlert', data);
//   });
//
//   socket.on('disconnect', () => {
//     console.log('Client disconnected');
//   });
// });
//
// server.listen(PORT, () => {
//   console.log(`Server is running on port ${PORT}`);
// });