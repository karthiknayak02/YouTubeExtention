'use strict';

var url = ""

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
  element.style.height = "30px";
  element.style.width = "350px";
  element.style.border= "0.5px solid #ff1a1a";

  // element.onclick =  button_click(element);// this is where you should JUMPPPPP

  // var foo = document.getElementById("resultfield");
  //Append the element in page (in span).  
  // foo.appendChild(element);
  document.body.appendChild(element);
  document.body.appendChild(br);
}


// document.addEventListener("click", function(e) {
//   if (!e.target.classList.contains("terms")) {
//     return;
//   }
//   console.log("hi");
//   var name = e.target.textContent;


// });



var time = ""
function button_click(element) {
	console.log(element.value);
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


var i;
for (i = 0; i < 10; i++) { 
    add(i, "hello", "3");
}

// 2. This code loads the IFrame Player API code asynchronously.
// var tag = document.createElement('script');

// tag.src = "https://www.youtube.com/iframe_api";
// var firstScriptTag = document.getElementsByTagName('script')[0];
// firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function seekVideo(tabid){

// var codeToExecute = 'document.querySelector(".ytp-play-button.ytp-button").click()';
// var codeToExecute = 'document.getElementById("movie_player").seekTo(26)';
var codeToExecute = "document.querySelector('video').currentTime = 20";


var executing = chrome.tabs.executeScript(
  		tabid,
  		{code: codeToExecute}
	);
//executing.then(onExecuted, onError);
}

// {
// 	"3.3"	: "I’ve had my ups and downs",
// 	"5.8"	: "my fair share of bumpy roads and heavy winds."
// 	"9.868"	: "That’s what made me what I am today."
// 	"13.901": "Now I stand here before you."
// 	"16.985": "What you see is a body crafted to perfection"
// }