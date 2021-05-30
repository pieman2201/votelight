const socket = io.connect('http://' + document.domain + ':' + location.port + '/ws');

$(document).ready(function() {
    socket.on('countdown', function(data) {
        $('#clock').text(data.countdown);
    });

    socket.on('result', function(data) {
        $('#winner').text(data.winner);

        $('#voter-interface').show();
        $('#voter-result').hide()

    });
});

function vote(candidate) {
    socket.emit('tally_vote', candidate);
    $('#vote').text(candidate);

    $('#voter-interface').hide();
    $('#voter-result').show()
}

