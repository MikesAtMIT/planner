$(document).ready(function(){
  
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
  })

});