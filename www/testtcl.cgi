#!/bin/tclsh

###
# 
# Little TCL Debugger, write error msg to tcl.log
# by HMside 2016
#
###

load tclrega.so
source querystring.tcl
source session.tcl

puts "Content-Type: text/plain; charset=iso-8859-1"
puts ""

if {[info exists sid] && [check_session $sid]} {
  # tcl.log File löschen
  set killlog "/var/log/tcl.log"
  catch { file delete -force -- $killlog }
  
  # TCL Check ausführen
  set tcl "/etc/config/addons/email/tclcheck.tcl"
  exec $tcl
  
  # tcl.log öffnen und Inhalt in tcllog übergeben
  if { [file exists "/var/log/tcl.log"] } {
    set tcllog [open "/var/log/tcl.log" r]
    set tclerror [read $tcllog]
    close $tcllog
    puts "$tclerror"
  } else {
    puts -nonewline "TCLOK"
  }
} else {
  puts -nonewline "Error: no valid session"
}
