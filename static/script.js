document.getElementById('predict-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    
    if (userInput.trim() === "") {
        alert("Please enter some text for analysis.");
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'text': userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<strong>Classification:</strong> ${data.classification}<br><strong>Reason:</strong> ${data.reason}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});