const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function() {
    $('#message').fadeOut('slow');
  }, 3000);

let hoverSize = [100, 400];

$(function() {
  var hoverSize = [1000, 400];
  $('.zoomable-image').on('click',function() {
      $(this).toggleClass('zoomed');
      if ($(this).hasClass('zoomed')) {
          $(this).css({
              height: hoverSize[0],
              width: hoverSize[1]
          });
      } else {
          $(this).css({
              height: "",
              width: ""
          });
      }
  });
});