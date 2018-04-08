'use strict';

var url = ""
var time = ""

// get current tab url
chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    url = tabs[0].url;
});

// call server with url  !!!

// get text from search bar when clicked 
var search_string ="";
function get_search_string() {
    search_string = document.getElementById("searchbox").value;

    
    // send server the search string !!!
    document.getElementById('demo').textContent = search_string;

}

document.getElementById('search').onclick = get_search_string;

// dynamically adds butttons
// button_text = ""
function add(index, button_text, button_value) {
  //Create an input type dynamically.   
  var element = document.createElement("button");
  var br = document.createElement("br");

  //Assign different attributes to the element. 
  element.type = "button";
  element.value = button_value;
  element.innerHTML = button_text;
  element.name = index; 
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

var i;
for (i = 0; i < 10; i++) { 
	var num = i * 10
	var n = num.toString();
    add(i, "hello", n);
}

// 2. This code loads the IFrame Player API code asynchronously.
// var tag = document.createElement('script');

// tag.src = "https://www.youtube.com/iframe_api";
// var firstScriptTag = document.getElementsByTagName('script')[0];
// firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var request = new XMLHttpRequest();

request.open('GET', 'http://127.0.0.1:5000/todo/api/v1.0/tasks/1', true);
request.onload = function () {

  // Begin accessing JSON data here
  var data = JSON.parse(this.response);

  if (request.status >= 200 && request.status < 400) {
  	console.log(data)
  	console.log(data.task.description)
  } else {
    console.log('error');
  }
}

request.send();

// data.forEach(movie => {
//   // Log each movie's title
//   console.log(movie.title);
// });

// {
// 	"3.3"	: "I’ve had my ups and downs",
// 	"5.8"	: "my fair share of bumpy roads and heavy winds."
// 	"9.868"	: "That’s what made me what I am today."
// 	"13.901": "Now I stand here before you."
// 	"16.985": "What you see is a body crafted to perfection"
// }