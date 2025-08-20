let ringtone; 

function startFakeCall() {
    // Make sure the audio object is created only once
    ringtone = new Audio("iphone/ringtone.mp3"); 
    ringtone.loop = true;  // keep ringing until answered/rejected

    ringtone.play().catch((error) => {
        console.log("❌ Ringtone play failed:", error);
    });

    document.getElementById("fakeCallScreen").style.display = "block";
}

function answerCall() {
    if (ringtone) ringtone.pause();
    // start dad's voice
    let dadVoice = new Audio("iphone/dadvoice.mp3");
    dad_voice.play();
}

function rejectCall() {
    if (ringtone) ringtone.pause();
    document.getElementById("fakeCallScreen").style.display = "none";
}




function startFakeCall() {
    let ringtone = document.getElementById("ringtone");
    ringtone.loop = true;

    ringtone.play().catch(err => {
        console.log("Ringtone blocked by browser, user must interact first:", err);
        alert("Tap the screen once to allow sound.");
    });

    document.getElementById("answerBtn").style.display = "inline-block";
    document.getElementById("endBtn").style.display = "none";
}

function answerCall() {
    let ringtone = document.getElementById("ringtone");
    let dadVoice = document.getElementById("dadVoice");

    ringtone.pause();
    ringtone.currentTime = 0;

    dadVoice.play().catch(err => {
        console.log("Dad voice blocked:", err);
        alert("Tap the screen again to allow dad’s voice.");
    });

    document.getElementById("answerBtn").style.display = "none";
    document.getElementById("endBtn").style.display = "inline-block";
}

function endCall() {
    let ringtone = document.getElementById("ringtone");
    let dadVoice = document.getElementById("dadVoice");

    ringtone.pause();
    ringtone.currentTime = 0;

    dadVoice.pause();
    dadVoice.currentTime = 0;

    document.getElementById("answerBtn").style.display = "none";
    document.getElementById("endBtn").style.display = "none";
}








function sendSOSEvidence() {
    // Ask for mic access
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            let mediaRecorder = new MediaRecorder(stream);
            let chunks = [];

            mediaRecorder.ondataavailable = e => chunks.push(e.data);

            mediaRecorder.onstop = () => {
                // Create recorded file
                let blob = new Blob(chunks, { type: "audio/webm" });
                let formData = new FormData();
                formData.append("file", blob, "evidence.webm");

                // Send SOS + audio evidence to backend
                fetch("/sos_evidence", { method: "POST", body: formData })
                    .then(r => r.text())
                    .then(msg => alert(msg));
            };

            mediaRecorder.start();

            // Record only 10s
            setTimeout(() => {
                mediaRecorder.stop();
                stream.getTracks().forEach(track => track.stop());
            }, 10000);
        })
        .catch(err => alert("⚠️ Mic access denied: " + err));
}











document.getElementById("sosEvidenceBtn").addEventListener("click", function () {
    let status = document.getElementById("status");

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            let mediaRecorder = new MediaRecorder(stream);
            let chunks = [];

            status.textContent = "🎤 Recording evidence...";

            mediaRecorder.ondataavailable = e => chunks.push(e.data);

            mediaRecorder.onstop = () => {
                let blob = new Blob(chunks, { type: "audio/webm" });
                let formData = new FormData();
                formData.append("file", blob, "evidence.webm");

                status.textContent = "📤 Sending evidence...";

                fetch("/sos_evidence", { method: "POST", body: formData })
                    .then(r => r.text())
                    .then(msg => status.textContent = msg)
                    .catch(err => status.textContent = "❌ Error: " + err);
            };

            mediaRecorder.start();

            // Stop after 5 sec
            setTimeout(() => {
                mediaRecorder.stop();
                stream.getTracks().forEach(track => track.stop());
            }, 5000);
        })
        .catch(err => {
            status.textContent = "⚠️ Mic access denied: " + err;
        });
});