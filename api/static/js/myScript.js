
$(document).ready(function() {
    // Handle quantity increase
    $('.plus-cart').on('click', function() {
        var cart_id = $(this).attr('pid');
        $.ajax({
            url: '/pluscart?cart_id=' + cart_id,
            method: 'GET',
            success: function(response) {
                $('#quantity' + cart_id).text(response.quantity);
                $('#amount').text(response.amount);
                $('#totalamount').text(response.total);
            }
        });
    });

    // Handle quantity decrease
    $('.minus-cart').on('click', function() {
        var cart_id = $(this).attr('pid');
        $.ajax({
            url: '/minuscart?cart_id=' + cart_id,
            method: 'GET',
            success: function(response) {
                $('#quantity' + cart_id).text(response.quantity);
                $('#amount').text(response.amount);
                $('#totalamount').text(response.total);
            }
        });
    });
});


$('.remove-cart').click(function(){
    
    var id = $(this).attr('pid').toString()

    var to_remove = this.parentNode.parentNode.parentNode.parentNode

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: {
            cart_id: id
        },

        success: function(data){
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
            to_remove.remove()
        }
    })


})
