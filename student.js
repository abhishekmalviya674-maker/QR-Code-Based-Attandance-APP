const backendUrl = "http://127.0.0.1:5000";

const html5QrCode = new Html5Qrcode("reader");

function onScanSuccess(decodedText) {
  const userId = document.getElementById("userId").value.trim();
  if (!userId) {
    alert("Please enter your ID first!");
    return;
  }

  const data = JSON.parse(decodedText);
  fetch(`${backendUrl}/markAttendance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, sessionId: data.sessionId })
  })
    .then(() => alert("✅ Attendance Marked!"))
    .catch(() => alert("❌ Error marking attendance"));
}

html5QrCode.start(
  { facingMode: "environment" },
  { fps: 10, qrbox: 250 },
  onScanSuccess
);
