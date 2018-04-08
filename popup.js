'use strict';

var url = ""

chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    url = tabs[0].url;
});

var x="";
function get_search_string() {
    x = document.getElementById("searchbox").value;
    document.getElementById('demo').textContent = x;
}

document.getElementById('search').onclick = get_search_string;


function add(type) {
  //Create an input type dynamically.   
  var element = document.createElement("button");
  var br = document.createElement("br");
  //Assign different attributes to the element. 
  element.type = "button";
  element.value = "typfasfae";
  element.innerHTML = 'hello';
  element.name = "button name"; 
  element.style.height = "30px";
  element.style.width = "350px";
  element.style.border= "0.5px solid #ff1a1a";

  element.onclick = get_search_string; // this is where you should JUMPPPPP

  // var foo = document.getElementById("resultfield");
  //Append the element in page (in span).  
  // foo.appendChild(element);
  document.body.appendChild(element);
  document.body.appendChild(br);
}

// document.getElementById("addBtn").onclick = function() {
//   add("text");
// };

var i;
for (i = 0; i < 10; i++) { 
    add("hello");
}

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// {
// 	"3.3"	: "I’ve had my ups and downs",
// 	"5.8"	: "my fair share of bumpy roads and heavy winds."
// 	"9.868"	: "That’s what made me what I am today."
// 	"13.901": "Now I stand here before you."
// 	"16.985": "What you see is a body crafted to perfection"
// }