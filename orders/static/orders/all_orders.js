$(document).ready(() => {
    const template = Handlebars.compile($('#confirmedLayout').html());
    const ajaxUrl = $('#ajaxUrl').data('ajax');

    $('.confirm-order').on('click', event => {
        var button = $(event.target);
        var order = button.data('order');

        $.ajax({
            url: ajaxUrl,
            data: {'order': order},
            dataType: 'json'
        }).done(data => {
            if (data.success) {
                button.closest('.row').remove();
                $('#allConfirmed').append(template({
                    'order': data.order,
                    'status': data.status
                }));
            }
        })
    })
})
