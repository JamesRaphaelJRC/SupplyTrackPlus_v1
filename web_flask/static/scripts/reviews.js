$(document).ready(function () {
    // Loads orders supplied by a vendor dynamically in the new reviews page
    $('#vendor_id').change(function () {
        var vendorId = $(this).val();
        $.ajax({
            url: '/get_orders/' + vendorId,
            type: 'GET',
            success: function(response){
                // Populate order options based on the response
                $('#order_id').empty();  // Clear existing options
                $.each(response, function(index, order){
                    // console.log(response)
                    let orderId = order[0];
                    let productName = order[1];
                    $('#order_id').append($('<option>', {
                        value: orderId,
                        text: productName
                    }));
                });
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});