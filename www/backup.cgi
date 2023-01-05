#!/bin/tclsh

###
# 
# Run Backup Script
# by HMside 2016
#
###

source session.tcl

puts "Content-Type: text/plain; charset=iso-8859-1"
puts ""

if {[info exists sid] && [check_session $sid]} {
  #set datum [clock seconds] 
  #set datum [clock format $datum -format {%d-%m-%Y}]
  
  # Backup ausführen
  set backup "/etc/config/addons/email/backup.sh"
  exec $backup
  
  # Ausgabe des Backups
  after 2000
  if { [file exists "/etc/config/addons/email/email-backup.tar.gz"] } {
    puts -nonewline "BACKUPOK"
  } else {
    puts -nonewline "ERROR: could not find backup"
  }
} else {
  puts -nonewline "Error: no valid session"
}
