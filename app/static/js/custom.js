
$(document).ready(function() {
  $('.full-height').css('height', $(window).height());
  
  $('.content-wrapper').css('min-height', ($(window).height()-200));


  $('.delete').on('click', function(e) {
    e.preventDefault();
    var currentElement = $(this);

    swal({
      title: "Are you sure?",
      text: "You will destroy this item. Proceed anyway?",
      type: "warning",
      buttons: true,
      dangerMode: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonClass: 'btn btn-danger',
      cancelButtonClass: 'btn btn-light',
      confirmButtonText: "Yes, delete!"
    }).then((willDelete) => {
      if (willDelete) {
        window.location.href = currentElement.attr('href');
      } else {
        console.log("not delete");
      }
    });
  });

  // AJAX EXAMPLE
  $('.unseen-message').click(function(event) {
    // store this so it's more easily accessible in the .done
    var msg = $(this);
    $.ajax({
        data : {
            message_id : $(this).attr('data-message')
        },
        type : 'POST',
        url : '/message/seen_on' // Notice I can't use a url_for
    })
    .done(function(data) {
        if (data.error) {
            // prevent user from repeatidly sending post requests
            // if there's an error, you're done.
            msg.off('click');
            
        }else {
            // show success
            msg.removeClass('unseen-message');
            msg.find('.badge-warning').hide();
            msg.off('click');
        }
        
    });
}); 

});

