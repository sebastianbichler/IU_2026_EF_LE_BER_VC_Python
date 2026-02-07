window.onload = function () {
    const dateElements = document.querySelectorAll('.datetime');
    dateElements.forEach(function (element) {
        const datetime = element.getAttribute('data-datetime');
        const date = new Date(datetime);

        const format = element.getAttribute('data-format');

        let options = {
            year: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        };

        if (format === 'long') {
            options.month = 'long';
        } else if (format === 'short') {
            options.month = 'short';
        } else if(format === 'date-only') {
            options = {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
            };
        } else {
            options.month = '2-digit';
        }

        element.textContent = date.toLocaleDateString('de', options);
    });

    const clickableElements = document.querySelectorAll('[data-clickable]');
    clickableElements.forEach(function (element) {
        element.style.cursor = 'pointer';
        element.addEventListener('click', function () {
            const url = element.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
}