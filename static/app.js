$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/ws');

    socket.on('countdown', function(data) {
        $('#clock').text(data.countdown);
    });
});
