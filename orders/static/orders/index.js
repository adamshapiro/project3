$(document).ready(() => {
    // get the url to the route for adding order items
    const ajaxUrl = $('#ajaxUrl').data('ajax');
    const template = Handlebars.compile($('#select').html());

    // for most menu items, simply grab the id and the price to pass along
    $('.add-item').on('click', event => {
        var button = $(event.target);
        var price = button.data('price');
        var id = button.closest('li').data('food');

        addItem(ajaxUrl, {
            'food': id,
            'price': price
        });

        // collapse the list after adding the item to indicate a change
        button.closest('.collapse').collapse('hide');
    });

    // when adding a sub, grab any chosen AddOns to pass along
    $('.add-sub').on('click', event => {
        var button = $(event.target);
        var price = button.data('price');
        var parent = button.closest('li');
        var id = parent.data('food');

        var addOns =  parent.find('.addSubOption:checked').get().map(v => v.value);

        // send add_ons as a string to be parsed server-side
        addItem(ajaxUrl, {
            'food': id,
            'price': price,
            'add_ons': addOns.join(',')
        });

        button.closest('.collapse').collapse('hide');
    });

    $('.add-pizza').on('click', event => {
        var button = $(event.target);
        var price = button.data('price');
        var parent = button.closest('li');
        var id = parent.data('food');
        var toppingsCount = parent.data('toppings');

        // if the chosen pizza has toppings, show a modal to choose them
        if (toppingsCount > 0) {
            var canSubmit = true;

            var modal = $('#toppingModal');
            modal.find('.modal-title').text(`Choose ${toppingsCount} Topping(s):`);

            // get rid of old form inputs and add a new one per topping
            $('#toppingModalForm').empty();
            for (let i = 1; i <= toppingsCount; i++) {
                $('#toppingModalForm').append(template({'i': i}));
            }
            // validate different toppings when a topping is chosen
            var selected = $('.topping-selector');
            selected.on('change', event => {
                var others = selected.not(event.target).get().map(v => v.value);
                if (others.includes(event.target.value)) {
                    canSubmit = false;
                    $('#toppingModalAlert').removeClass('d-none');
                } else {
                    canSubmit = true;
                    $('#toppingModalAlert').addClass('d-none');
                }
            });

            // make sure old onclick is removes and add a submit function to the modal
            $('#toppingModalSubmit').off('click');
            $('#toppingModalSubmit').on('click', event => {
                if (canSubmit) {
                    // validate unique toppings here in case user submits without
                    // changing the select fields
                    var submitting = selected.get().map(v => v.value);
                    if (hasDuplicates(submitting)) {
                        canSubmit = false;
                        $('#toppingModalAlert').removeClass('d-none');
                    } else {
                        // submit the pizza with selected toppings
                        addItem(ajaxUrl, {
                            'food': id,
                            'price': price,
                            'toppings': submitting.join(',')
                        });

                        button.closest('.collapse').collapse('hide');
                        modal.modal('hide');
                    }
                }
            });

            modal.modal('show');
        } else {
            addItem(ajaxUrl, {
                'food': id,
                'price': price
            });

            button.closest('.collapse').collapse('hide');
        }
    })
});

// function to send a menu item to the server to be added to the cart
function addItem (url, item) {
    $.ajax({
        url: url,
        data: item,
        dataType: 'json'
    }).done(data => {
        if (data.success) {
            $('#viewCart').removeClass('disabled');
            $('#itemCount').text(data.items);
        }
    });
}

// function to determine if an array has duplicate values.
function hasDuplicates (arr) {
    var check = {};
    for (var l in arr) {
        if (arr[l] in check)
            return true;
        else
            check[arr[l]] = true;
    }
    return false;
}
