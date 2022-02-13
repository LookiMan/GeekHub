

function changeAmountProductsInBadge(amount) {
    $('span#quantityOfProductsBadge').text(amount);
}


function changeButtonStyle(button) {
    $(button).toggleClass('btn-primary');
    $(button).toggleClass('btn-danger');
}


function add_product_to_cart(event) {
    event.preventDefault();
    let href = event.target.href;

    $.ajax({
        url: href,
        method: 'post',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (data) { 
            changeAmountProductsInBadge(data.amount_products);
            changeButtonStyle(event.target)
            $(event.target).off('click');
            $(event.target).on('click', remove_product_from_cart);
            $(event.target).text('С корзины');
            $(event.target).attr('href', href.replace('/add_to_cart/', '/remove_from_cart/'));
        },
        error: function(data) {
            console.error(data);
        }
    });
}


function remove_product_from_cart(event) {
    event.preventDefault();
    let href = event.target.href;

    $.ajax({
        url: href,
        method: 'post',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (data) { 
            changeAmountProductsInBadge(data.amount_products);
            changeButtonStyle(event.target)
            $(event.target).off('click');
            $(event.target).on('click', add_product_to_cart);
            $(event.target).text('В корзину');
            $(event.target).attr('href', href.replace('/remove_from_cart/', '/add_to_cart/'));
        },
        error: function(data) {
            console.error(data);
        }
    });
}


$(document).ready(function () { 
    $('div.card-body a.btn-primary').each(function () {
        $(this).on('click', add_product_to_cart);
    });

    $('div.card-body a.btn-danger').each(function () {
        $(this).on('click', remove_product_from_cart);
    });

});