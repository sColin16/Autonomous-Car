var REFRESHRATE = 1000; // Interval between remote control's image update

var recording = false; // Whether or not the car is recording
var automatic = false; // Whether or not the car is in auto mode

/***
 * Sends simple GET requests to control various aspects of the car
***/
function sendRequest(route, callback){
    request = new XMLHttpRequest();

    request.onload = callback;

    request.open('GET', route, true);
    request.send();
}

/***
 * Adds multiple event listeners, with names seperated by spaces
***/
function addEventListeners(object, events, callback){
    eventArray = events.split(' ');

    for(var i = 0, n = events.length; i<n; i++){
        object.addEventListener(eventArray[i], callback, false);
    }
}

/***
 * Updates the image on the remote control
 * Adds the date to change the link, and "bust" the cache
***/
function updateImage() {
    document.getElementById("image").src = "/image?" + Date.now()
}

/***
 * Toggles the automatic mode for the car
 * Updates the button's text accordingly
***/

function toggleAuto() {
    sendRequest('auto')

    automatic = !automatic

    autoButton.innerText = automatic?'Auto Off':'Auto On';
}


/***
 * Toggles the recording mode for the car
 * Updates the button's text accordingly
***/
function toggleRecord() {
    sendRequest('record')

    recording = !recording

    recordButton.innerText = recording?'Stop Recording':'Start Recording'
}

window.onload = function(){
    sendRequest('/drive/stop'); // Stop the car if it is moving ASAP
};

// Store buttons in variables to clean up code
forwardButton = document.getElementById('fwd');
backwardButton = document.getElementById('bck');
leftButton = document.getElementById('left');
rightButton = document.getElementById('right');
stopButton = document.getElementById('stop');
recordButton = document.getElementById('record');
autoButton = document.getElementById('auto');

// Events listeners for driving when buttons are pressed
addEventListeners(forwardButton, 'touchstart', function(){sendRequest('drive/forward')});
addEventListeners(backwardButton, 'touchstart', function(){sendRequest('drive/backward')});
addEventListeners(leftButton, 'touchstart', function(){sendRequest('drive/left')});
addEventListeners(rightButton, 'touchstart', function(){sendRequest('drive/right')});
addEventListeners(stopButton, 'touchstart', function(){sendRequest('drive/stop')});

// Event listeners for driving when buttons are released
addEventListeners(forwardButton, 'touchend touchcancel', function(){sendRequest('drive/stop')});
addEventListeners(backwardButton, 'touchend touchcancel', function(){sendRequest('drive/stop')});
addEventListeners(leftButton, 'touchend touchcancel', function(){sendRequest('drive/straight')});
addEventListeners(rightButton, 'touchend touchcancel', function(){sendRequest('drive/straight')});

// Event listeners for controlling car modes
addEventListeners(recordButton, 'touchstart', toggleRecord);
addEventListeners(autoButton, 'touchstart', toggleAuto)

setInterval(updateImage, REFRESHRATE); // Set update interval
