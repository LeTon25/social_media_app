$(document).ready(function() {
    joinGroup()
    createPostGroup()
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

// Tham gia group
function joinGroup() {
    $(document).on("click", "#join-group", function(){
        let id = $(this).attr("data-group-id")
        console.log(id);
    
        $.ajax({
            url: "/join-group/",
            dataType: "JSON",
            data:{
                "id":id
            },
            success: function(res){
                if(res.group_id && res.group_detail_url) {
                    window.location.href = res.group_detail_url;
                }
                else {
                    console.log("Lỗi khi tham gia group")
                }
            }
        })
    })
}

// Tạo bài post trong group
function createPostGroup() {
    $('#group-post-form').submit(function(e) {
        e.preventDefault();
        console.log("createPostGroup")
        // let post_caption = $("#post-caption").val();
        // let post_visibility = $("#visibility").val();
    
        // var fileInput = $('#post-thumbnail')[0];
        // var file = fileInput.files[0];
        // var fileName = file.name; // Extract the filename
    
        // var formData = new FormData();
        // formData.append('post-caption', post_caption);
        // formData.append('visibility', post_visibility);
        // formData.append('post-thumbnail', file, fileName);
    
        // $.ajax({
        //   url: '/create-post/',
        //   type: 'POST',
        //   dataType: 'JSON',
        //   data: formData,
        //   processData: false,
        //   contentType: false,
    
        //   success: function(res) {
        //       console.log("============ POST da luu vao db ============");
        //       console.log(res.post)
        //       console.log(res.post.title);
        //       console.log(res.post.image_url);
        //       console.log(res.post.full_name);
        //       console.log(res.post.profile_image);
        //       console.log(res.post.date);
              
        //       let _html = '<div class="card lg:mx-0 uk-animation-slide-bottom-small mt-3 mb-3">\
        //       <div class="flex justify-between items-center lg:p-4 p-2.5">\
        //           <div class="flex flex-1 items-center space-x-4">\
        //               <a href="#">\
        //                   <img src="' + res.post.profile_image + '" style="width: 40px; height: 40px;" class="bg-gray-200 border border-white rounded-full w-10 h-10" />\
        //               </a>\
        //               <div class="flex-1 font-semibold capitalize">\
        //                   <a href="#" class="text-black dark:text-gray-100">' + res.post.full_name + '</a>\
        //                   <div class="text-gray-700 flex items-center space-x-2">' + res.post.date + ' ago \
        //                       <ion-icon name="story-time"></ion-icon>\
        //                   </div>\
        //               </div>\
        //           </div>\
        //           <div>\
        //               <a href="#"> <i class="icon-feather-more-horizontal text-2xl hover:bg-gray-200 rounded-full p-2 transition -mr-1 dark:hover:bg-gray-700"></i> </a>\
        //               <div class="bg-white w-56 shadow-md mx-auto p-2 mt-12 rounded-md text-gray-500 hidden text-base border border-gray-100 dark:bg-gray-900 dark:text-gray-100 dark:border-gray-700" uk-drop="mode: click;pos: bottom-right;animation: uk-animation-slide-bottom-small">\
        //                   <ul class="space-y-1">\
        //                       <li>\
        //                           <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
        //                               <i class="uil-share-alt mr-1"></i> Share\
        //                           </a>\
        //                       </li>\
        //                       <li>\
        //                           <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
        //                               <i class="uil-edit-alt mr-1"></i>  Edit Post \
        //                           </a>\
        //                       </li>\
        //                       <li>\
        //                           <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
        //                               <i class="uil-comment-slash mr-1"></i>   Disable comments\
        //                           </a>\
        //                       </li>\
        //                       <li>\
        //                           <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
        //                               <i class="uil-favorite mr-1"></i>  Add favorites \
        //                           </a>\
        //                       </li>\
        //                       <li>\
        //                           <hr class="-mx-2 my-2 dark:border-gray-800">\
        //                       </li>\
        //                       <li>\
        //                           <a href="#" uk-toggle="target: #delete-post-modal" data-id="{{p.id}}" class="link-delete-post flex items-center px-3 py-2 text-red-500 hover:bg-red-100 hover:text-red-500 rounded-md dark:hover:bg-red-600">\
        //                               <i class="uil-trash-alt mr-1"></i>  Delete\
        //                           </a>\
        //                       </li>\
        //                   </ul>\
        //               </div>\
        //           </div>\
        //       </div>\
        //       <div uk-lightbox>\
        //               <div class="p-5 pt-0 border-b dark:border-gray-700 pb-3">\
        //                   ' + res.post.title + '\
        //               </div>\
        //           <div class="grid grid-cols-2 gap-2 px-5">\
        //               <!-- Show thumnnail -->\
        //               <a href="' + res.post.image_url + '" class="col-span-2">  \
        //                   <img src="' + res.post.image_url + '" style="width: 100%; height: 300px; object-fit: cover;" alt="" class="rounded-md w-full lg:h-76 object-cover">\
        //               </a>\
        //           </div>\
        //       </div>\
        //       <div class="p-4 space-y-3">\
        //           <div class="flex space-x-4 lg:font-bold">\
        //               <a  class="flex items-center space-x-2  text-blue-500" style="cursor: pointer;" >\
        //                   <div class="p-2 rounded-full like-btn'+res.post.id+' text-black " id="like-btn" data-like-btn="'+res.post.id+'">\
        //                       <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-blue-100">\
        //                           <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />\
        //                       </svg>\
        //                   </div>\
        //                   <div> Like</div>\
        //               </a>\
        //               <a href="#" class="flex items-center space-x-2">\
        //                   <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
        //                       <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
        //                           <path fill-rule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clip-rule="evenodd" />\
        //                       </svg>\
        //                   </div>\
        //                   <div> <b><span id="comment-count'+res.post.id+'">0</span></b> Comment</div>\
        //               </a>\
        //               <a href="#" class="flex items-center space-x-2 flex-1 justify-end">\
        //                   <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
        //                       <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
        //                           <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />\
        //                       </svg>\
        //                   </div>\
        //                   <div> Share</div>\
        //               </a>\
        //           </div>\
        //           <div class="flex items-center space-x-3 pt-2">\
        //               \
        //               <div class="dark:text-gray-100">\
        //                   <strong><span id="like-count'+res.post.id+'">0</span></strong> Likes\
        //               </div>\
        //           </div>\
        //           <div class="border-t py-4 space-y-4 dark:border-gray-600" id="comment-div'+res.post.id+'">\
        //           </div>\
        //               <a href="#" class="hover:text-blue-600 hover:underline">No Comments </a>\
        //               <div class="bg-gray-100 rounded-full relative dark:bg-gray-800 border-t">\
        //                   <input placeholder="Add your Comment..." id="comment-input'+res.post.id+'" data-comment-input="'+res.post.id+'" class="bg-transparent max-h-10 shadow-none px-5 comment-input'+res.post.id+'">\
        //                   <div class="-m-0.5 absolute bottom-0 flex items-center right-3 text-xl">\
        //                       <a style="cursor: pointer;" id="comment-btn" class="comment-btn'+res.post.id+'" data-comment-btn="'+res.post.id+'">\
        //                           <ion-icon name="send-outline" class="hover:bg-gray-200 p-1.5 rounded-full"></ion-icon>\
        //                       </a>\
        //                   </div>\
        //               </div>\
        //           </div>\
        //   </div>\
        //       ';
        //   $(".post-div").prepend(_html);
        //   $("#create-post-modal").removeClass("uk-flex uk-open")
        //   $('#post-caption').val("")
        //   $('#preview_post_thumbnail').attr("src", "")
        //   },
        //   error: function(xhr, status, error) {
        //     console.error(error);
        //   }
        // });
    });
}