$(document).ready(function () {
    $('#title').keyup(validate_title)
    $('#description').keyup(validate_description)
    $('#due_date').keyup(validate_due_date)
    $('#title').blur(validate_title)
    $('#description').blur(validate_description)
    $('#due_date').blur(validate_due_date)

    $('#task_form_id').submit(function(e){
        e.preventDefault()
        console.log(validate_description() , validate_due_date() , validate_title())
        if (validate_description() & validate_due_date() & validate_title()){
            var form_data = new FormData(this)
            if($('#form-type').val()=='add_task'){
                $.ajax({
                    type: "post",
                    url: "http://192.168.1.184:8001/tasks/create-task/",
                    data: form_data,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        if (response.status){
                            $('#message').show();
                            $('#message').addClass('alert alert-success').text('Task added successfully')
                        }else{
                            $('#message').show();
                            $('#message').addClass('alert alert-danger').text('Task not added')
                        }
                        setTimeout(() => {
                            $('#message').removeClass('alert alert-danger alert-success').text('')
                            $('#message').hide()
                        }, 3000);
                        taskload()
                    }
                });
            }else{
                var task_id = $("#task_id").val()
                console.log("url", "update-task/"+task_id,)
                $.ajax({
                    type: "post",
                    url: "update-task/"+task_id,
                    data: form_data,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        if (response.status){
                            $('#message').show();
                            $('#message').addClass('alert alert-success').text('Task updated successfully')
                        }else{
                            $('#message').show();
                            $('#message').addClass('alert alert-danger').text('Task not updated')
                        }
                        setTimeout(() => {
                            $('#message').removeClass('alert alert-danger alert-success').text('')
                            $('#message').hide()
                        }, 3000);
                        taskload()
                    }
                });
            }
            $('#task_form').dialog('close')
        }
    })
});

function hexToRgba(hex, opacity) {
    // Remove '#' if present
    hex = hex.replace('#', '');
    // Convert hex to RGB
    var r = parseInt(hex.substring(0, 2), 16);
    var g = parseInt(hex.substring(2, 4), 16);
    var b = parseInt(hex.substring(4, 6), 16);
    // Return RGBA string
    return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + opacity + ')';
}

function validate_title(){
    var title = $('#title')
    var title_help = $('#title_help')
    if (title.val()==''){
        title_help.text('This is a required field.')
        return false
    }
    else{
        title_help.text('')
        return true
    }
}

function validate_description(){
    var description = $('#description')
    var description_help = $('#description_help')
    if (description.val()==''){
        description_help.text('This is a required field.')
        return false
    }
    else{
        description_help.text('')
        return true
    }
}

function validate_due_date(){
    var due_date = $('#due_date')
    var due_date_help = $('#due_date_help')
    if (due_date.val()==''){
        due_date_help.text('This is a required field.')
        return false
    }
    else{
        due_date_help.text('')
        return true
    }
}

function taskload(){
    var taskstable = $('#taskstable tbody');
    taskstable.empty();
    $.ajax({
        type: "get",
        url: "get-all-tasks/",
        data:'',
        success: function (response) {
            console.log(response)
            var str = ""
            if (response.length==0){
                str +='<tr><td colspan="4" style="text-align:center;">No Records Found</td></tr>'
            }else{
                $.each(response, function(index, task) {
                    var rgbaColor = hexToRgba(task.color, 0.5);
                    str += '<tr style="background-color: ' + rgbaColor + '">';
                    str += '<td>' + (index+1) + '</td>';
                    str += '<td>' + task.title + '</td>';
                    // str += '<td>' + task.description + '</td>';
                    str += '<td>' + task.due_date + '</td>';
                    str += '<td>' + '<span onclick="update_task('+task.id+')" class="btn btn-warning"><i class="fa fa-pencil" aria-hidden="true"></i></span>  <span class="btn btn-danger" onclick="delete_task('+task.id+')"><i class="fa fa-trash" aria-hidden="true"></i></span>'
                    str += '</tr>';
                });
            }
            taskstable.append(str)
            $('#taskstable').dataTable()
        }
    });
}

function add_task(){
    $('#task_form').dialog({
        autoOpen: false,
        width: 400,
        modal: true,
        title:'Add Task',
        buttons:{
            Cancel: function(){
                $(this).dialog("close")
            }
        },
        close:function(){
            $('#task_form_id')[0].reset();
            $('.help').text('')
        }
    })
    $('.ui-dialog-titlebar-close').hide();
    $('#task_form').dialog('open')
    $('#form-type').val('add_task')
}

function delete_task(id){
    var result = confirm('Are you sure you want to delete task?')
    if (result){
        $.ajax({
            type: "get",
            url: "http://192.168.1.184:8001/tasks/delete-task/"+id,
            success: function (response) {
                if (response.status){
                    $('#message').show();
                    $('#message').addClass('alert alert-success').text('Task deleted successfully')
                }else{
                    $('#message').show();
                    $('#message').addClass('alert alert-danger').text('Task not deleted')
                }
                setTimeout(() => {
                    $('#message').removeClass('alert alert-danger alert-success').text('')
                    $('#message').hide()
                }, 3000);
                taskload()
            }
        });
    }
}

function update_task(id){
    $('#task_form').dialog({
        autoOpen: false,
        width: 400,
        modal: true,
        title:'Update Task',
        buttons:{
            Cancel: function(){
                $(this).dialog("close")
            }
        },
        close:function(){
            $('#task_form_id')[0].reset();
            $('.help').text('')
        }
    })
    $('.ui-dialog-titlebar-close').hide();
    $('#task_form').dialog('open')
    $('#form-type').val('update_task')
    $.ajax({
        type: "get",
        url: "get-task/"+id,
        success: function (response) {
            if(response.taskInfo){
                // console.log(response)
                var parse_taskInfo = JSON.parse(response.taskInfo);
                console.log(parse_taskInfo)
                var taskInfo = parse_taskInfo[0].fields;
                console.log(taskInfo);
                console.log(parse_taskInfo[0].pk)
                // $('#color').colorpicker();s
                $('#task_id').val(parse_taskInfo[0].pk)
                $('#title').val(taskInfo.title);
                $('#description').val(taskInfo.description);
                $('#color').val(taskInfo.color);
                $('#due_date').val(taskInfo.due_date);
            }
        }
    });
}