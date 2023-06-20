$(document).ready(function() {
    $('#contact-form').on('submit', function(event) {
        event.preventDefault();

        var form = $(this);
        var formData = form.serialize();

        $.ajax({
            headers: {
                'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()
            },
            type: 'POST',
            url: form.attr('action'),
            data: formData,
            success: function(response) {
                // Обработка успешного ответа
                console.log(response);

                // Отправка данных боту через запрос к серверу
                sendToBot(formData);
            },
            error: function(error) {
                // Обработка ошибки
                console.error(error);
            }
        });
    });

    function sendToBot(formData) {
        // Отправка данных боту через Ajax-запрос
        $.ajax({
            type: 'POST',
            url: '/send_message_to_bot/',  // Замени на URL-адрес, обрабатывающий отправку сообщения боту
            data: formData,
            success: function(response) {
                // Обработка успешного ответа
                console.log(response);
            },
            error: function(error) {
                // Обработка ошибки
                console.error(error);
            }
        });
    }
});