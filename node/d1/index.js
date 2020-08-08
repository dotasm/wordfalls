var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var amqp = require('amqplib');


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

/*
io.on('connection', (socket) => {
  io.emit('chat message', init_msg);

  socket.on('chat message', (msg) => {
    console.log('message: ' + msg);
    if (msg == 'fire') {
      io.emit('chat message', fire_msg);
    } else {
      io.emit('chat message', msg);
    }
  });
});
*/

amqp.connect('amqp://localhost').then(function(conn) {
  process.once('SIGINT', function() { conn.close(); });
  return conn.createChannel().then(function(ch) {

    var ok = ch.assertQueue('pipe_api', {durable: false});

    ok = ok.then(function(_qok) {
      return ch.consume('pipe_api', function(msg) {
        // add websocket
        /*if (msg.content.toString() == 'fire') {
          io.emit('chat message', fire_msg);
        }*/
        io.emit('chat message', msg.content.toString());

        console.log(" [x] Received '%s'", msg.content.toString());
      }, {noAck: true});
    });

    return ok.then(function(_consumeOk) {
      console.log(' [*] Waiting for messages. To exit press CTRL+C');
    });
  });
}).catch(console.warn);

http.listen(3000, () => {
  console.log('listening on *:3000');
});