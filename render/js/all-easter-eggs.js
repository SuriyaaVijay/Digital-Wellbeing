"use strict";

let kirby = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/kirby.gif";
  img.style.width = "350px";
  img.style.height = "300px";
  img.style.transition = "6s all linear";
  img.style.position = "fixed";
  img.style.left = "-400px";
  img.style.bottom = "0px";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.left = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 6000);
};

let mario = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/mario.gif";
  img.style.width = "350px";
  img.style.height = "300px";
  img.style.transition = "6s all linear";
  img.style.position = "fixed";
  img.style.left = "-400px";
  img.style.bottom = "calc(-50% + 330px)";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.left = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 6000);
};

var pikachu = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/pikachu.gif";
  img.style.width = "250px";
  img.style.height = "149px";
  img.style.transition = "1s all";
  img.style.position = "fixed";
  img.style.left = "calc(50% - 125px)";
  img.style.bottom = "-149px";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.bottom = "0px";
  }, 50);
  window.setTimeout(function() {
    shock.style.width = "100%";
    shock.style.height = "100%";
    shock.style.left = 0;
    shock.style.top = 0;
    shock.style.position = "fixed";
    shock.style.zIndex = 9999999;
    shock.style.background = "#fffb95";
    shock.style.opacity = 0;
    document.body.appendChild(shock);
    for (var x = 0; x < 81; x++) {
      (function(x) {
        window.setTimeout(function() {
          if (x % 2 === 0) {
            shock.style.opacity = 0;
          } else {
            shock.style.opacity = 0.3;
          }
        }, x * 25);
      })(x);
    }
  }, 2500);
  window.setTimeout(function() {
    img.style.bottom = "-149px";
  }, 4300);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
    shock.parentNode.removeChild(shock);
  }, 5400);
};

let pikarun = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/running-pikachu.gif";
  img.style.width = "450px";
  img.style.height = "350px";
  img.style.transition = "4s all";
  img.style.position = "fixed";
  img.style.left = "-400px";
  img.style.bottom = "calc(-50% + 320px)";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.left = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 4300);
};

var piqiu = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/piqiu.gif";
  img.style.width = "374px";
  img.style.height = "375px";
  img.style.transition = "13s all";
  img.style.position = "fixed";
  img.style.right = "-374px";
  img.style.bottom = "calc(-50% + 320px)";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.right = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 10300);
};

let pokeball = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/pokeball.gif";
  img.style.width = "500px";
  img.style.height = "350px";
  img.style.transition = "8s all linear";
  img.style.position = "fixed";
  img.style.left = "-450px";
  img.style.bottom = "-10px";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.left = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 8000);
};
var psyduck = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/psyduck.gif";
  img.style.width = "500px";
  img.style.height = "500px";
  img.style.transition = "1s all";
  img.style.position = "fixed";
  img.style.left = "calc(50% - 250px)";
  img.style.bottom = "-600px";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.bottom = "0px";
  }, 30);
  window.setTimeout(function() {
    img.style.bottom = "-600px";
  }, 4300);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
    shock.parentNode.removeChild(shock);
  }, 5400);
};

var salamander = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/salamander.gif";
  img.style.width = "374px";
  img.style.height = "375px";
  img.style.transition = "13s all";
  img.style.position = "fixed";
  img.style.right = "-374px";
  img.style.bottom = "calc(-50% + 320px)";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.right = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 10300);
};

var snorlax = function() {
  var shock = document.createElement("div");
  var img = new Image();
  img.src = "./images/snorlax.gif";
  img.style.width = "374px";
  img.style.height = "375px";
  img.style.transition = "13s all";
  img.style.position = "fixed";
  img.style.right = "-374px";
  img.style.bottom = "-10px";
  img.style.zIndex = 999999;
  document.body.appendChild(img);
  window.setTimeout(function() {
    img.style.right = "calc(100% + 500px)";
  }, 50);
  window.setTimeout(function() {
    img.parentNode.removeChild(img);
  }, 10300);
};

// 5% chance of seeing a random egg
var probaOfRandomEgg = 0.05;

var aRandomEasterEgg = function(proba) {
  if (Math.random() < (probaOfRandomEgg || probaOfRandomEgg)) {
    var allEasterEggs = [ kirby, mario, pikachu, pikarun, piqiu, pokeball, psyduck, salamander, snorlax ];
    var randomEasterEgg = allEasterEggs[Math.floor(Math.random() * allEasterEggs.length)];
    randomEasterEgg();
  };
};