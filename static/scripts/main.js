var REFRESHRATE = 1000;
var newImage;
var recording = false;

function sendRequest(route, callback){
    request = new XMLHttpRequest();

    request.onload = callback;

    request.open('GET', route, true);
    request.send();
}

function addEventListeners(object, events, callback){
    eventArray = events.split(' ');
    for(var i = 0, n = events.length; i<n; i++){
        object.addEventListener(eventArray[i], callback, false);
    }
    
}

function updateImage() {
    document.getElementById("image").src = newImage.src

    newImage = new Image();
    newImage.src = "/image?" + Date.now()
}

function toggleRecord() {
    sendRequest('record')

    recording = !recording
    
    recordButton.innerText = recording?'Stop Recording':'Start Recording'
}

window.onload = function(){
    sendRequest('/stop'); // Stop the car if it is moving
};

forwardButton = document.getElementById('fwd');
backwardButton = document.getElementById('bck');
leftButton = document.getElementById('left');
rightButton = document.getElementById('right');
stopButton = document.getElementById('stop');
recordButton = document.getElementById('record');

addEventListeners(forwardButton, 'touchstart', function(){sendRequest('drive/forward')});
addEventListeners(backwardButton, 'touchstart', function(){sendRequest('drive/backward')});
addEventListeners(leftButton, 'touchstart', function(){sendRequest('drive/left')});
addEventListeners(rightButton, 'touchstart', function(){sendRequest('drive/right')});
addEventListeners(stopButton, 'touchstart', function(){sendRequest('drive/stop')});

addEventListeners(forwardButton, 'touchend touchcancel', function(){sendRequest('drive/stop')});
addEventListeners(backwardButton, 'touchend touchcancel', function(){sendRequest('drive/stop')});
addEventListeners(leftButton, 'touchend touchcancel', function(){sendRequest('drive/straight')});
addEventListeners(rightButton, 'touchend touchcancel', function(){sendRequest('drive/straight')});

addEventListeners(recordButton, 'touchstart', toggleRecord);

newImage = new Image();
newImage.src = "/image?" + Date.now();

setInterval(updateImage, REFRESHRATE);
