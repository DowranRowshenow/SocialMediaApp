const notificationSocket = new WebSocket('ws://' + window.location.host + '/ws/notifications/' + userName + '/');

/* WEBSOCKETS */
notificationSocket.onmessage = function(e)
{
    const data = JSON.parse(e.data);
}