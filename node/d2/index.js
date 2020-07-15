var app = require('express')();
var http = require('http').createServer(app);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.get('/pos', (req, res) => {
  res.sendFile(__dirname + '/align.html');
})

app.get('/ali', (req, res) => {
  res.sendFile(__dirname + '/ali2.html');
})

http.listen(3000, () => {
  console.log('listening on *:3000');
});