// Get the current URL
var urlPath = window.location.pathname;

var wsURL = "ws://127.0.0.1:8001" + urlPath;

const chatData = 'Hello, server!';

console.log(wsURL);

let socket;
let connectAttempts = 0;
let time = 1000;

function connectWebSocket(){

    socket = new WebSocket(wsURL);
    
    socket.addEventListener('open', (event) => {
        console.log("webSocket connection opened:", event);
        connectAttempts = 0;
        time = 1000;
    });
    
    socket.addEventListener('error', (event) => {
        console.log("webSocket connection error: ", event);
    });
    
    
    socket.addEventListener('close', (event) => {
        console.log("webSocket connection closed: ", event);
        connectAttempts++;
        time += 1000;
        if (connectAttempts < 15){
            setTimeout(() => {
                connectWebSocket();
            }, time);

        }
    });
    
    
    
    // Event listener for when a message is received
    socket.addEventListener('message', (event) => {
        const receivedMessage = JSON.parse(event.data);
        addChatObject(receivedMessage);
    });
}

connectWebSocket();

const send_button = document.getElementById("send-button");
const message_box = document.getElementById("message-box");

const message_form = document.getElementById("message-form");

message_form.addEventListener('submit', function(event) {
    event.preventDefault();

    var user_message = message_box.value;

    message_box.value = '';

    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    
    fetch(urlPath, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrfToken,
        },
        body : JSON.stringify({message: user_message})
    })

    .then(response => {
        return response.json()
    })

    .then(data => {
        socket.send(JSON.stringify(data));
        console.log(data);
        addChatObject(data)
    })
    .catch(error =>{
        console.log("Error: ", error);
    })

})


function addChatObject(chatData){
    const messageContainer = document.getElementById('messageContainer');

    var direction = "flex-row"
    if(chatData.created_by === user){
        direction = "flex-row-reverse"
    }
                
    messageContainer.innerHTML += `
        <div class="flex ${direction} py-2">
            <div class="p-2 bg-gray-100 rounded-lg">
                <p class="text-lg">${chatData.message}</p>
                <p class="text-sm text-gray-600">${ chatData.created_by } | ${ chatData.created_at }</p>
            </div>
        </div>
    `

    messageContainer.scrollTop = messageContainer.scrollHeight;
}