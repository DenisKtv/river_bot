$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();

        // Отправка данных формы с использованием AJAX
        $.ajax({
            url: '/send_message_to_bot/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // Вывод успешного сообщения
                    alert(response.message);
                    location.reload();
                } else {
                    // Вывод сообщения об ошибке
                    alert(response.message);
                }
            },
            error: function() {
                // Вывод сообщения об ошибке AJAX-запроса
                alert('Ошибка при отправке сообщения.');
            }
        });
    });
});