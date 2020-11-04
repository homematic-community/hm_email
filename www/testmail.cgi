#!/bin/tclsh
##
# @file testmail.cgi
# @brief Sendet eine Testmail mit der Template ID aus dem Querystring
#
# @author Uwe Langhammer
# @license Public Domain
##

load tclrega.so
source querystring.tcl
source session.tcl

puts "Content-Type: text/plain; charset=iso-8859-1"
puts ""

set email "/etc/config/addons/email/email"

if {[info exists sid] && [check_session $sid]} {
  if { [info exists env(QUERY_STRING)] } {
    regsub -all {[&=]} $env(QUERY_STRING) { } query_str
    regsub -all {  } $query_str { {} } query_str
    foreach {key val} $query_str {
      set query($key) $val
    }
    if { [info exists query(ID)] } {
      set ID [ format "%02d" $query(ID) ]
      exec $email $ID
      puts -nonewline "OK"
    } else {
      puts -nonewline "ERROR: ID missing"
    }
  }
} else {
  puts -nonewline "Error: no valid session"
}
