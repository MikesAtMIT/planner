$(document).ready(function(){

  filterProjects();
  
  $('#start-date,#end-date').datepicker({
    format: "D, M d, yyyy",
    todayBtn: true,
    autoclose: true,
    todayHighlight: true,
  });

  $('#filter-dates').click(function(){
    var start = $('#start-date').datepicker('getDate');
    var end = $('#end-date').datepicker('getDate');
    if (start == null || end == null) {
      return;
    }

    // super hacky hard-coded way follows. think of a better way
    var url = window.location.href;
    url += moment(start).format('YYYYMMDD');
    url += '-';
    url += moment(end).format('YYYYMMDD');
    window.location.href = url;
  });

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
  
});