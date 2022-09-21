/* VARIABLES */
const postHash = JSON.parse(document.getElementById('json-postHash').textContent);
const postSocket = new WebSocket('ws://' + window.location.host + '/ws/posts/' + postHash + '/');

/* MAIN */
scrollToBottom();

/* WEBSOCKETS */
postSocket.onmessage = function(e) 
{
    const data = JSON.parse(e.data);
    if (data.type == 'post_comment') 
    {
        let html = '';

        var i = parseInt(post_comment_count.innerHTML);
        post_comment_count.innerHTML = i + 1;

        if (userName == data.userName)
        {
            html += '<div class="right">';
            html +=     '<div class="message_box_rigth margin_right_20">';
            html +=         '<div class="message_right">';
            html +=           '<a class="message_text font_light">' + data.content + '</a>';
            html +=      '</div>';
            html +=     '<div>' + data.sentDateTime + '</div></div>';
            html += '</div>';
            html += '<div id="chat_spacer" class="message_user spacer">&nbsp;</div>';
        } 
        else 
        {
            html += '<div class="message_user message_box left">';
            html +=     '<div class="user_field top">';
            html +=         '<img class="user_field_img radius_20" src="' + data.senderImage + '"></img>';
            html +=     '</div>'; 
            html +=     '<div class="message_field">'; 
            html +=         '<a class="message_field_text font_light">' + data.userName + '</a>'; 
            html +=         '<div class="message">'; 
            html +=             '<a class="message_text font_light">' + data.content + '</a>'; 
            html +=         '</div>'; 
            html +=         data.sentDateTime; 
            html +=     '</div>'; 
            html += '</div>';
            html += '<div id="chat_spacer" class="message_user spacer">&nbsp;</div>';
        }
        chat_spacer.remove();
        chat_messages.innerHTML += html;
        scrollToBottom();
    } 
    else if (data.type == 'post_like' || data.type == 'post_dislike') 
    {
        likes.innerHTML = data.likes;
        dislikes.innerHTML = data.dislikes;
    }
}
function send_comment()
{
    var content = chat_message_input.value;
    if (content)
    {
        content = content.replace("<","&lt;");
        content = content.replace(">","&gt;");
        postSocket.send(JSON.stringify({
            'type': 'comment_post',
            'content': content,
        }));
    }
    else
    {
        alert('You can not send empty comment!');
    }
    chat_message_input.value = '';
}
function like_post()
{
    postSocket.send(JSON.stringify({
        'type': 'like_post',
    }));
}
function dislike_post()
{
    postSocket.send(JSON.stringify({
        'type': 'dislike_post',
    }));
}

/* FUNCTIONS */
var input = document.getElementById("chat_message_input");
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        send_comment();
    }
});
function scrollToBottom() 
{
    try 
    { chat_messages.scrollTo({ top: chat_messages.scrollHeight, behavior: 'smooth' }); } 
    catch{}
}