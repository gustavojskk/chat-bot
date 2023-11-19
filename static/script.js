document.addEventListener("DOMContentLoaded", function () {
    // Adiciona um manipulador de eventos ao formulário de upload
    document.getElementById("upload-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Impede o envio tradicional do formulário

        var pdfFileInput = document.getElementById("pdf_file");
        var pdfFile = pdfFileInput.files[0];

        if (pdfFile) {
            uploadPDF(pdfFile);
        } else {
            alert("Por favor, selecione um arquivo PDF para enviar.");
        }
    });

    // Adiciona um manipulador de eventos ao botão de envio da pergunta
    document.getElementById("send-question").addEventListener("click", function () {
        var userQuestionInput = document.getElementById("user-input");
        var userQuestion = userQuestionInput.value;

        if (userQuestion) {
            askQuestion(userQuestion);
            userQuestionInput.value = "";
        } else {
            alert("Por favor, digite uma pergunta antes de enviar.");
        }
    });

    function uploadPDF(pdfFile) {
        var formData = new FormData();
        formData.append("pdf_file", pdfFile);

        fetch("/upload_pdf", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro no envio do arquivo: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || data.error);
        })
        .catch(error => {
            console.error("Erro durante o envio do arquivo:", error);
        });
    }

    function askQuestion(userQuestion) {
        fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: "question=" + encodeURIComponent(userQuestion),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro no envio da pergunta: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            appendMessage(userQuestion, "user-message");
            appendMessage(data.answer, "bot-message");
        })
        .catch(error => {
            console.error("Erro durante o envio da pergunta:", error);
        });
    }

    function appendMessage(text, className) {
        var chatBody = document.getElementById("chat-body");
        var messageElement = document.createElement("p");
        messageElement.className = className;
        messageElement.textContent = text;
        chatBody.appendChild(messageElement);

        chatBody.scrollTop = chatBody.scrollHeight;
    }
});