#!/bin/tclsh

###
# 
# Little TCL Debugger, write error msg to tcl.log
# by HMside 2016
#
###

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
    puts "Content-Type: text/plain"
    puts ""
    puts "$tclerror"
  } else {
  	puts "Content-Type: text/plain"
    puts ""
    puts -nonewline "TCLOK"
  }
              
