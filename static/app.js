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

    player = OvenPlayer.create("player", {
        sources: [
            {
                "file": "ws://" + document.domain + ":3333/app/stream",
                "label": "webrtc-0",
                "type": "webrtc"
            }
        ],
        autoStart: true,
        controls: false,
        mute: true,
        volume: 0
    });
});

function vote(candidate) {
    socket.emit('tally_vote', candidate);
    $('#vote').text(candidate);

    $('#voter-interface').hide();
    $('#voter-result').show()
}


