async function send() {
    let input = document.getElementById("msg");
    let chat = document.getElementById("chat-box");

    let message = input.value;
    if (!message) return;

    chat.innerHTML += `<div class="msg user">${message}</div>`;
    input.value = "";

    let res = await fetch("http://127.0.0.1:5050/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    let data = await res.json();

    chat.innerHTML += `
        <div class="msg bot">
        🤖 ${data.llm}
        <br><br>
        📚 ${data.wiki}
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;
}
