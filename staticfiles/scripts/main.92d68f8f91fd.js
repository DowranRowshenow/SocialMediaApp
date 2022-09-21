/* VARIABLES */
var settings = {
    cursor: false,
    sounds: true,
    animaitons: true,
    notifications: true,
}
var is_dropdown = false;
const userName = JSON.parse(document.getElementById('json-userName').textContent);
const userEmail = JSON.parse(document.getElementById('json-userEmail').textContent);
const userHash = JSON.parse(document.getElementById('json-userHash').textContent);
const friendSocket = new WebSocket('ws://' + window.location.host + '/ws/friends/' + userName + '/');

/* MAIN */
Main();
function Main()
{
    Settings();
    Defaults();
}
function Settings()
{
    try
    {
        storageSettings = JSON.parse(localStorage.getItem("settings"));
        if (storageSettings != null)
        {
            settings = storageSettings;
        }
        else
        {
            localStorage.setItem("settings", JSON.stringify(settings));
        }
    } 
    catch {}
    console.log(settings);
}
function saveSettings()
{
    localStorage.setItem("settings", JSON.stringify(settings));
}
function Defaults()
{
    if (!settings.cursor)
    {
        try
        { document.getElementById('cursor').checked = settings.cursor; }
        catch {}
        cursor();
    }
    if (!settings.animaitons)
    {
        try
        { document.getElementById('animations').checked = settings.animaitons; }
        catch {}
        animaitons();
    }
}

/* WEBSOCKETS */
friendSocket.onmessage = function(e)
{
    const data = JSON.parse(e.data);
    if (data.type == 'friend_request')
    {
        let html = '';
        grouper = document.getElementById("friend_requests_grouper");
        if (!side.contains(grouper))
        {
            html += '<div id="friend_requests_grouper" class="grouper">';
            html +=     '<i class="fa fa-angle-down"></i>';
            html +=     '<a class="grouper_text">' + trans_friend_requests.innerHTML + '</a>';
            html +=     '<i class="fa fa-circle font_red font_8"></i>';
            html += '</div>';
        }
        html += '<div class="item cur_pointer_dark dropdown">';
        html +=     '<img src="' + data.sender_image + '" class="item_img"></img>';
        html +=     '<a class="item_text">' + data.sender_username + '</a>';
        html +=     '<i class="profile_bar_i fa fa-ellipsis-vertical cur_pointer_dark dropbtn" onclick="on_dropdown_click(dropdown_request_' + data.sender_username + ');"></i>'; 
        html +=     '<div id="dropdown_request_' + data.sender_username + '" class="dropdown-content">'; 
        html +=         '<div class="drop_item horizontal">'; 
        html +=             '<i class="drop_item_icon fa address-card"></i>'; 
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
        document.getElementById("side").innerHTML += html;
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
    username = document.getElementById('friend_request_form_input').value;
    if (username)
    {
        const requestSocket = new WebSocket('ws://' + window.location.host + '/ws/friends/' + username + '/');
        
        requestSocket.onopen = function (e) 
        {
            requestSocket.send(JSON.stringify({
                'username': username,
            }));
        }
        requestSocket.onmessage = function (e) 
        {
            requestSocket.close(1000, "Work complete");

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
                    html +=     '<i class="fa fa-circle font_red font_8"></i>';
                    html += '</div>';
                }
                html += '<div class="item cur_pointer_dark dropdown">';
                html +=     '<img src="' + data.receiver_image + '" class="item_img"></img>';
                html +=     '<a class="item_text">' + username + '</a>';
                html +=     '<i class="profile_bar_i fa fa-ellipsis-vertical cur_pointer_dark dropbtn" onclick="on_dropdown_click(dropdown_request_' + username + ');"></i>'; 
                html +=     '<div id="dropdown_request_' + username + '" class="dropdown-content">'; 
                html +=         '<div class="drop_item horizontal">'; 
                html +=             '<i class="drop_item_icon fa address-card"></i>'; 
                html +=             '<a class="drop_item_text">' + trans_profile.innerHTML + '</a>'; 
                html +=         '</div>'; 
                html +=     '</div>'; 
                html += '</div>'; 
                document.getElementById("nav").innerHTML += html;
            }
        }
    }
}

/* ON CLICK EVENTS */
function page(page)
{
    page_form_input.value = page;
    page_form.submit();
}
var friends = document.getElementsByClassName("friend");
for (var i = 0; i < friends.length; i++) 
{
    friends[i].addEventListener('click', function (e) 
    {
        if (e.target.classList.contains('dont')) 
        {
            return false;
        } 
        else 
        {
            friend_form_input.value=e.target.getAttribute("value");
            friend_form.submit();
        }
    }, false);
}
function open_section(item, image_url = null, content = null, element = null)
{
    item.style.opacity = 1;
    item.style.visibility = 'visible';
    if (image_url) 
    { 
        image_section_image.src = image_url;
    }
    if (content) 
    { 
        edit_post_form_content_input.value = content; 
        TextArea(edit_post_form_content_input);
    }
}
function close_section(item)
{
    scrollBottom_2 = document.getElementById("scroll_bottom_chat");
    item.style.opacity = 0;
    item.style.visibility = 'hidden';
    friend_request_form_input.value = "";
    post_form_content_input.value = "";
    post_form_image_input.value = "";
    image_section_image.src = "";
    edit_post_form_content_input.value = "";
}
function on_dropdown_click(item) 
{
    if (!is_dropdown)
    {
        is_dropdown = true;
        item.classList.toggle("show");
    }
    else
    {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) 
        {
            if (dropdowns[i].classList.contains('show')) 
            {
                is_dropdown = false;
                dropdowns[i].classList.remove('show');
            }
        }
    }
}
// Close the dropdown if the user clicks outside of it
window.onclick = function(event) 
{
    if (!event.target.matches('.dropbtn')) 
    {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) 
        {
            if (dropdowns[i].classList.contains('show')) 
            {
                is_dropdown = false;
                dropdowns[i].classList.remove('show');
            }
        }
    }
}
function checkScroll()
{
    scrollTop = document.getElementById("scroll_top");
    scrollTop_2 = document.getElementById("scroll_top_chat");
    scrollBottom = document.getElementById("scroll_bottom");
    scrollBottom_2 = document.getElementById("scroll_bottom_chat");
    if (chat_messages.scrollTop > 100)
    {
        if (scrollTop) { scrollTop.style.top = "60px"; }
        if (scrollTop_2) { scrollTop_2.style.top = "40px"; }
    }
    else
    {
        if (scrollTop) { scrollTop.style.top = "-60px"; }
        if (scrollTop_2) { scrollTop_2.style.top = "-60px"; }
    }
    if (chat_messages.scrollTop < chat_messages.scrollHeight - 1100)
    {
        if (scrollBottom) { scrollBottom.style.bottom = "20px"; }
        if (scrollBottom_2) { scrollBottom_2.style.bottom = "100px"; }
    }
    else
    {
        if (scrollBottom) { scrollBottom.style.bottom = "-60px"; }
        if (scrollBottom_2) { scrollBottom_2.style.bottom = "-60px"; }
    }
}

/* FUNCTIONS */
function cursor()
{
    var root = document.querySelector(':root');
    if(document.getElementById('cursor').checked)
    {
        var cursors = document.getElementsByClassName('cur_default');
        var arrFromList = Array.prototype.slice.call(cursors);
        for (var i = 0; i < arrFromList.length; i++) 
        {
            arrFromList[i].classList.add('cur_default_dark');
            arrFromList[i].classList.remove('cur_default');
        }
        var cursors = document.getElementsByClassName('cur_pointer');
        var arrFromList = Array.prototype.slice.call(cursors);
        for (var i = 0; i < arrFromList.length; i++) 
        {
            arrFromList[i].classList.add('cur_pointer_dark');
            arrFromList[i].classList.remove('cur_pointer');
        }
        var cursors = document.getElementsByClassName('cur_text');
        var arrFromList = Array.prototype.slice.call(cursors);
        for (var i = 0; i < arrFromList.length; i++) 
        {
            arrFromList[i].classList.add('cur_text_dark');
            arrFromList[i].classList.remove('cur_text');
        }
        root.style.setProperty('--cursor_default', '');
        settings.cursor = true;
    }
    else
    {
        var cursors = document.getElementsByClassName('cur_default_dark');
        var arrFromList = Array.prototype.slice.call(cursors);
        for (var i = 0; i < arrFromList.length; i++) 
        {
            arrFromList[i].classList.add('cur_default');
            arrFromList[i].classList.remove('cur_default_dark');
        }
        var cursors = document.getElementsByClassName('cur_pointer_dark');
        var arrFromList = Array.prototype.slice.call(cursors);
        for (var i = 0; i < arrFromList.length; i++) 
        {
            arrFromList[i].classList.add('cur_pointer');
            arrFromList[i].classList.remove('cur_pointer_dark');
        }
        var cursors = document.getElementsByClassName('cur_text_dark');
        var arrFromList = Array.prototype.slice.call(cursors);
        for (var i = 0; i < arrFromList.length; i++) 
        {
            arrFromList[i].classList.add('cur_text');
            arrFromList[i].classList.remove('cur_text_dark');
        }
        root.style.setProperty('--cursor_default', '../library/cursors/Dark/Arrow.cur');
        settings.cursor = false;
    }
    saveSettings();
}
function animaitons()
{
    var root = document.querySelector(':root');
    if (document.getElementById('animations').checked)
    {
        root.style.setProperty('--animations_4', '1.2s');
        settings.animaitons = true;
    }
    else
    {
        root.style.setProperty('--animations_4', '0s');
        settings.animaitons = false;
    }
    saveSettings();
}
function scrollToTop() 
{
    try 
    { chat_messages.scrollTo({ top: 0, behavior: 'smooth' }); } 
    catch{}
}
function scrollToBottom() 
{
    try 
    { chat_messages.scrollTo({ top: chat_messages.scrollHeight, behavior: 'smooth' }); } 
    catch{}
}

/* UI ELEMENTS */
function TextArea(element) 
{
    element.style.height = 0;
    element.style.height = (element.scrollHeight) + "px";
}
var input = document.getElementById("post_form_content_input");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
  }
});

/* FILE INPUT */
function getName(element) 
{
    var fullPath = element.src;
    var filename = fullPath.replace(/^.*[\\\/]/, '');
    return filename;
}
function loadURLToInputFiled(url, fileName)
{
    getImgURL(url, (imgBlob)=>{
      let file = new File([imgBlob], fileName,{type:"image/jpeg", lastModified:new Date().getTime()}, 'utf-8');
      let container = new DataTransfer(); 
      container.items.add(file);
      edit_post_form_image_input.files = container.files;  
    });
}
function getImgURL(url, callback)
{
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        callback(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
}

/* SELECT */
var x, i, j, l, ll, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /* When an item is clicked, update the original select box,
        and the selected item: */
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            yl = y.length;
            for (k = 0; k < yl; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}
function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);