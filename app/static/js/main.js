let startY = 0;

document.addEventListener("touchstart", e => {
    startY = e.touches[0].clientY;
});

document.addEventListener("touchend", e => {
    if (e.changedTouches[0].clientY - startY > 150) {
        location.reload();
    }
});

if (typeof io !== "undefined") {
    const socket = io();

    window.sendMessage = function () {
        const input = document.getElementById("msg");
        if (!input || !input.value.trim()) return;
        socket.emit("send_message", { text: input.value.trim() });
        input.value = "";
    };

    socket.on("receive_message", (data) => {
        const box = document.getElementById("chat-box");
        if (box) {
            box.innerHTML += `<p>${data.text}</p>`;
        }
    });

    socket.on("new_notification", data => {
        alert("🔔 " + data.text);
    });
}
