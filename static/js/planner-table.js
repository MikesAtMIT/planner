$(document).ready(function(){

  $('table').on('click', '.task-toggle', function(){
    var $panel = $(this).parents('.task-panel');
    var task_id = $panel.data('id');
    var csrftoken = $.cookie('csrftoken');
    var action = $(this).data('action');

    data = {
      csrfmiddlewaretoken: csrftoken,
      task_id: task_id,
      action: action,
    }
    $.ajax({
      type: 'POST',
      url: '/toggle-task/',
      data: data,
      dataType: 'json',
      success: function(data){
        $panel.removeClass('panel-success panel-warning panel-danger');
        switch (data.status) {
          case 'O':
            $panel.addClass('panel-warning');
            break;
          case 'C':
            $panel.addClass('panel-success');
            break;
          case 'A':
            $panel.addClass('panel-danger');
            break;
        }
      },
    });
  });

  $('table').on('click', '.task-delete', function(){
    var $panel = $(this).parents('.task-panel');
    var task_id = $panel.data('id');
    var csrftoken = $.cookie('csrftoken');

    data = {
      csrfmiddlewaretoken: csrftoken,
      task_id: task_id,
    }
    $.ajax({
      type: 'POST',
      url: '/delete-task/',
      data: data,
      dataType: 'json',
      success: function(data){
        if (data.status == 'D'){
          $panel.remove();
        }
      },
    });
  });
  
  $('.task-name').popover();

  $('table').on('click', '.task-edit', function(){
    var $panel = $(this).parents('.task-panel');
    var task_id = $panel.data('id');
    var date = $panel.parent().data('date');
    var experiment = $panel.parent().data('experiment-id');
    var name = $panel.find('.task-name').text();
    var notes = $panel.find('.task-name').data('content');

    $('#task-id').val(task_id);
    $('#task-experiment').val(experiment);
    $('#task-date').val(date);
    $('#task-name').val(name);
    $('#task-notes').val(notes);
    $('#task-modal .modal-title').html('Edit Task');
    $('#task-modal').modal('show');
  });

  $('.new-task').click(function(){
    var date = $(this).parent().data('date');
    var experiment = $(this).parent().data('experiment-id');

    $('#task-id').val('');
    $('#task-experiment').val(experiment);
    $('#task-date').val(date);
    $('#task-name').val('');
    $('#task-notes').val('');
    $('#task-modal .modal-title').html('New Task');
    $('#task-modal').modal('show');
  })

  $('#save-task').click(function(){
    var $form = $('#task-form');
    var data = $form.serialize();
    
    if ($('#task-id').val() == '') {
      var url = '/save-new-task/';
      var success = function(data){
        var $new_panel = $('#panel-template').clone().removeAttr('id');
        $new_panel.addClass('panel-warning');
        $new_panel.attr('data-id', data.id);
        $new_panel.find('.task-name').attr('data-content', data.notes).popover();
        $new_panel.find('.task-name').html(data.name);
        var $target_td = $('td[data-experiment-id="' + data.experiment + '"][data-date="' + data.date + '"]');
        $new_panel.insertBefore($target_td.children('button'));
        console.log($new_panel);
        $('#task-modal').modal('hide');
      }
    } else {
      var url = '/update-task/';
      var success = function(data){
        var $panel = $('.panel[data-id="' + data.id + '"]');
        $panel.find('.task-name').attr('data-content', data.notes).popover();
        $panel.find('.task-name').html(data.name);
        var old_date = $panel.parent().data('date');
        var old_experiment = $panel.parent().data('experiment-id');
        if (old_date != data.date || old_experiment != data.experiment) {
          var $target_td = $('td[data-experiment-id="' + data.experiment + '"][data-date="' + data.date + '"]');
          $panel.insertBefore($target_td.children('button'));
        }
        $('#task-modal').modal('hide');
      }
    }

    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      dataType: 'json',
      success: success,
    });
  });
});