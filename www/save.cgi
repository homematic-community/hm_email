#!/bin/tclsh

##
# @file save.cgi
# @brief Speichert die Konfiguration
#
# Zum Speichern wird ein HTTP POST an dieses Skript gesendet. Die HTTP-Query
# enthält Informationen über den Teil der Konfiguration, der gespeichert werden
# soll:
#   mail       Speichert eine E-Mail
#   account    Speichert die E-Mail-Kontodaten
#   userScript Speichert das benutzerdefinierte Tcl-Script
#
# Die POST-Daten sind im Allgemeinen wie folgt aufgebaut
# >  HeaderName:Value
# >  HeaderName:Value
# >
# >  Inhalt
#
# Es wird zunächst mit einigen Kopfdaten angefangen. Jeder Header umfasst genau
# eine Zeile. Bezeichnung und Wert des Headers sind durch einen Doppelpunkt
# voneinander getrennt. Es dürfen keine überflüssigen Leerzeichen enthalten 
# sein. Header-Namen sind case-sensitiv, d.h. es wird zwischen Groß- und Klein-
# schreibung unterschieden.
# Auf die Kopfdaten folgt eine Leerzeile. Dieser schleißt sich ein Inhalt an,
# der praktisch beliebigen Text enthalten darf.
# Welche Header benötigt werden und was der Inhalt bedeutet ist vom jeweiligen
# Kommando abhängig.
#
# Bei erfolgreichem Aufruf wird "OK" zurückgegeben, ansonsten "ERROR" gefolgt
# von dem Grund des Scheiterns.
#
# @author Harima-kun
# @license Public Domain
##

source session.tcl

puts "Content-Type: text/plain; charset=iso-8859-1"
puts ""

if { [info exists sid] && [check_session $sid] } {
  if { [catch {

  source /etc/config/addons/email/config.tcl

  ##############################################################################
  # Allgemeine Hilfsfunktionen                                                 #
  ##############################################################################
  
  ##
  # @fn saveToFile
  # @brief Speichert Daten in einer Datei
  #
  # @param filename Dateiname
  # @param content Zu speichernde Daten
  #
  # @return 0, falls das Speichern erfolgreich war
  ##
  proc saveToFile { filename content} {
    catch {
      set fd [open $filename w]
      puts -nonewline $fd $content
      close $fd
    }
  }
  
  ##############################################################################
  # Argumente                                                                  #
  ##############################################################################
  
  ##
  # @var __args
  # @brief Enthält die Argumente des Aufrufs
  ##
  array set __args {}

  ##
  # @fn __args_init
  # @brief Intialisiert die Argumente.
  #
  # Dazu werden die Post-Daten sowie die HTTP-Query ausgewertet.
  ##
  proc __args_init { } {
    global __args env
  
    # 1. Header parsen
    while { "" != [set line [gets stdin]] } {
      if { [regexp {([^:]+):(.*)} $line dummy name value] } then {
        set __args($name) $value
      }
    }
  
    # 2. Post-Daten einlesen
    set __args(Content) [read stdin]
  
    # 3. CGI-Query übernehmen
    if { [info exists env(QUERY_STRING)] } then {
      set input $env(QUERY_STRING)
      set pairs [split $input &]
      foreach pair $pairs {
        if {0 == [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
          set __args(Query) $pair
          break
        }
      }
    }
  }

  ##
  # @fn __args_get
  # @brief Liefert den Wert eines Arguments.
  #
  # Ist das Argument nicht enthalten, wird die leere Zeichenkette zurückgegeben.
  #
  # @param name Bezeichnung des Arguments
  # @return Wert des Arguments oder die leere Zeichenkette.
  ##
  proc __args_get { name } {
    global __args
  
    if { [info exists __args($name)] } {
      return $__args($name)
    } else {
      return ""
    }
  }

  ##############################################################################
  # Speicheroperationen                                                        #
  ##############################################################################
  
  ##
  # @fn __saveMail
  # @brief Speichert eine E-Mail
  #
  # Folgende Header werden ausgewertet:
  #   Id:          Id der E-Mail
  #   Description: Kurzbeschreibung der Vorlage
  #   To:          Empfänger
  #   Subject:     Betreffzeile
  #   AttType:     Datei von der CCU, oder Download
  #   Attachment:  Pfad zur Datei
  #   Snapuser:    Benutzername für Kamera Snapshots
  #   Snappass:    Kennwort für Kamera Snapshots
  #   Tcl:         Legt fest, ob Tcl für die E-Mail aktiv sein soll
  #
  # Der weitere Inhalt der Anfrage wird als Text der E-Mail interpretiert.
  ##
  proc __saveMail { } {
    global MAIL_DIR
    
    array set mail {}
    set mail(Description) [__args_get Description]
    set mail(To)      [__args_get To]
    set mail(Subject) [__args_get Subject]
    set mail(AttType) [__args_get AttType]
    set mail(Attachment) [__args_get Attachment]
    set mail(Snapuser) [__args_get Snapuser]
    set mail(Snappass) [__args_get Snappass]
    set mail(Content) [__args_get Content]
    set mail(Tcl)     [__args_get Tcl]
    set mail(Prio)     [__args_get Prio]
    
    saveToFile "$MAIL_DIR/[__args_get Id].mail" [array get mail]
  }
  
  ##
  # @fn __saveAccount
  # @brief Speichert die E-Mail-Kontoinformationen
  #
  # Folgende Header werden ausgwertet:
  #   Server:   SMTP Server
  #   From:     Absender
  #   Auth:     Form der Authentisierung (off, auto, plain, cram-md5, external oder login)
  #   User:     Benutzername
  #   Password: Passwort
  #   Port:     Port
  #   TLS:      Verschlüsselte Verbindung ein/aus
  #   STARTTLS: STARTTLS ein/aus
  #
  # Der weitere Inhalt wird ignoriert.
  ##
  proc __saveAccount { } {
    global ACCOUNT_FILE MSMTP_CONFIG_FILE
    
    array set account {}
    set account(Server)   [__args_get Server]
    set account(From)     [__args_get From]
    set account(Auth)     [__args_get Auth]
    set account(Username) [__args_get User]
    set account(Password) [__args_get Password]
    set account(Port)     [__args_get Port]
    set account(TLS)      [__args_get TLS]
	  set account(STARTTLS) [__args_get STARTTLS]
    
    saveToFile $ACCOUNT_FILE [array get account]
    
    # MSMTP Konfigurationsdatei erzeugen
    set fd [open $MSMTP_CONFIG_FILE w]

    puts $fd "# MSMTP Konfigurationsdatei"
    puts $fd "# -------------------------"
    puts $fd "# Diese Datei wurde automatisch generiert."
    puts $fd ""
    puts $fd "# Standardwerte für alle weiteren Accounts"
    puts $fd "defaults"
    puts $fd ""
    if { $account(TLS) == "true" } {
      puts $fd "# Transport Layer Security (TLS)"
      puts $fd "tls on"
      puts $fd "tls_certcheck off"
      puts $fd ""
    }
	if { $account(STARTTLS) == "true" } {
      puts $fd "tls_starttls off"
      puts $fd ""
    }
    puts $fd "# Logdatei"
    puts $fd "logfile /var/log/email.log"
    puts $fd ""
    puts $fd "# SMTP Account"
    puts $fd "account provider"
    puts $fd "host $account(Server)"
    puts $fd "from $account(From)"
### > Domain erzeugt Fehler z.B. bei GMX 
### if [regexp {@([^@]*)$} $account(From) dummy domain] { puts $fd "domain $domain" }
    puts $fd "auth $account(Auth)"
    puts $fd "user $account(Username)"
    puts $fd "password $account(Password)"
	puts $fd "port $account(Port)"
    puts $fd ""
    puts $fd "# Standard Account"
    puts $fd "account default: provider"

    close $fd
  }
  
  ##
  # @fn __saveUserScript
  # @brief Speichert das benutzerdefinierte Tcl-Skript.
  #
  # Es werden keine Header ausgewertet. Der Inhalt wird als das 
  # benutzerdefinierte Tcl-Skript interpretiert.
  ##
  proc __saveUserScript { } {
    global USER_SCRIPT_FILE
    
    saveToFile $USER_SCRIPT_FILE [__args_get Content]
  }
  
  ##############################################################################
  # Einsprungpunkt                                                             #
  ##############################################################################
  
  __args_init

  switch -exact -- [__args_get Query] {
    mail       { __saveMail }
    account    { __saveAccount }
    userScript { __saveUserScript }
    default    { error "Unknown Command [__args_get Query]" }
  }
  
  puts -nonewline "OK"

  } errorMessage] } then {
    puts -nonewline "ERROR $errorMessage"
  }
} else {
  puts -nonewline "ERROR: no valid session"
}
