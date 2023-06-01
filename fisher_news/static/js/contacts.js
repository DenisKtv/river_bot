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
            },
            error: function(error) {
                // Обработка ошибки
                console.error(error);
            }
        });
    });
});