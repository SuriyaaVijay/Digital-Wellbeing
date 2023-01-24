/*
 * render_utils.js for https://github.com/Naereen/uLogMe/
 * MIT Licensed, https://lbesson.mit-license.org/
*/

// place for some more generic utility functions

// take number of seconds and convert it to human-readable
// string like 5h30m21s
function strTimeDelta(secs) {
  var hours = Math.floor(secs/60/60);
  secs = secs - hours*60*60;
  var minutes = Math.floor(secs/60);
  secs = secs - minutes * 60;
  var txt = secs + "s";
  if(minutes > 0) txt = minutes + "m " + txt;
  if(hours > 0) txt = hours + "h " + txt;
  return txt;
}

// pretty print date in a nice format, utility function
function ppDay(date) {
  return ["Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday",
        "Saturday"][date.getDay()]
        + " "
        + (function (d) {
            var s = d.toString(), l = s[s.length-1];
            return s+(["st","nd","rd"][l-1] || "th");
        })(date.getDate())
        + " "
        + ["Jan.", "Feb.", "Mar.",
        "Apr.", "May.", "Jun.",
        "Jul.", "Aug.", "Sep.",
        "Oct.", "Nov.", "Dec."][date.getMonth()]
        + ", "
        + date.getFullYear();
}

// pretty print date in a nice format, utility function
function ppDate(date) {
  return ppDay(date)+ " " + ppHour(date);
}

function ppHour(date) {
  return date.getHours() + ":" + ("0" + date.getMinutes()).slice(-2);
}

function ppDateShort(date) {
  var months = ["Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"];
  var days = ["Sun", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat"];
  return days[date.getDay()] + ", " + date.getDate() + " " + months[date.getMonth()];
}
