// $(document).ready(function () {
//     console.log("OKKKKKKKKKKKKK")
//     handleWebSocket()
//     selectImageAndFile()
//     handleNoMessage()
//     handleOnInfoAndVideoCall()
// });

// // Xử lý web socket
// function handleWebSocket() {
//     var receiver = null;
//     var receiver_id = "{{ reciever.username }}";
//     var logged_in = "{{ request.user.username }}";
//     const pathname = window.location.pathname;

//     const parts = pathname.split('/');
//     const username = parts[parts.length - 2];

//     if (receiver_id === logged_in) {
//         receiver = receiver_id;
//     } else {
//         receiver = receiver_id;
//     }

//     var socket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + receiver + '/');

//     socket.onopen = function () {
//         console.log('WebSocket connection established.');
//     }

//     // Hiển thị tin nhắn 
//     socket.onmessage = function (event) {
//         var data = JSON.parse(event.data);
//         var message = data.message;
//         var sender = data.sender;
//         var profileImage = data.profile_image;
//         var reciever = data.reciever;
//         var image_path = data.image_paths;
//         var file_path = data.file_paths;
//         if (sender === "{{sender}}") {
//             var chatMessage = ''
//             // load hình ảnh nếu có
//             if (image_path.length != 0) {
//                 chatMessage += '<div class="message-bubble me">'
//                 chatMessage += '<div class="message-bubble-inner">';
//                 chatMessage += '<div class="message-text">';
//                 chatMessage += '<a href = <img src="/media/uploads/images/' + image_path + '" target="_blank">'    
//                 chatMessage += '<img src="/media/uploads/images/' + image_path + '" class="message-image" alt="">';
//                 chatMessage += '</a>'
//                 chatMessage += '</div>';
//                 chatMessage += '</div>';
//                 chatMessage += '<div class="clearfix"></div>';
//                 chatMessage += '</div>';
//             }
//             // load file nếu có 
//             if (file_path.length !=0)
//             {
//                 chatMessage += '<div class="message-bubble me">'
//                 chatMessage += '<div class="message-bubble-inner">';
//                 chatMessage += '<div class="message-text">';
//                 chatMessage += '<a href ="/media/uploads/files/' + file_path + '" target="_blank">'  
//                 chatMessage += '<div class="d-flex justify-content-between align-items-center p-1 text-black ">'
//                 chatMessage += '<i class="bi bi-file-earmark-fill"></i>'
//                 chatMessage += '<span class="message-reply__file__name">'+ file_path + '</span>'
//                 chatMessage += '</div>'
//                 chatMessage += '</a>'
//                 chatMessage += '</div>';
//                 chatMessage += '</div>';
//                 chatMessage += '<div class="clearfix"></div>';
//                 chatMessage += '</div>';
//             }
//             chatMessage += '<div class="message-bubble me">';
//             chatMessage += '<div class="message-bubble-inner">';
//             chatMessage += '<div class="message-avatar"><img src="' + profileImage + '" alt=""></div>';
//             chatMessage += '<div class="message-text">';
//             chatMessage += '<p>' + message + '</p>';
//             chatMessage += '</div>';
//             chatMessage += '</div>';
//             chatMessage += '<div class="clearfix"></div>';
//             chatMessage += '</div>';
//             $('#chat-messages').append(chatMessage);
//             var chatContainer = document.querySelector('.chat_container');
//             chatContainer.scrollTop = chatContainer.scrollHeight;
//         } else {
//             var chatMessage = ''
//             if (image_path.length != 0) {
//                 chatMessage += '<div class="message-bubble">'
//                 chatMessage += '<div class="message-bubble-inner">';
//                 chatMessage += '<div class="message-text">';
//                 chatMessage += '<a href = <img src="/media/uploads/images/' + image_path + '" target="_blank" >'    
//                 chatMessage += '<img src="/media/uploads/images/' + image_path + '" class="message-image" alt="">';
//                 chatMessage += '</a>'
//                 chatMessage += '</div>';
//                 chatMessage += '</div>';
//                 chatMessage += '<div class="clearfix"></div>';
//                 chatMessage += '</div>';
//             }
//             // load file nếu có 
//             if (file_path.length !=0)
//             {
//                 chatMessage += '<div class="message-bubble me">'
//                 chatMessage += '<div class="message-bubble-inner">';
//                 chatMessage += '<div class="message-text">';
//                 chatMessage += '<a href = <img src="/media/uploads/files/' + file_path + '" target="_blank">'  
//                 chatMessage += '<div class="d-flex justify-content-between align-items-center p-1 text-white ">'
//                 chatMessage += '<i class="bi bi-file-earmark-fill"></i>'
//                 chatMessage += '<span class="message-reply__file__name">'+ file_path + '</span>'
//                 chatMessage += '</div>'
//                 chatMessage += '</a>'
//                 chatMessage += '</div>';
//                 chatMessage += '</div>';
//                 chatMessage += '<div class="clearfix"></div>';
//                 chatMessage += '</div>';
//             }
//             chatMessage += '<div class="message-bubble">';
//             chatMessage += '<div class="message-bubble-inner">';
//             chatMessage += '<div class="message-avatar"><img src="' + profileImage + '" alt=""></div>';
//             chatMessage += '<div class="message-text">';
//             chatMessage += '<p>' + message + '</p>';
//             chatMessage += '</div>';
//             chatMessage += '</div>';
//             chatMessage += '<div class="clearfix"></div>';
//             chatMessage += '</div>';
//             $('#chat-messages').append(chatMessage);

//             var chatContainer = document.querySelector('.chat_container');
//             chatContainer.scrollTop = chatContainer.scrollHeight;
//         }
//     }

//     socket.onclose = function () {
//         console.log('WebSocket connection closed.');
//     }

//     // Xử lí khi nhấn nút gửi
//     handleSentMessage()
// }

// // Xử lí khi nhấn nút gửi tin nhắn
// function handleSentMessage() {
//     $('#send-btn').on('click', function () {
//         var input = $('#chat-input');
//         var message = input.val();
//         var sender = "{{request.user.username}}";
//         var image = '';
//         var fileDoc_data='';
//         var fileDoc_name='';
//         $('.message-reply__file').each((index, element) => {
//             let type = element.getAttribute('data-type')
//             switch (type) {
//                 case 'anh':
//                     image = element.getAttribute('src')
//                     break;
//                 case 'file':
//                     fileDoc_data = element.getAttribute('data-value') ?  element.getAttribute('data-value') : ''
//                     fileDoc_name = element.getElementsByClassName('message-reply__file__name')[0].textContent ? element.getElementsByClassName('message-reply__file__name')[0].textContent : ''
//                     break;    
//             }
//         })
//         console.log(fileDoc_data)
//         var data = {
//             'message': message,
//             'sender': sender,
//             'reciever': username,
//             'image': `${image}`,
//             'file_doc':`${fileDoc_data}`,
//             'file_name': `${fileDoc_name}`
//         };
//         socket.send(JSON.stringify(data));
//         input.val('');
//         $('#fileInputContainer').empty();
//         var sendButton = $('#send-btn');
//         sendButton.prop('disabled', true);
//         $(".chat_container").scrollTop(100000000000);
//     });
// }

// // Xử lý chọn ảnh hoặc file
// function selectImageAndFile() {
//     $(".chat_container").scrollTop(100000000000);
//     $('.message-reply__action').each((index, element) => {
//         $(element).click(e => {
//             let action = e.currentTarget.getAttribute('data-action')
//             switch (action) {
//                 case 'anh':
//                     uploadImage()
//                     break;
//                 case 'file':
//                     uploadFile()
//                     break;
//                 case 'icon':
//                     break;
//             }
//         })
//     })
// }



// // Các xử lý khi gửi "Ảnh"
// function uploadImage() {
//     $('#imageInput').click()
//     $('#imageInput').change(function () {
//         var selectedFile = this.files[0];
//         if (selectedFile) {
//             var imgSelectorID = addImageElementToContainer()
//             addImageInputToContainer(imgSelectorID + ' img', selectedFile)
//             setEventToDeleteFileIcon(imgSelectorID + ' .message-reply__file-delete')
//             $('#imageInput').val('')
//         }
//     })
// }
// function addImageInputToContainer(selector, selectedFile) {

//     var reader = new FileReader();
//     reader.onload = function (event) {
//         $(selector).attr('src', event.target.result).show();
//     };
//     reader.readAsDataURL(selectedFile);
// }
// function addImageElementToContainer() {
//     let dateN = new Date()
//     let id = `${dateN.getSeconds()}${dateN.getMinutes()}${dateN.getHours()}`

//     let elementN = `
//         <div class="message-reply__file" id="${id}" data-type="anh">
//                 <img src="" class="message-reply__file__image" alt="">
//                 <div class="message-reply__file-delete" data-target-ele="${id}">
//                     <i class="bi bi-x-circle "></i>
//                 </div>
//         </div>
//          `
//     $('#fileInputContainer').append(elementN)
//     return '#' + id;
// }
// function setEventToDeleteFileIcon(selector) {
//     $(selector).click(function (e) {
//         $('#' + this.getAttribute('data-target-ele')).remove()
//     })
// }



// // Xử lí khi gửi file doc,pdf,txt...
// function uploadFile() {
//     $('#fileInput').click()
//     $('#fileInput').change(function () {
//         var selectedFile = this.files[0];
//         addFileElementToContainer(selectedFile)
//         $('#fileInput').val('')
//     })
// }
// function addFileElementToContainer(selectedFile) {
//     let dateN = new Date()
//     let id = `${dateN.getSeconds()}${dateN.getMinutes()}${dateN.getHours()}`
//     if (selectedFile) {
//         let elementN = `
//         <div class="message-reply__file message-reply__file--doc" id="${id}" data-type="file">
//             <div class="d-flex justify-content-between align-items-center p-1 text-white ">
//                 <i class="bi bi-file-earmark-fill"></i>
//                 <span class="message-reply__file__name">${selectedFile.name}</span>
//             </div>
//             <div class="message-reply__file-delete" data-target-ele="${id}">
//                 <i class="bi bi-x-circle "></i>
//             </div>
//         </div>
//          `
//         $('#fileInputContainer').append(elementN)
//         $('#' + id + ' .message-reply__file-delete').click(function (e) {
//             $('#' + this.getAttribute('data-target-ele')).remove()
//         })
//         var reader = new FileReader();
//         reader.onload = function (event) {
//             $('#'+id).attr('data-value', event.target.result);
//         };
//         reader.readAsDataURL(selectedFile);
//     }
// }


// // Xử lí khi chưa nhập tin nhắn thì không cho nhắn nút gửi
// function handleNoMessage() {
//     var chatInputValue = $('#chat-input');
//     var sendButton = $('#send-btn');
//     // Disable the button initially
//     sendButton.prop('disabled', true);
//     // Check input field on keyup event
//     chatInputValue.on('keyup', function () {
//         var inputText = $(this).val();
//         // Enable/disable button based on input field value
//         if (inputText.trim() !== '') {
//             sendButton.prop('disabled', false);
//         } else {
//             sendButton.prop('disabled', true);
//         }
//     });
// }

// // Xử lý bật info và ấn vào video call
// function handleOnInfoAndVideoCall() {
//     $('.message-info__btn').click(function () {
//         $('.message-info').toggle()
//     })

//     $('.call__btn').click(function () {
//         console.log("call__btn OKKKK")
//     })
    
//     $('.video-call__btn').click(async function () {
//         let user_id = $(this).attr("data-call-user")
//         let user_name = $(this).attr("data-name-user")
        
//         let response = await fetch(`/get_token/?channel=${user_id}`)
//         let data = await response.json()

//         let UID = data.uid
//         let token = data.token

//         sessionStorage.setItem('UID', UID)
//         sessionStorage.setItem('token', token)
//         sessionStorage.setItem('user_id', user_id)
//         sessionStorage.setItem('user_name', user_name)

//         window.open(`/core/inbox/${user_name}/video/`, "_blank", "width=800,height=600,left=400,top=100")
//     })
// }