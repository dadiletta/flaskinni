// fade out the load screen
$(window).on('load', function(){
  $('#cover').fadeOut(1000);
});

// STUFF TO HAPPEN AFTER LOAD
$(document).ready(function() {

  // Anything marked full-height gets set the size of the window
  $('.full-height').css('height', $(window).height());
  
  // Min height for a content wrapper
  $('.content-wrapper').css('min-height', ($(window).height()-200));

  // Sweet Alert triggered on anything labeled delete
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
  $('#sidebarToggle').on('click', function(e) {
    $.ajax({
      data : {
          something : "hello, I don't have any data to give you"
      },
      type : 'POST',
      url : '/togglesidebar' // Notice I can't use a url_for
    })
    .done(function(data) {
        if (data.error) {
          // error?            
        }else {
          // cool, it worked
        }
        
    });
  });

  // TRIGGER LOAD SCREEN
  $('.loadScreen').click(function(){
    $('#cover').css('height', $(window).height());
    $('.navbar').hide();
    $('.navbar-top').css('padding-top', 0);
    $('#cover').fadeIn(1000);
  });

});

