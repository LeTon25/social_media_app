$(document).ready(function() {
    
})

function renderListYourGroup() {
    $.ajax({
        url: '/add-group/',
        method: 'POST',
        dataType: 'JSON',
        data: formData,
        success: function(res) {
        
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function addGroup() {
    $(document).on("click", "#btn-add-group", () => {
    
        let gr_name = $('.form-create-group #gr-name').val()
        let gr_category = $('.form-create-group #select-category').val()
        let gr_description = $('.form-create-group #txt-description').val()
        let gr_friend = $('.form-create-group #select-friends').val()
        let gr_visibility = $('.form-create-group #select-status').val()
        
        var formData = new FormData();
        formData.append('group-name', gr_name);
        formData.append('group-topic', gr_category);
        formData.append('group-description', gr_description);
        formData.append('group-friend', gr_friend);
        formData.append('visibility', gr_visibility);
    
        $.ajax({
            url: '/add-group/',
            method: 'POST',
            dataType: 'JSON',
            data: formData,
            processData: false,
            contentType: false,
            success: function(res) {
                if (res && res.group) {
                    console.log("============ GROUP da luu vao db ============");
                    console.log("res.group = " + res.group)
                    console.log("name = " + res.group.name)
                    console.log("description = " + res.group.description)
                    console.log("date = " + res.group.date)
                    console.log("views = " + res.group.views)
                    console.log("visibility = " + res.group.visibility)
    
                    localStorage.setItem('groupData', JSON.stringify(res.group));
                    window.location.href = 'group-detail-manage';
                } else {
                    console.error("res.group is undefined");
                }
    
                
                // $(".post-div").prepend(_html);
                // $("#create-post-modal").removeClass("uk-flex uk-open")
            
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    })
}