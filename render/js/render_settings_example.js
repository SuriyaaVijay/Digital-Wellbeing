
var title_mappings = [
    // Internet
    {pattern: /Google Chrome/,        mapto: "Firefox"}, // lol
    {pattern: /Firefox/,              mapto: "Firefox"},
    // Social browsing
    {pattern: /Outlook/,              mapto: "Mails"},
    {pattern: /GMail/,                mapto: "Mails"},
    {pattern: /Thunderbird/,          mapto: "Mails"},
    {pattern: /Skype/,                mapto: "Skype"},
    {pattern: /Facebook/,             mapto: "Facebook"},
    {pattern: /Messenger/,            mapto: "Facebook"},
    {pattern: /Slack/,                mapto: "Slack"},
    // Self-quantified browsing
    {pattern: /Stats pour/,           mapto: "Self-Quantified"},
    {pattern: /Munin/,                mapto: "Self-Quantified"},
    {pattern: /uLogMe - /,            mapto: "Self-Quantified"},
    {pattern: /WakaTime/,             mapto: "Self-Quantified"},
    {pattern: /Google Analytics/,     mapto: "Self-Quantified"},
    // Agenda
    {pattern: /TODO list/,            mapto: "Agenda"},
    {pattern: /Google Agenda/,        mapto: "Agenda"},
    // Hacking browsing
    {pattern: /GitHub/,               mapto: "GitHub"},
    {pattern: / · Naereen/,           mapto: "GitHub"},
    {pattern: /Bitbucket/,            mapto: "Bitbucket"},
    // Music
    {pattern: /YouTube/,              mapto: "YouTube"},
    {pattern: /VLC/,                  mapto: "VLC"},
    {pattern: / par /,                mapto: "GMusicBrowser"},
    // Programming
    {pattern: /MATLAB/,               mapto: "Matlab"},
    {pattern: /Figure/,               mapto: "Figure"},
    {pattern: /Notebook/,             mapto: "Notebook"},
    {pattern: /notebook/,             mapto: "Notebook"},
    {pattern: /.pdf/,                 mapto: "PDF"},
    {pattern: /Terminal/,             mapto: "Terminal"},
    // Sublime Text 3 patterns
    {pattern: /Sublime Text/,         mapto: "ST3"},
    {pattern: /\.py.*Sublime Text/,   mapto: "ST3 Python"},
    {pattern: /\.sh.*Sublime Text/,   mapto: "ST3 Bash"},
    {pattern: /\.js.*Sublime Text/,   mapto: "ST3 JS"},
    {pattern: /\.html.*Sublime Text/, mapto: "ST3 HTML"},
    {pattern: /\.css.*Sublime Text/,  mapto: "ST3 CSS"},
    {pattern: /\.tex.*Sublime Text/,  mapto: "ST3 LaTeX"},
    {pattern: /\.md.*Sublime Text/,   mapto: "ST3 Markdown"},
    {pattern: /\.rst.*Sublime Text/,  mapto: "ST3 rST"},
    // Visual Studio Code pattern
    {pattern: /Visual Studio/,        mapto: "VS-Code"},
    {pattern: /\.py.*Visual Studio/,  mapto: "VS-Code Python"},
    {pattern: /\.sh.*Visual Studio/,  mapto: "VS-Code Bash"},
    {pattern: /\.js.*Visual Studio/,  mapto: "VS-Code JS"},
    {pattern: /\.html.*Visual Studio/,mapto: "VS-Code HTML"},
    {pattern: /\.css.*Visual Studio/, mapto: "VS-Code CSS"},
    {pattern: /\.tex.*Visual Studio/, mapto: "VS-Code LaTeX"},
    {pattern: /\.md.*Visual Studio/,  mapto: "VS-Code Markdown"},
    {pattern: /\.rst.*Visual Studio/, mapto: "VS-Code rST"},
    // Atom pattern
    {pattern: /Atom/,                 mapto: "Atom"},
    {pattern: /\.py.*Atom/,           mapto: "Atom Python"},
    {pattern: /\.sh.*Atom/,           mapto: "Atom Bash"},
    {pattern: /\.js.*Atom/,           mapto: "Atom JS"},
    {pattern: /\.html.*Atom/,         mapto: "Atom HTML"},
    {pattern: /\.css.*Atom/,          mapto: "Atom CSS"},
    {pattern: /\.tex.*Atom/,          mapto: "Atom LaTeX"},
    {pattern: /\.md.*Atom/,           mapto: "Atom Markdown"},
    {pattern: /\.rst.*Atom/,          mapto: "Atom rST"},
    // PyCharm patterns
    {pattern: /PyCharm/,              mapto: "PyCharm"},
    {pattern: /\.py.*PyCharm/,        mapto: "PyCharm Python"},
    {pattern: /\.md.*PyCharm/,        mapto: "PyCharm Markdown"},
    {pattern: /\.rst.*PyCharm/,       mapto: "PyCharm rST"},
    // Extra
    {pattern: /__LOCKEDSCREEN/,       mapto: "Computer locked"}, // __LOCKEDSCREEN is a special token
    {pattern : /__SUSPEND/,           mapto: "Computer suspended"}, // __SUSPEND is a special token
];


function mapwin(w) {
  var n = title_mappings.length;
  var mapped_title = "Misc";
  for(var i=0;i<n;i++) {
    var patmap = title_mappings[i];
    if(patmap.pattern.test(w)) {
      mapped_title = patmap.mapto;
    }
  }
  return mapped_title;
}

// These groups will be rendered together in the "barcode view". For example, I like
// to group my work stuff and play stuff together.
var display_groups = [];

display_groups.push(["GitHub", "Bitbucket"]); // Hacking browsing
display_groups.push(["Mails", "Skype", "Facebook", "Slack"]); // Social browsing

display_groups.push(["YouTube", "VLC", "GMusicBrowser"]); // Music
display_groups.push(["Agenda", "Self-Quantified"]); // Self-quantified browsing and Agenda

display_groups.push(["Firefox", "Misc"]); // Internet
display_groups.push(["ST3", "Atom", "VS-Code", "PyCharm"]); // Generic coding
display_groups.push(["Terminal"]); // Terminal
display_groups.push(["Matlab", "Figure", "ST3 Python", "VS-Code Python", "Atom Python", "Notebook", "PyCharm Python"]); // Coding Python related
display_groups.push(["ST3 Bash", "VS-Code Bash", "Atom Bash"]); // Coding bash related
display_groups.push(["ST3 JS", "ST3 HTML", "ST3 CSS", "VS-Code JS", "VS-Code HTML", "VS-Code CSS", "Atom JS", "Atom HTML", "Atom CSS"]); // Coding js/html/css related
display_groups.push(["ST3 Markdown", "ST3 rST", "VS-Code Markdown", "VS-Code rST", "Atom Markdown", "Atom rST", "PyCharm Markdown", "PyCharm rST"]); // Coding md/rst related
display_groups.push(["ST3 LaTeX", "VS-Code LaTeX", "Atom LaTeX", "PDF"]); // Paper writing related

// display_groups.push(["Locked Screen"]); // Computer not being used
display_groups.push(["Computer locked", "Computer idle", "Computer suspended"]); // computer not being used


// Activity groups to group related work. This will be shown as inner piechart ring.
// All related activities will be shown in outer piechart ring.
var activity_groups = [];
activity_groups.push({name:"Fun", titles: ["YouTube", "VLC", "GMusicBrowser"]});
activity_groups.push({name:"Coding", titles: ["GitHub", "Bitbucket", "Matlab", "Figure", "Notebook", "ST3 Python", "ST3 Bash", "ST3 JS", "ST3 HTML", "ST3 CSS", "ST3 Markdown", "ST3 rST", "ST3 LaTeX", "ST3", "VS-Code Python","VS-Code Bash", "VS-Code JS", "VS-Code HTML", "VS-Code CSS", "VS-Code Markdown", "VS-Code rST", "VS-Code LaTeX", "VS-Code", "Atom Python","Atom Bash", "Atom JS", "Atom HTML", "Atom CSS", "Atom Markdown", "Atom rST", "Atom LaTeX", "Atom", "Terminal", "PyCharm", "PyCharm Python", "PyCharm Markdown", "PyCharm rST"]});
activity_groups.push({name:"Social", titles: ["Mails", "Skype", "Facebook", "Slack", , "Misc"]});
activity_groups.push({name:"Browsing", titles: ["Self-Quantified", "Firefox", "Agenda", "PDF"]});
activity_groups.push({name:"Away", titles: ["Computer locked", "Computer idle", "Computer suspended"]});


// list of titles that classify as "hacking", or being productive in general
// the main goal of the day is to get a lot of focused sessions of hacking
// done throughout the day. Windows that aren't in this list do not
// classify as hacking, and they break "streaks" (events of focused hacking)
// the implementation is currently quite hacky, experimental and contains
// many magic numbers.
var hacking_titles = ["Notebook", "Terminal", "Matlab", "ST3 Python", "ST3 JS", "ST3 HTML", "ST3 HTML", "ST3 LaTeX", "ST3 Markdown", "ST3 rST", "ST3", "VS-Code Python", "VS-Code JS", "VS-Code HTML", "VS-Code HTML", "VS-Code LaTeX", "VS-Code Markdown", "VS-Code rST", "VS-Code", "Atom Python", "Atom JS", "Atom HTML", "Atom HTML", "Atom LaTeX", "Atom Markdown", "Atom rST", "Atom", "PyCharm", "PyCharm Python", "PyCharm Markdown", "PyCharm rST"];
var hacking_title = "Continuous typing";
var draw_hacking = true; // by default turning this on

// draw notes row?
var draw_notes = true;

// experimental coffee levels indicator :)
// looks for notes that mention coffee and shows
// levels of coffee in body over time
var draw_coffee = true;

// Reload interval in minutes. Set to 0 to turn off.
var auto_reload_interval = 0;
