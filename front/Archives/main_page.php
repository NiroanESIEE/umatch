<?php
	session_start();
	
	if(!isset($_SESSION["ID"]))
		header('Location: ../');

?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8"/>
	<title>UMatch</title>
	<link rel="stylesheet" type="text/css" href="CSS/UMatch.css"></link>
</head>
<body>
	<header>
		<img id="logo" src="Logos/Logo_UMATCH.png"></img>
		<h2 id="title">UMatch</h2>
		<h2 id="about">About us</h2>
	</header>

	<div id="container">
		<video autoplay="true" id="videoElement">
		</video>
		<div id="divScreenShot">
			<canvas id="canvasScreenShoot">
				<image id="screenShootImageInCanvas"></image>
			</canvas>
			<div id="cancelScreenShotDiv" onclick="cancelScreenShootImageFunction()">
				<image id="cancelScreenShotImage" src="Logos/delete.png"></image>
			</div>
		</div>
		<div id="videoBanner">
			<div id="divSavePhoto" onclick="savePhotoFunction()">
				<image id="saveImage" src="Logos/save.png"></image>
			</div>
			<div id="divRecordImage" onclick="takePhotoFunction()">
				<image id="recordImage" src="Logos/record.png"></image>
			</div>
			<div id="divFullScreenImage" onclick="displayFullScreenFunction()">
				<image id="fullScreenImage" src="Logos/full_screen_button.png"></image>
			</div>
		</div>
		<div id="imageElementDiv">
			<!-- Upload  -->
			<form id="file-upload-form" class="uploader">
				<input id="file-upload" type="file" name="fileUpload" accept="image/*" />

				<label for="file-upload" id="file-drag">
					<img id="file-image" src="#" alt="Preview" class="hidden">
					<div id="start">
						<div>Select a file or drag here</div>
						<div id="notimage" class="hidden">Please select an image</div>
						<span id="file-upload-btn" class="btn btn-primary">Select a file</span>
					</div>
					<div id="response" class="hidden">
						<div id="messages"></div>
					</div>
				</label>
			</form>
		</div>
	</div>

	<div id="choice">
		<div id="divCameraPhoto" onclick="divCameraPhotofunction()">
			<img id="cameraPhoto" src="Logos/appareil_photo.png"></img>
		</div>
		<div id="divUploadPhoto" onclick="divUploadPhotofunction()">
			<img id="uploadPhoto" src="Logos/upload_photo.png"></img>
		</div>
	</div>

	<script>

	var enableVideo = true;
	var autorisationVideo = false;
	if (enableVideo == true) {
		divCameraPhotofunction();
	}
	else {
		divUploadPhotofunction();
	}

	//Affichage de la partie video lors du clic
	function divCameraPhotofunction(){

		document.getElementById("videoElement").style.visibility = "visible";
		document.getElementById("videoBanner").style.visibility = "visible";

		document.getElementById("imageElementDiv").style.visibility = "hidden";
		document.getElementById("divScreenShot").style.visibility = "hidden";

		var yellowColor = "#FDFD96";
		var grayColor = "#E8E8E8";
		document.getElementById("divCameraPhoto").style.backgroundColor = yellowColor;
		document.getElementById("divUploadPhoto").style.backgroundColor = grayColor;

		var video = document.querySelector("#videoElement");
		//Si jamais effectuee autorisation de la video alors demande
		if (autorisationVideo == false) {
			if (navigator.mediaDevices.getUserMedia) {
				navigator.mediaDevices.getUserMedia({video: true})
				.then(function(stream) {
					video.srcObject = stream;
					video.play();
				})
				.catch(function(err0r) {
					console.log("Something went wrong!");
				});
			}
			autorisationVideo = true;
		}
		//Si deja autorisation de la video
		else {
			video.play();
		}

	}

	//Affichage du chargement image lors du clic
	function divUploadPhotofunction(){

		document.getElementById("videoElement").style.visibility = "hidden";
		document.getElementById("videoBanner").style.visibility = "hidden";

		document.getElementById("imageElementDiv").style.visibility = "visible";
		document.getElementById("divScreenShot").style.visibility = "hidden";

		var yellowColor = "#FDFD96";
		var grayColor = "#E8E8E8";
		document.getElementById("divCameraPhoto").style.backgroundColor = grayColor;
		document.getElementById("divUploadPhoto").style.backgroundColor = yellowColor;

		var video = document.querySelector("#videoElement");
		video.pause();
	}


	//UPLOAD IMAGES
	function Upload(){
		function Init() {

			console.log("Upload Initialised");

			var fileSelect    = document.getElementById('file-upload'),
					fileDrag      = document.getElementById('file-drag'),
					submitButton  = document.getElementById('submit-button');

			fileSelect.addEventListener('change', fileSelectHandler, false);

			// Is XHR2 available?
			var xhr = new XMLHttpRequest();
			if (xhr.upload) {
				// File Drop
				fileDrag.addEventListener('dragover', fileDragHover, false);
				fileDrag.addEventListener('dragleave', fileDragHover, false);
				fileDrag.addEventListener('drop', fileSelectHandler, false);
			}
		}

		function fileDragHover(e) {
			var fileDrag = document.getElementById('file-drag');

			e.stopPropagation();
			e.preventDefault();

			fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
		}

		function fileSelectHandler(e) {
			// Fetch FileList object
			var files = e.target.files || e.dataTransfer.files;

			// Cancel event and hover styling
			fileDragHover(e);

			// Process all File objects
			for (var i = 0, f; f = files[i]; i++) {
				parseFile(f);
				uploadFile(f);
			}
		}

		// Output
		function output(msg) {
			// Response
			var m = document.getElementById('messages');
			m.innerHTML = msg;
		}

		function parseFile(file) {

			console.log(file.name);
			output(
				'<strong>' + encodeURI(file.name) + '</strong>'
			);

			// var fileType = file.type;
			// console.log(fileType);
			var imageName = file.name;

			var isGood = (/\.(?=gif|jpg|png|jpeg)/gi).test(imageName);
			if (isGood) {
				document.getElementById('start').classList.add("hidden");
				document.getElementById('response').classList.remove("hidden");
				document.getElementById('notimage').classList.add("hidden");
				// Thumbnail Preview
				document.getElementById('file-image').classList.remove("hidden");
				document.getElementById('file-image').src = URL.createObjectURL(file);
			}
			else {
				document.getElementById('file-image').classList.add("hidden");
				document.getElementById('notimage').classList.remove("hidden");
				document.getElementById('start').classList.remove("hidden");
				document.getElementById('response').classList.add("hidden");
				document.getElementById("file-upload-form").reset();
			}
		}


		function uploadFile(file) {

			var xhr = new XMLHttpRequest(),
				fileInput = document.getElementById('class-roster-file'),
				pBar = document.getElementById('file-progress'),
				fileSizeLimit = 1024; // In MB
			if (xhr.upload) {
				// Check if file is less than x MB
				if (file.size <= fileSizeLimit * 1024 * 1024) {
					// Progress bar
					pBar.style.display = 'inline';
					xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);
					xhr.upload.addEventListener('progress', updateFileProgress, false);

					// File received / failed
					xhr.onreadystatechange = function(e) {
						if (xhr.readyState == 4) {
							// Everything is good!

							// progress.className = (xhr.status == 200 ? "success" : "failure");
							// document.location.reload(true);
						}
					};

					// Start upload
					xhr.open('POST', document.getElementById('file-upload-form').action, true);
					xhr.setRequestHeader('X-File-Name', file.name);
					xhr.setRequestHeader('X-File-Size', file.size);
					xhr.setRequestHeader('Content-Type', 'multipart/form-data');
					xhr.send(file);
				} else {
					output('Please upload a smaller file (< ' + fileSizeLimit + ' MB).');
				}
			}
		}

		// Check for the various File API support.
		if (window.File && window.FileList && window.FileReader) {
			Init();
		} else {
			document.getElementById('file-drag').style.display = 'none';
		}
	}
	Upload();
	
	function takePhotoFunction() {
		
		document.getElementById("videoElement").style.visibility = "visible";
		document.getElementById('divScreenShot').style.visibility = "visible";
		
		const screenshotButton = document.getElementById('divSavePhoto');
		const img = document.getElementById('screenShootImageInCanvas');
		
		const video = document.getElementById('videoElement');
		const canvas = document.getElementById('canvasScreenShoot');
		
		canvas.width = 750;
		canvas.height = 562;
		canvas.style.transform = "scaleX(-1)";
		canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
		
		img.src = canvas.toDataURL('image/webp');
	}
	
	function cancelScreenShootImageFunction() {
		document.getElementById('divScreenShot').style.visibility = "hidden";
	}
	
	function savePhotoFunction() {
		//fonction pour sauvegarder l'image dans la base de donnée
	}
	
	function displayFullScreenFunction() {
		var videoEl = document.getElementById("container");
		videoEl.webkitRequestFullScreen();
		var videoBan = document.getElementById("videoBanner");
		/*videoBan.style.left = */
	}
	
	
	

</script>
</body>
</html>
