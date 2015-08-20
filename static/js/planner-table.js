$(document).ready(function(){

  // scroll to today on page load
  function jump_to_row(row){
    var nav_height = $('.navbar').height();
    var thead_height = $('thead').height();
    var target = row.offset().top;
    $('body').scrollTop(target - nav_height - thead_height);
  }
  jump_to_row($('.today'));

  $('table').on('click', '.task-toggle', function(){
    var $panel = $(this).parents('.task-panel');
    var task_id = $panel.attr('data-id');
    var csrftoken = $.cookie('csrftoken');
    var action = $(this).attr('data-action');

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
    var task_id = $panel.attr('data-id');
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
    var task_id = $panel.attr('data-id');
    var date = $panel.parent().attr('data-date');
    var experiment = $panel.parent().attr('data-experiment-id');
    var name = $panel.find('.task-name').text();
    var notes = $panel.find('.task-name').attr('data-content');

    $('#task-id').val(task_id);
    $('#task-experiment').val(experiment);
    $('#task-date').val(date);
    $('#task-name').val(name);
    $('#task-notes').val(notes);
    $('#task-modal .modal-title').html('Edit Task');
    $('#task-modal').modal('show');
  });

  $('table').on('click', '.new-task', function(){
    var date = $(this).parent().attr('data-date');
    var experiment = $(this).parent().attr('data-experiment-id');

    $('#task-id').val('');
    $('#task-experiment').val(experiment);
    $('#task-date').val(date);
    $('#task-name').val('');
    $('#task-notes').val('');
    $('#task-modal .modal-title').html('New Task');
    $('#task-modal').modal('show');
    $('#task-name').focus();
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
        $('#task-modal').modal('hide');
      }
    } else {
      var url = '/update-task/';
      var success = function(data){
        var $panel = $('.panel[data-id="' + data.id + '"]');
        // upate panel status? not necessary right not bc status isn't edited via modal
        $panel.find('.task-name').attr('data-content', data.notes).popover();
        $panel.find('.task-name').html(data.name);
        var old_date = $panel.parent().attr('data-date');
        var old_experiment = $panel.parent().attr('data-experiment-id');
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

  $('table').on('click', '.experiment-edit', function(){
    var $th = $(this).parents('th');
    var experiment_id = $th.attr('data-experiment-id');
    var project_id = $th.find('.experiment-project').attr('data-id');
    var name = $th.find('.experiment-name').text();
    var objective = $th.find('.experiment-objective').text();
    var notes = $th.find('.experiment-notes').text();

    $('#experiment-id').val(experiment_id);
    $('#experiment-project').val(project_id);
    $('#experiment-name').val(name);
    $('#experiment-objective').val(objective)
    $('#experiment-notes').val(notes);
    $('#experiment-modal .modal-title').html('Edit Experiment');
    $('#experiment-modal').modal('show');
  });

  $('#new-experiment').click(function(){
    $('#experiment-id').val('');
    $('#experiment-project').val('');
    $('#experiment-name').val('');
    $('#experiment-objective').val('');
    $('#experiment-notes').val('');
    $('#experiment-modal .modal-title').html('New Experiment');
    $('#experiment-modal').modal('show');
  })

  $('#save-experiment').click(function(){
    var $form = $('#experiment-form');
    var data = $form.serialize();
    
    if ($('#experiment-id').val() == '') {
      var url = '/save-new-experiment/';
      var success = function(data){
        // make header
        $new_header = $('#header-template').clone().removeAttr('id');
        $new_header.removeClass().addClass('column warning');   // again, weird jquery hack for matching classes
        $new_header.attr('data-experiment-id', data.id);
        $new_header.attr('data-order', data.order);
        $new_header.find('.experiment-project').attr('data-id', data.project_id).html(data.project);
        $new_header.find('.experiment-name').html(data.name);
        $new_header.find('.experiment-objective').html(data.objective);
        $new_header.find('.experiment-notes').html(data.notes);
        $('thead th.date').after($new_header);

        // make td to insert in each row
        $sp = $('<span>')
          .addClass('glyphicon glyphicon-plus')
          .attr('aria-hidden','true');
        $btn = $('<button>')
          .attr('type','button')
          .addClass('btn btn-default btn-sm btn-block new-task')
          .append($sp);
        $td = $('<td>')
          .addClass('column')
          .attr('data-experiment-id', data.id)
          .append($btn);
        $('tbody th.date').each(function(){
          var date = $(this).attr('data-date');
          var $new_td = $td.clone().attr('data-date', date);
          $(this).after($new_td);
        });

        // update dropdown in new task modal
        $opt = $('<option>')
          .val(data.id)
          .html(data.project + ' - ' + data.name);
        $('#task-experiment').append($opt);

        $('#experiment-modal').modal('hide');
      }
    } else {
      var url = '/update-experiment/';
      var success = function(data){
        var $header = $('th.column[data-experiment-id="' + data.id + '"]');
        $header.children('.experiment-project').attr('data-id', data.project_id).html(data.project_name);
        $header.children('.experiment-name').html(data.name);
        $header.children('.experiment-objective').html(data.objective);
        $header.children('.experiment-notes').html(data.notes);
        // update status - not necessary now bc status is not edited via modal
        // update ordering?
        $('#experiment-modal').modal('hide');
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
  
  $('table').on('click', '.experiment-toggle', function(){
    var $header = $(this).parents('th.column');
    var experiment_id = $header.attr('data-experiment-id');
    var csrftoken = $.cookie('csrftoken');
    var action = $(this).attr('data-action');

    data = {
      csrfmiddlewaretoken: csrftoken,
      experiment_id: experiment_id,
      action: action,
    }
    $.ajax({
      type: 'POST',
      url: '/toggle-experiment/',
      data: data,
      dataType: 'json',
      success: function(data){
        $header.removeClass('success warning danger');
        switch (data.status) {
          case 'O':
            $header.addClass('warning');
            break;
          case 'C':
            $header.addClass('success');
            break;
          case 'A':
            $header.addClass('danger');
            break;
        }
      },
    });
  });

  $('table').on('click', '.experiment-delete', function(){
    var $header = $(this).parents('th.column');
    var experiment_id = $header.attr('data-experiment-id');
    var csrftoken = $.cookie('csrftoken');

    data = {
      csrfmiddlewaretoken: csrftoken,
      experiment_id: experiment_id,
    }
    $.ajax({
      type: 'POST',
      url: '/delete-experiment/',
      data: data,
      dataType: 'json',
      success: function(data){
        if (data.status == 'D'){
          $('th[data-experiment-id="' + data.experiment_id + '"], td[data-experiment-id="' + data.experiment_id + '"]').remove();
        }
      },
    });
  });

  $('table').on('click', '.update-order', function(){
    var $header = $(this).parents('th.column');
    var experiment_id = $header.attr('data-experiment-id');
    var csrftoken = $.cookie('csrftoken');

    data = {
      csrfmiddlewaretoken: csrftoken,
      experiment_id: experiment_id,
    }
    
    var up = $(this).attr('data-direction') == 'up';
    if (up) {
      $adjacent = $header.prev();
    } else {
      $adjacent = $header.next();
    }

    if ($adjacent.hasClass($header.attr('class'))){   // this is a total hack of how jquery handles hasClass
      data.new_order = $adjacent.attr('data-order');
    } else {
      return;
    }
    
    $.ajax({
      type: 'POST',
      url: '/update-experiment-order/',
      data: data,
      dataType: 'json',
      success: function(data){
        // returns list of experiments with IDs and their updated order values

        // first, update the data-order values of all affected experiments
        for (var i in data) {
          var experiment_id = data[i].experiment_id;
          var order = data[i].order;
          $('th.column[data-experiment-id="' + experiment_id + '"]').attr('data-order', order);
        }

        // then, swap the two relevant columns
        if (up) {
          $('.column[data-experiment-id="' + experiment_id + '"]').each(function(){
            $(this).insertBefore($(this).prev());
          });
        } else {
          $('.column[data-experiment-id="' + experiment_id + '"]').each(function(){
            $(this).insertAfter($(this).next());
          });
        }
      },
    });

  });

});
