$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port);

	socket.on('get status', function(msg) {

                var i = msg.num;	
                var j = msg.ftype;	
                var n = msg.ftype;	
                $('#file_label'.concat(j.toString()).concat(i.toString())).text(msg.name);
	        $('#file_label'.concat(j.toString()).concat(i.toString())).removeClass('').addClass('label-success');
                if(n == 4) {$('#file_status'.concat(j.toString()).concat(i.toString())).text(msg.stat); }
                else if(n == 5) {$('#file_status'.concat(j.toString()).concat(i.toString())).text('Last run in the list: ' + msg.stat); }
                else {$('#file_status'.concat(j.toString()).concat(i.toString())).text(msg.stat + ' MB'); }
	        $('#file_status'.concat(j.toString()).concat(i.toString())).removeClass('').addClass('label-success');

	    });
    });
