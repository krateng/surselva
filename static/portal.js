
var localisation = {};

function pageLoad() {
	listVideos();
}



function sendVideo() {
	document.getElementById("status").innerHTML = localisation["ADDVIDEO"];
	var url = document.getElementById("yturl").value;
	id = url.replace(/.*v=(.*?)/,"$1")
	id = id.replace(/(.*?)&.*/,"$1")
	var audio = document.getElementById("audio").checked;


	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = sendVideoDone;
	
	var data = {
	  add: id,
	  audioonly: audio
	};
	var searchParams = new URLSearchParams(data);
	xhttp.open("GET", "/xhttp?" + searchParams.toString(), true);
	console.log("Sending xhttp request to add id " + id);
	xhttp.send();
	console.log("Sent!");
}

function sendVideoDone() {
	if (this.readyState == 4 && this.status == 200) {
		document.getElementById("status").innerHTML = localisation[this.responseText];
		document.getElementById("yturl").value = "";

		window.setTimeout(clear,2000);
	}

}

function clear() {
	document.getElementById("status").innerHTML = "&nbsp;";
	listVideos();
}





function listVideos() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = listVideosDone;

	xhttp.open("GET", "/xhttp?list=yes", true);
	console.log("Sending xhttp request to show video list");
	xhttp.send();
	console.log("Sent!");
}

function listVideosDone() {
	if (this.readyState == 4 && this.status == 200) {
		var filelist = this.responseText;
		document.getElementById("filelist").innerHTML = filelist;
	}
}

function deleteVideo(id) {
	console.log("Deleting " + id);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = deleteVideoDone;

	xhttp.open("GET", "/xhttp?delete=" + id, true);
	console.log("Sending xhttp request to delete video " + id);
	xhttp.send();
	console.log("Sent!");
}

function deleteVideoDone() {
	console.log("Deleted!");
	location.reload();
}
