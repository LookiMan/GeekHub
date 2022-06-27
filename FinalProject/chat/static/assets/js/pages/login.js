
$(document).ready(function () {
    $('body').on('keydown', function (event) {
        const keyId = event.keyCode || event.which || event.key || 0;

        if (keyId === 13) {
            $('#login-form').submit();
        }
    });
});
