const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


$(document).ready(function() {
  $('a:not(.dropdown-toggle), button').on('click', function() {
    // Show the spinner when a button or link (except dropdown toggle link) is clicked
    $('#spinner').fadeIn();
  });
  
  $(window).on('load', function() {
    // Hide the spinner once the page is fully loaded
    $('#spinner').fadeOut();
  });
});