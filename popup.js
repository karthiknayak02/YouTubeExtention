// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

var x="";
function get_search_string() {
    x = document.getElementById("searchbox").value;
    document.getElementById('demo').textContent = x;
}

document.getElementById('search').onclick = get_search_string;


function add(type) {
  //Create an input type dynamically.   
  var element = document.createElement("input");
  //Assign different attributes to the element. 
  element.type = "button";
  element.value = "button value";
  element.name = "button name"; 
  element.onclick = get_search_string; // this is where you should JUMPPPPP

  var foo = document.getElementById("fooBar");
  //Append the element in page (in span).  
  foo.appendChild(element);
}

document.getElementById("addBtn").onclick = function() {
  add("text");
};
