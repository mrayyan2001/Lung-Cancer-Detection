
    document.getElementById('submitButton').onclick = function() {
        event.preventDefault(); // منع التصرف الافتراضي للزر
        console.log("hi");
        const input = document.getElementById('customFile');
        const resultContainer = document.getElementById('result-container');
        if (input.files && input.files[0]) {
            const image = document.createElement('img');
            image.src = URL.createObjectURL(input.files[0]);
            resultContainer.innerHTML = ''; // مسح أي محتوى موجود
            resultContainer.appendChild(image);
        }

    };