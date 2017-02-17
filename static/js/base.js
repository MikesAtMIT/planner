$(document).ready(function(){

  filterProjects();
  
  $('#start-date,#end-date').datepicker({
    format: "D, M d, yyyy",
    todayBtn: true,
    autoclose: true,
    todayHighlight: true,
  });
  $('#start-date').datepicker('update',
    new Date(moment($('tbody .date').first().data('date')))
  );
  $('#end-date').datepicker('update',
    new Date(moment($('tbody .date').last().data('date')))
  );

  $('#choose-filters').click(function(){
    $('#filter-modal').modal('show');
  });

  $('.user-checkbox').click(function(){
    filterProjects();
  });

  function filterProjects() {
    var users = {}
    $('.user-checkbox').each(function(i) {
      users[$(this).attr('data-id')] = $(this).is(':checked');
    });
    $('.project-checkbox').each(function(i) {
      var contributor_id_list = $(this).attr('data-contributors').split(',');
      if (contributor_id_list.some(function(contributor) { return users[contributor]; })) {
        $(this).removeClass('hidden');
      } else {
        $(this).addClass('hidden').find('input').attr('checked', false);
      }
    });
  }

  $('#filter-form').submit(function() {
    var startDate = $('#start-date').datepicker('getDate');
    var startDateString = startDate.getFullYear().toString() + '-' +
                          (startDate.getMonth() + 1).toString() + '-' +
                          startDate.getDate().toString();
    $('#start-date-hidden').val(startDateString);

    var endDate = $('#end-date').datepicker('getDate');
    var endDateString = endDate.getFullYear().toString() + '-' +
                          (endDate.getMonth() + 1).toString() + '-' +
                          endDate.getDate().toString();
    $('#end-date-hidden').val(endDateString);
  });

});