/*
 * ga.js for https://github.com/Naereen/uLogMe/
 * MIT Licensed, https://lbesson.mit-license.org/
 *
 * A short automatic script for Google Analytics audit service
 * Automatically detect the current domain name (host location)
 * and adapt the settings accordingly. By Lilian Besson, (C), 2013-16
*/
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  /* Here are set the default values for these variables,
   * corresponding to the default domain. */
  var my_id = 'UA-38514290-15',    my_domain = 'ga-beacon.appspot.com';
  /* Here a case-by-case analysis is done to change this variable
   * when the page is located on another web server. */
  switch(window.location.host) {
    case 'lbesson.bitbucket.org':
        my_id = 'UA-38514290-14'; my_domain = 'bitbucket.org';
        break;
    case 'perso.crans.org':
        my_id = 'UA-38514290-1'; my_domain = 'crans.org';
        break;
    default:
        break; };
  ga('create', my_id, my_domain); ga('send', 'pageview');
