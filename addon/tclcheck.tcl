#!/bin/tclsh

###
# 
# Little TCL Debugger, write error msg to tcl.log
# by HMside 03/2016
#
###

if {[catch {source /etc/config/addons/email/userscript.tcl} msg]} {
#    puts "I got an error: $msg"
#    puts "The stack trace was this:\n$errorInfo"
       # error msg to data
        set data "$msg"
        # set name of logfile
        set filename "/var/log/tcl.log"
        # open the logfile for writing
        set fileId [open $filename "w"]
        # send data to logfile -
        # failure to add '-nonewline' will result in an extra newline
        # at the end of the file
        puts -nonewline $fileId $data
        # close the file, ensuring the data is written out before you continue
        # with processing.
        close $fileId
        }