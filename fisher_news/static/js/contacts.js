$(document).ready(function() {
    $('#contact-form').on('submit', function(event) {
        event.preventDefault();

        var form = $(this);
        var formData = form.serialize();

        // Получаем значения полей телефона, email и username
        var phone = $('#phone').val();
        var email = $('#email').val();
        var username = $('#username').val();

        // Проверяем, что хотя бы одно из полей заполнено
        if (!phone && !email && !username) {
            // Выводим сообщение об ошибке и прерываем отправку формы
            alert('Хотя бы одно из полей (телефон, email, telegram) должно быть заполнено.');
            return;
        }

        // Продолжаем отправку формы
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
            url: '/send_message_to_bot/',
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
