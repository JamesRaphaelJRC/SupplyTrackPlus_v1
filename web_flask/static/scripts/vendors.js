$(document).ready(function () {
       // Open the drawer when the button is clicked i.e for the preview section of vendors.html
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
                <div class="info-box" id="vend-name"><strong>Name: &nbsp;&nbsp;</strong> ${response.name}</div>
                <div class="info-box"  id="vend-created"><strong>Date Created: &nbsp;&nbsp;</strong>${response.created_at} </div>
                <div class="info-box"  id="vend-email"><strong>Email: &nbsp;&nbsp;</strong> ${response.email} </div>
                <div class="info-box"  id="vend-mobile"><strong>Mobile Number: &nbsp;&nbsp;</strong> ${response.phone_number} </div>
                <div class="info-box"  id="vend-addr"><strong>Address: &nbsp;&nbsp;</strong> ${response.address} </div>
                <div class="info-box"  id="vend-last-order"><strong>Last Order: &nbsp;&nbsp;</strong> ${response.last_order} </div>
                <div class="info-box"  id="vend-tot-or"><strong>Total Orders: &nbsp;&nbsp;</strong> ${response.total_orders}  </div>
                <div class="info-box"  id="vend-open-or"><strong>Open Orders: &nbsp;&nbsp;</strong> ${response.open_orders}</div>
                <div class="info-box"  id="vend-close-or"><strong>Closed Orders: &nbsp;&nbsp;</strong> ${response.closed_orders}</div>
                <div class="info-box"  id="avr-rev"><strong>Average Review: &nbsp;&nbsp;</strong>${response.avr_review}</div>
                </div>`)
                
            },
            error: function(error) {
                console.log(error + '- Wahala dey')
            }
        });

    });




    // Handles the transition of vendor information from table form to cards
    $('#change-view-btn').click(function () {
        $('.card-display-section').toggle();
        $('.table-view').toggleClass('show')
    });

});
