const friendSocket = new WebSocket('ws://' + window.location.host + '/ws/friends/' + userName + '/');

/* WEBSOCKETS */
friendSocket.onmessage = function(e)
{
    const data = JSON.parse(e.data);
    if (data.type == 'friend_request')
    {
        let html = '';
        var cursor = '';
        grouper = document.getElementById("friend_requests_grouper");
        if (!side.contains(grouper))
        {
            html += '<div class="width_auto vertical cur_pointer">';
            html +=     '<div class="grouper width_auto" onclick="grouper(friend_requests_grouper, friend_requests_grouper_icon);">';
            html +=         '<i id="friend_requests_grouper_icon" class="fa fa-angle-down font_light"></i>';
            html +=         '<a class="grouper_text font_light">' + trans_friend_requests.innerHTML + '</a>';
            html +=         '<i class="fa fa-circle font_red font_8"></i>';
            html +=     '</div>';
            html +=      '<div id="friend_requests_grouper">';
            html +=     '</div>';
            html += '</div>';
        }
        document.getElementById("side").innerHTML += html;
        html =  '<div class="item ' + cursor + ' dropdown dropbtn" onclick="on_dropdown_click(dropdown_request_' + data.sender_username + ');">';
        html +=     '<img src="' + data.sender_image + '" class="item_img"></img>';
        html +=     '<a class="item_text font_light">' + data.sender_username + '</a>';
        html +=     '<i class="profile_bar_i fa fa-ellipsis-vertical ' + cursor + ' dropbtn font_light"></i>'; 
        html +=     '<div id="dropdown_request_' + data.sender_username + '" class="dropdown-content">'; 
        html +=         '<div class="drop_item horizontal" onclick="profile_view_form_input.value=\'' + data.sender_hash + '\';profile_view_form.submit();">'; 
        html +=             '<i class="drop_item_icon fa fa-address-card"></i>'; 
        html +=             '<a class="drop_item_text">' + trans_profile.innerHTML + '</a>'; 
        html +=         '</div>'; 
        html +=         '<div class="drop_item horizontal" onclick="window.location=\'' + '/friends/friend_request_accept/' + data.sender_email + '\';">'; 
        html +=             '<i class="drop_item_icon fa fa-check font_green"></i>';
        html +=             '<a class="drop_item_text">' + trans_accept.innerHTML + '</a>'; 
        html +=         '</div>'; 
        html +=         '<div class="drop_item horizontal" onclick="window.location=\'' + '/friends/friend_request_decline/' + data.sender_email +  '\';">'; 
        html +=             '<i class="drop_item_icon fa fa-cancel font_red"></i>'; 
        html +=             '<a class="drop_item_text">' + trans_decline.innerHTML + '</a>'; 
        html +=         '</div>'; 
        html +=     '</div>'; 
        html += '</div>';
        document.getElementById("friend_requests_grouper").innerHTML += html;
    }
    else if (data.type == 'friend_accept')
    {
        if (confirm(data.username + ' has accepted your friend request.')) {
            location.reload();
        }
    }
    else if (data.type == 'friend_decline')
    {
        alert(data.email);
    }
}
function friend_request(username = null)
{
    if (username == null)
    {
        username = document.getElementById('friend_request_form_input').value;
    }
    if (username)
    {
        const requestSocket = new WebSocket('ws://' + window.location.host + '/ws/friends/' + username + '/');
        
        requestSocket.onopen = function (e) 
        {
            requestSocket.send(JSON.stringify({
                'username': username,
            }));
            friend_section_loader.style.display = "flex";
        }
        requestSocket.onmessage = function (e) 
        {
            requestSocket.close(1000, "Work complete");
            friend_section_loader.style.display = "none";

            const data = JSON.parse(e.data);
            if (data.type == 'error')
            {
                friend_request_form_error.innerHTML = '<li>' + data.error + '</li>';
            }
            else if (data.type == 'friend_request')
            {
                close_section(friend_section);
                let html = '';
                grouper = document.getElementById("requested_friends_grouper");
                if (!nav.contains(grouper))
                {
                    html += '<div id="requested_friends_grouper" class="grouper width_auto">';
                    html +=     '<i class="fa fa-angle-down"></i>';
                    html +=     '<a class="grouper_text">' + trans_sent_friend_requests.innerHTML + '</a>';
                    html +=     '<i class="fa fa-circle font_green font_8"></i>';
                    html += '</div>';
                }
                html += '<div class="item cur_pointer dropdown">';
                html +=     '<img src="' + data.receiver_image + '" class="item_img"></img>';
                html +=     '<a class="item_text">' + username + '</a>';
                html +=     '<i class="profile_bar_i fa fa-ellipsis-vertical cur_pointer dropbtn" onclick="on_dropdown_click(dropdown_request_' + username + ');"></i>'; 
                html +=     '<div id="dropdown_request_' + username + '" class="dropdown-content">'; 
                html +=         '<div class="drop_item horizontal">'; 
                html +=             '<i class="drop_item_icon fa fa-address-card"></i>'; 
                html +=             '<a class="drop_item_text">' + trans_profile.innerHTML + '</a>'; 
                html +=         '</div>'; 
                html +=     '</div>'; 
                html += '</div>'; 
                document.getElementById("nav").innerHTML += html;
            }
        }
    }
}