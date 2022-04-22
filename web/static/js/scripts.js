window.onload = function () {
  var socket = io('http://10.174.200.1:5000')

  function addToChat(msg) {
    console.log(msg)
    const chat = document.querySelector('.chat')

    chat.innerHTML = `<h1>${msg}</h1>`
  }

  socket.on('connect', () => {
    socket.send('Usuário conectado ao socket!')
  })

  document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault()
    socket.emit('sendMessage', {
      name: event.target[0].value,
      message: event.target[1].value,
    })
    //event.target[0].value = ''
    //event.target[1].value = ''
  })

  socket.on('getMessage', msg => {
    addToChat(msg)
  })

  socket.on('message', msgs => {
    for (msg of msgs) {
      addToChat(msg)
    }
  })
}
