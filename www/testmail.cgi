#!/bin/tclsh
##
# @file testmail.cgi
# @brief Sendet eine Testmail mit der Template ID aus dem Querystring
#
# @author Uwe Langhammer
# @license Public Domain
##

set email "/etc/config/addons/email/email"

if { [info exists env(QUERY_STRING)] } {
  regsub -all {[&=]} $env(QUERY_STRING) { } query_str
  regsub -all {  } $query_str { {} } query_str
  foreach {key val} $query_str {
    set query($key) $val
  }
  if { [info exists query(ID)] } {
    set ID [ format "%02d" $query(ID) ]
    exec $email $ID
    puts "Content-Type: text/plain"
    puts ""
    puts -nonewline "OK"
  } else {
    puts "Content-Type: text/plain"
    puts ""
    puts "ERROR ID missing"
  }
}
              
