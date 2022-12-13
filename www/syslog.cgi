#!/bin/tclsh

set logfile "/var/log/messages"
set filter "msmtp"

puts "Content-Type: text/plain; charset=iso-8859-1"
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
