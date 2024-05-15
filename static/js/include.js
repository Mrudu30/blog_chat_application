$(document).ready(function () {
    $("#blog_form").submit(function(e){
        e.preventDefault();
        if (validate_content() & validate_title() & validate_files()){
            var formData = new FormData(this)
            $.ajax({
                type: "post",
                url: "http://192.168.1.184:8001/blogs/create-save",
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log(response)
                    $("#blog_form")[0].reset()
                    if (response.status=='success'){
                        window.location.href = 'http://192.168.1.184:8001/blogs/'
                    }
                }
            });
        }
    })
});

function validate_title(){
    var title = $('#title').val()
    var title_help = $('#title_help')
    if (title==""){
        title_help.text('Please add a Title.').addClass('text-danger')
        return false
    }else{
        title_help.text('').removeClass('text-danger')
        return true
    }
}

function validate_content(){
    var content = $('#content').val()
    var content_help = $('#content_help')
    if (content==""){
        content_help.text('Please add Content.').addClass('text-danger')
        return false
    }else{
        content_help.text('').removeClass('text-danger')
        return true
    }
}

function validate_files(){
    var files = $('#images').get(0).files;
    var images_help = $('#images_help');
    if (files.length === 0){
        images_help.text('Please add at least one image.').addClass('text-danger');
        return false;
    } else {
        images_help.text('').removeClass('text-danger');
        return true;
    }
}