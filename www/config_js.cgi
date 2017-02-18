#!/bin/tclsh

##
# @file config_js.cgi
# @brief Generiert die JavaScript-Konfigurationsdatei.
#
# @author Harima-kun
# @license Public Domain
##

source /etc/config/addons/email/config.tcl

################################################################################
# Hilfsfunktionen                                                              #
################################################################################

##
# @fn loadFromFile
# @brief Lädt den Inhalt einer Datei.
#
# Ist die Datei nicht vorhanden oder kommt es zu sonstigen Fehlern,
# wird eine leere Zeichenkette zurückgegeben.
#
# @param filename Dateiname
# @return Inhalt der Datei
##
proc loadFromFile { filename } {
  set content ""
  catch  {
    set fd [open $filename r]
    set content [read $fd]
    close $fd
  }
  return $content
}

##
# @fn jsstring
# @brief Codiert eine Zeichenkette als JavaScript-String.
#
# Dabei werden die wichtigsten Sonderzeichen durch Escape-Sequenzen ersetzt.
#
# @param Zeichenkette
# @return Codierte Zeichenkette
##
proc jsstring { value } {
  return [string map {
    "\\" "\\"
    "\"" "\\\""
    "\'" "\\\'"
    "\t" "\\t"
    "\r" "\\r"
    "\n" "\\n"
    
  } $value]
}

################################################################################
# Ausgabefunktionen                                                            #
################################################################################

##
# @fn putMail
# @brief Gibt die E-Mail-Daten aus.
##
proc putMails {} {
  global MAIL_DIR MAIL_IDS
  set first 1
  
  puts "  Mails:"
  puts "  \["
  
  foreach id $MAIL_IDS {
    if { 1 != $first } then { puts "    ," } else { set first 0 }
    array set mail {}
    set mail(Id)     $id
    set mail(Description) {}
    set mail(To)      {}
    set mail(Subject) {}
    set mail(AttType) {}
    set mail(Attachment) {}
    set mail(Snapuser) {}
    set mail(Snappass) {}
    set mail(Content) {}
    set mail(Tcl)     "false"
    set mail(Prio)     "false"
    
    catch { array set mail [loadFromFile "$MAIL_DIR/$id.mail"] } 
    
    
    puts "    \{"
    puts "      \"id\": \"[jsstring $mail(Id)]\","
    puts "      \"description\": \"[jsstring $mail(Description)]\","
    puts "      \"to\": \"[jsstring $mail(To)]\","
    puts "      \"subject\": \"[jsstring $mail(Subject)]\","
    puts "      \"atttype\": \"[jsstring $mail(AttType)]\","
    puts "      \"attachment\": \"[jsstring $mail(Attachment)]\","
    puts "      \"snapuser\": \"[jsstring $mail(Snapuser)]\","
    puts "      \"snappass\": \"[jsstring $mail(Snappass)]\","
    puts "      \"content\": \"[jsstring $mail(Content)]\","
    puts "      \"tcl\": \"$mail(Tcl)\","
    puts "      \"prio\": $mail(Prio)"
    puts "    \}"
  }
  
  puts "  \]"
}

##
# @fn putAccount
# @brief Gibt Informationen über das E-Mail-Konto aus.
##
proc putAccount {} {
  global ACCOUNT_FILE
  
  array set account {}
  set account(Server) {}
  set account(From) {}
  set account(Auth) {}
  set account(Username) {}
  set account(Password) {}
  set account(Port) {}
  set account(TLS) "false"
  set account(STARTTLS) "false"
  
  catch { array set account [loadFromFile $ACCOUNT_FILE] }
  
  puts "  Account:"
  puts "  \{"
  puts "    \"server\": \"[jsstring $account(Server)]\","
  puts "    \"from\": \"[jsstring $account(From)]\","
  puts "    \"auth\": \"[jsstring $account(Auth)]\","
  puts "    \"username\": \"[jsstring $account(Username)]\","
  puts "    \"password\": \"[jsstring $account(Password)]\","
  puts "    \"port\": \"[jsstring $account(Port)]\","
  puts "    \"tls\": \"[jsstring $account(TLS)]\","
  puts "    \"starttls\": $account(STARTTLS)"
  puts "  \}"
}

##
# @fn putUserScript
# @brief Gibt das benutzerdefinierte Tcl-Script aus.
##
proc putUserScript {} {
  global USER_SCRIPT_FILE
  
  puts "  \"UserScript\": \"[jsstring [loadFromFile $USER_SCRIPT_FILE]]\""
}

################################################################################
# Einsprungpunkt                                                               #
################################################################################

puts "Content-Type: text/javascript; charset=utf-8"
puts ""
puts "Configuration ="
puts "\{"
putMails
puts "  ,"
putAccount
puts "  ,"
putUserScript
puts "\};"
