'use strict';
 
var url = ""
var time = ""
 
 
// get current tab url
chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    url = tabs[0].url;
    console.log(url);
 
    var obj = {"url": url};
    var jsonString= JSON.stringify(obj);
    console.log(jsonString);
 
    // send server the url link
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/todo/api/v1.0/tasks', true);
 
    // Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/JSON");
 
    xhr.onreadystatechange = function() {//Call a function when the state changes.
    if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        // Request finished. Do processing here.
    }
    }
    xhr.send(jsonString);
});
 
 
 
// request.open('GET', 'http://127.0.0.1:5000/todo/api/v1.0/tasks/normal?link=' + url, true);
// call server with url  !!!
 
// get text from search bar when clicked
var search_string ="";
function get_search_string() {
    search_string = document.getElementById("searchbox").value;
 
    var obj = {"url": url, "search": search_string};
    var jsonString= JSON.stringify(obj);
    console.log(jsonString);
 
    // send server the search string !!!
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://localhost:5000/todo/api/v1.0/tasks/2', true);
 
    // Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/JSON");
 
    xhr.onreadystatechange = function() {//Call a function when the state changes.
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            // Request finished. Do processing here.
        }
    }
    xhr.send(jsonString);

    generate();
 
}
 
document.getElementById('search').onclick = get_search_string;
 
// dynamically adds butttons
// button_text = ""
function add(button_text, button_value) {
  //Create an input type dynamically.  
  var element = document.createElement("button");
  var br = document.createElement("br");
 
  //Assign different attributes to the element.
  element.type = "button";
  element.value = button_value;
  element.innerHTML = button_text;
  // element.name = index;
  element.class = "terms"
  element.style.borderRadius = "10px";
  element.style.height = "30px";
  element.style.width = "300px";
  element.style.border= "0.5px solid #ff1a1a";
 
  element.addEventListener("click", button_click); // this is where you JUMPPPPP
 
  document.body.appendChild(element);
  document.body.appendChild(br);
}
 
 
 
function button_click(e) {
     
    time = e.target.value;
    chrome.tabs.query({url: "*://*.youtube.com/*"}, logTabs);
    // time = button_value
    // console.log(time)
}
 
 
function logTabs(tabs) {
  for (let tab of tabs) {
    // tab.url requires the `tabs` permission
    seekVideo(tab.id);
  }
}
 
function seekVideo(tabid){
    var codeToExecute = "document.querySelector('video').currentTime = " + time;
 
    chrome.tabs.executeScript(tabid, {code: codeToExecute});
}
 
// var i;
// for (i = 0; i < 10; i++) {
//  var num = i * 10
//  var n = num.toString();
//     add(i, "hello", n);
// }
 
// 2. This code loads the IFrame Player API code asynchronously.
// var tag = document.createElement('script');
 
// tag.src = "https://www.youtube.com/iframe_api";
// var firstScriptTag = document.getElementsByTagName('script')[0];
// firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
 
function generate() {
    var request = new XMLHttpRequest();
 
    request.open('GET', 'http://127.0.0.1:5000/todo/api/v1.0/tasks/3', true);
    request.onload = function () {
 
      // Begin accessing JSON data here
      var data = JSON.parse(this.response);
 
      if (request.status >= 200 && request.status < 400) {
        console.log(data)
        console.log(data.task)
        var p = data;
 
        for (var key in p) {
        if (p.hasOwnProperty(key)) {
            console.log(key + " -> " + p[key]);
            add(key.toString().split(":")[0], p[key]);
        }
    }
      } else {
        console.log('error');
      }
    }
 
    request.send();
 
}
 
// document.getElementById('gen').onclick = generate

    var request = new XMLHttpRequest();
 
    request.open('GET', 'http://127.0.0.1:5000/todo/api/v1.0/tasks/1', true);
    request.onload = function () {
 
      // Begin accessing JSON data here
      var data = JSON.parse(this.response);
 
      if (request.status >= 200 && request.status < 400) {
        console.log(data)
        console.log(data.task)
        var p = data;
 
        for (var key in p) {
        if (p.hasOwnProperty(key)) {
            console.log(key + " -> " + p[key]);
            add(key.toString().split(":")[0], p[key]);
        }
    }
      } else {
        console.log('error');
      }
    }
 
    request.send();
 
 
// function post(path, params, method) {
//     method = method || "post"; // Set method to post by default if not specified.
 
//     // The rest of this code assumes you are not using a library.
//     // It can be made less wordy if you use one.
//     var form = document.createElement("form");
//     form.setAttribute("method", method);
//     form.setAttribute("action", path);
 
//     for(var key in params) {
//         if(params.hasOwnProperty(key)) {
//             var hiddenField = document.createElement("input");
//             hiddenField.setAttribute("type", "hidden");
//             hiddenField.setAttribute("name", key);
//             hiddenField.setAttribute("value", params[key]);
 
//             form.appendChild(hiddenField);
//         }
//     }
 
//     document.body.appendChild(form);
//     form.submit();
// }
 
 
 
 
 
// var x = new XMLHttpRequest();
// x.open("GET", "http://video.google.com/timedtext?lang=en&v=M7FIvfx5J10", true);
// x.onreadystatechange = function () {
//   if (x.readyState == 4 && x.status == 200)
//   {
//     var doc = x.responseXML;
//     console.log(doc)
//     // …
//   }
// };
// x.send(null);
 
 
// var data = "key=9a0dba48727b9d159eb67a44074d9eb5&lang=en&txt=" + YOUR_TXT_VALUE&url=YOUR_URL_VALUE&doc=YOUR_DOC_VALUE&tt=YOUR_TT_VALUE";
 
// var xhr = new XMLHttpRequest();
// xhr.withCredentials = true;
 
// xhr.addEventListener("readystatechange", function () {
//   if (this.readyState === this.DONE) {
//     console.log(this.responseText);
//   }
// });
 
// xhr.open("POST", "http://api.meaningcloud.com/topics-2.0");
// xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded");
 
// xhr.send(data);