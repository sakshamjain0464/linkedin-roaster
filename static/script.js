document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file');
    const customFileButton = document.querySelector('.custom-file-upload');
    const fileNameDisplay = document.getElementById('fileName');

    // Trigger the file input when clicking on the custom file upload button
    customFileButton.addEventListener('click', function () {
        fileInput.click()
    });

    // Display the file name once a file is selected
    fileInput.addEventListener('change', function () {
        const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file chosen';
        fileNameDisplay.textContent = fileName;
    });

    // Form submission event
    const uploadForm = document.getElementById('uploadForm');
    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();
        document.getElementById('outputBox').style.display = 'none';
        const outputContent = document.getElementById('outputContent')
        outputContent.textContent = "";
        document.getElementById("buttonGroup").style.display = 'none'
        // You can add the form submission logic here (e.g., sending the file to the server)
        console.log("Form submitted with file: ", fileInput.files[0].name);

        // Example of using FormData to submit file (you can modify based on your backend logic)
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Submit the form via AJAX (fetch or XMLHttpRequest)
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log('Roast data:', data);
                // Update output display
                document.getElementById('outputBox').style.display = 'block';
                const outputContent = document.getElementById('outputContent')
                outputContent.textContent = data.output;
                document.getElementById("buttonGroup").style.display = 'flex'
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

const downloadBtn = document.getElementById("downloadBtn")

downloadBtn.addEventListener('click', function () {
    const outputBox = document.getElementById('output')
    outputBox.style.backgroundColor = "#121212"
    html2canvas(outputBox).then(function (canvas) {
        // Convert canvas to PNG and trigger download
        const imageUrl = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = 'roast_output.png';
        link.click();
    }).catch(function (error) {
        console.error('Error capturing canvas:', error);
    });
});
