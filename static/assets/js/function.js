// Add Friend
$(document).on("click", "#add-friend", function(){
    let id = $(this).attr("data-friend-id")
    console.log(id);

    $.ajax({
        url: "/add-friend/",
        dataType: "JSON",
        data:{
            "id":id
        },
        success: function(response){
            console.log("Bool ==",response.bool);
            if (response.bool == true) {
                $("#friend-text").html("<i class='fas fa-user-minus'></i> Cancel Request ")
                $(".add-friend"+id).addClass("bg-red-600")
                $(".add-friend"+id).removeClass("bg-blue-600")
            }
            if (response.bool == false) {
                $("#friend-text").html("<i class='fas fa-user-plus'></i> Add Friend ")
                $(".add-friend"+id).addClass("bg-blue-600")
                $(".add-friend"+id).removeClass("bg-red-600")
            }
        }
    })
})

// Accept Friend Request
$(document).on("click", "#accept-friend-request", function(){
    let id = $(this).attr("data-request-id")
    console.log(id);

    $.ajax({
        url: "/accept-friend-request/",
        dataType: "JSON",
        data: {
            "id":id
        },
        success: function(response){
            console.log(response.data);
            $(".reject-friend-request-hide"+id).hide()
            $(".accept-friend-request"+id).html("<i class='fas fa-check-circle'></i> Friend Request Accepted")
            $(".accept-friend-request"+id).addClass("text-white")
        }
    })
})

// Reject Friend Request
$(document).on("click", "#reject-friend-request", function(){
    let id = $(this).attr("data-request-id")
    console.log(id);

    $.ajax({
        url: "/reject-friend-request/",
        dataType: "JSON",
        data: {
            "id":id
        },
        success: function(response){
            console.log(response.data);
            $(".accept-friend-request-hide"+id).hide()
            $(".reject-friend-request"+id).html("<i class='fas fa-check-circle'></i> Friend Request Rejected")
            $(".reject-friend-request"+id).addClass("text-white")
        }
    })
})

// Hủy kết bạn User
$(document).on("click", "#unfriend", function(){
    let id = $(this).attr("data-friend-id")
    console.log(id);

    $.ajax({
        url: "/unfriend/",
        dataType: "JSON",
        data: {
            "id":id
        },
        success: function(response){
            console.log(response);
            $("#unfriend-text").html("<i class='fas fa-check-circle'></i> Friend Removed ")
            $(".unfriend"+id).addClass("bg-blue-600")
            $(".unfriend"+id).removeClass("bg-red-600")
        }
    })
})

// Block User
$(document).on("click", "#block-user-btn", function(){
    let id = $(this).attr("data-block-user")
    
    $.ajax({
        url: "/block-user/",
        dataType: "JSON",
        data: {
            "id":id
        },
        success: function(response){
            console.log(response);
            $(".block-text"+id).html("<i class='fas fa-check-circle'></i> User Blocked Successfully. ")
        }
    })
})
