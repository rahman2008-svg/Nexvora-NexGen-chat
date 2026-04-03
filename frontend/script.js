const BACKEND_URL = "http://192.168.0.100:5050/chat"; // Termux IP + backend port

async function sendMessage() {
    const input = document.getElementById("userInput").value;
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;
    try {
        const res = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: input})
        });
        const data = await res.json();
        chatBox.innerHTML += `<p><b>AI:</b> ${data.reply}</p>`;
    } catch(err) {
        chatBox.innerHTML += `<p style="color:red;"><b>AI:</b> Error connecting to backend</p>`;
    }
    document.getElementById("userInput").value = "";
}
