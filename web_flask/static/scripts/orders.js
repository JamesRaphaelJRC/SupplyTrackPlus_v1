$(document).ready(function () {
    $('DIV.grouped-header').click(function () {
        $(this).closest('li').find(".grouped-orders").slideToggle()
    });
});