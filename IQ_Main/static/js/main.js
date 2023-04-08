const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function() {
  $('#message').fadeOut('slow');
}, 3000);

$(document).ready(function() {
  $('a:not(.dropdown-toggle):not(.noOverlay), button:not(.noOverlay)').on('click', function() {
    // Show the spinner when a button or link (except dropdown toggle link, or elements with noOverlay class) is clicked
    $('#spinner').fadeIn();
  });

  $(window).on('load', function() {
    // Hide the spinner once the page is fully loaded
    $('#spinner').fadeOut();
  });
});