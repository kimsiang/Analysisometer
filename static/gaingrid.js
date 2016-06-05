$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port);

	(function askForGains() {
		socket.emit('all gains');
		setTimeout(askForGains, 2000);
	})();

	socket.on('sipm gain', function(msg) {
		$('#sipm'.concat(msg.num)).text(msg.gain);	
	});

	$('#setAllGains').keydown(function(e) {
		if (e.which == 13) {
			socket.emit('set all gains', {'new_gain' : $('#setAllGains').val()});
			$('#setAllGains').val('');
		}
	});

	$('#downloadGains').click( function() {
		console.log('test');
		var fileName = prompt('enter file name (leave out file extension)', '');
		fileName = fileName.replace(/ /g, '');
		//remove unfriendly characters
		fileName = fileName.replace(/[^a-zA-Z0-9-_.]/g, '');
		if (!fileName.length) {
			alert("bad filename!");
		} else {
			window.location.assign('/gainfile_' + fileName);
		}
	});

       
});
