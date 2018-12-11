$(document).ready(function() {
  var table = $('#browse-table')
  table.DataTable();
  var feedback = $('#loading-message');
  feedback.removeClass("alert-warning");
  feedback.addClass("alert-success");
  feedback.html("Thank you for Waiting <button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>");
  table.fadeIn(400);
});
