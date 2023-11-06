$(document).ready(function () {
       // Open the drawer when the button is clicked
    $('button#drawer-btn').click(function(event) {
        event.stopPropagation(); // Prevent the click event from reaching the body
        $('.drawer').toggleClass('open');
    });

    // Close the drawer when body is clicked
    $(document).click(function(event) {
        if (!$(event.target).closest('.drawer').length && !$(event.target).is(
            'button#drawer-btn')) {
            $('.drawer').removeClass('open');
        }

        if (!$(event.target).closest('tr#table-body').length && !$(event.target).is(
            'tr#table-body')) {
            $('.preview-box').removeClass('show-preview')
            $('#default').addClass('default-show')
            $('#default').html('<div><br><br><br><br>Tap on any Item<br>for more details</div>')

        }
    });

    // Prevent clicks inside the drawer from closing it
    $('.drawer').click(function(event) {
        event.stopPropagation();
    });

 
    // Handles how the retrieval and display of a vendor information on the preview section
    $('tr#table-body').click(function(event) {
        $('#default').empty();
        $('#default').removeClass();
        $('.preview-box').addClass('show-preview')
        const vendorId = $(this).find('#td-vendor-id').text()
        console.log(vendorId)

        $.ajax({
            url: '/user/vendors/' + vendorId,
            type: 'GET',
            success: function (response) {
                console.log(response)
                $('.preview-box').html(`<div class="head-row"></div>
                <div class="page-name" id="vend-prev">Vendor Preview</div>
                <div class="info-box" id="vend-name">Name:<span style="font-weight: 350;"> ${response.name}</span></div>
                <div class="info-box"  id="vend-created">Date Created: ${response.created_at} </div>
                <div class="info-box"  id="vend-email">Email: ${response.email} </div>
                <div class="info-box"  id="vend-mobile">Mobile Number: ${response.phone_number} </div>
                <div class="info-box"  id="vend-addr">Address: ${response.address} </div>
                <div class="info-box"  id="vend-last-order">Last Order: ${response.last_order} </div>
                <div class="info-box"  id="vend-tot-or">Total Orders: ${response.total_orders}  </div>
                <div class="info-box"  id="vend-open-or">Open Orders: ${response.open_orders}</div>
                <div class="info-box"  id="vend-close-or">Closed Orders: ${response.closed_orders}</div>
                <div class="info-box"  id="avr-rev">Average Review: ${response.avr_review}</div>
                </div>`)
                
            },
            error: function(error) {
                console.log(error + '- Wahala dey')
            }
        });

    });


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
                    console.log(response)
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

    // Handles the transition of vendor information from table form to cards
    $('#change-view-btn').click(function () {
        $('.card-display-section').toggle();
        $('.table-view').toggleClass('show')
    });


    // Handles filter operations
    $('.filters').change(function () {
        const filterWord = $(this).val()

        // $.ajax({
        //     url: '/user/orders/filter_by/' + filterWord,
        //     type: 'GET',
        //     success: function() {
        //         console.log('worked!')
        //     }
        // })
    })


    // handle create funtion
    // $('#new_vendor').click(function () {
    //     $.ajax({
    //         url: "/user/vendors/new",
    //         type: "GET",
    //         success: function(response) {
    //             console.log(response)
    //             $(".selected-view-container").html(response);
    //         },
    //         error: function(error) {
    //             console.log(error);
    //         }
    //     });
    // });
});
