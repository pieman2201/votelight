const socket = io.connect('http://' + document.domain + ':' + location.port + '/ws');

$(document).ready(function() {
    socket.on('countdown', function(data) {
        $('#clock').text(data.countdown);
    });

    socket.on('resume', function(data) {
        $('#voter-interface').show();
        $('#voter-result').hide()
        $('#vote-time').show();
        $('#rest-time').hide();
        $('#current-hex').text(data.color);
        $('#current-box').css('background', data.color);
    });


    socket.on('result', function(data) {

        $('#r_count').text(data.tally.R);
        $('#g_count').text(data.tally.G);
        $('#b_count').text(data.tally.B);

        $('#vote-time').hide();
        $('#rest-time').show();

        $('#voter-interface').hide();
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
    if (candidate === 'R') {
        $('#vote').css('color', 'red');
    } else if (candidate === 'G') {
        $('#vote').css('color', 'green');
    } else if (candidate === 'B') {
        $('#vote').css('color', 'blue');
    } else {
        $('#vote').css('color', 'white');
    }

    $('#voter-interface').hide();
    $('#voter-result').show()
}


