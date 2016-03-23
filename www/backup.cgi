#!/bin/tclsh

###
# 
# Run Backup Script
# by HMside 2016
#
###

#set datum [clock seconds] 
#set datum [clock format $datum -format {%d-%m-%Y}]

# Backup ausführen
set backup "/etc/config/addons/email/backup.sh"
exec $backup

# Ausgabe des Backups
after 2000
   if { [file exists "/etc/config/addons/email/email-backup.tar.gz"] } {
    puts "Content-Type: text/plain"
    puts ""
    puts -nonewline "BACKUPOK"
 } else {
    puts "Content-Type: text/plain"
    puts ""
    puts "ERROR"
      }