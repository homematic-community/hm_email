#!/bin/tclsh

set logfile "/var/log/messages"
set filter *

catch {
  set input $env(QUERY_STRING)
  set pairs [split $input &]
  foreach pair $pairs {
    if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
      set $varname $val
    }
  }
}

puts "Content-Type: text/plain;Charset=ISO-8859-1"
puts ""

if {[catch {open "$logfile" r} fd]} {
  puts "ERROR open($logfile) $fd"
} else {
  while {[gets $fd line] >= 0} {
    if {[string match -nocase "*$filter*" $line]} {
      puts $line
    }
  }
  close $fd
}
