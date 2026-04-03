const sendBtn = document.getElementById("send");
const chatDiv = document.getElementById("chat");
const promptInput = document.getElementById("prompt");

sendBtn.onclick = async () => {
  const prompt = promptInput.value.trim();
  if (!prompt) return;
  chatDiv.innerHTML += `<p><b>You:</b> ${prompt}</p>`;

  let apiUrl = prompt.startsWith("wiki:") ? `/wiki?q=${encodeURIComponent(prompt.replace("wiki:", ""))}` : "/ai";
  let options = {};
  if (apiUrl === "/ai") {
    options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    };
  }

  try {
    const res = await fetch(apiUrl, options);
    const data = await res.json();
    chatDiv.innerHTML += `<p><b>${apiUrl === "/ai" ? "LLM" : "Wiki"}:</b> ${data.result || data.error}</p>`;
    chatDiv.scrollTop = chatDiv.scrollHeight;
  } catch (err) {
    chatDiv.innerHTML += `<p><b>Error:</b> ${err}</p>`;
  }
  promptInput.value = "";
};
