##
# @file config.tcl
# @brief Konfiguration
#
# Enthält Pfade zu den einzelnen Konfigurationsdateien.
#
# @author Harima-kun
# @license Public Domain
##

##
# @var MAIL_DIR
# @brief Verzeichnis für E-Mails
##
set MAIL_DIR /etc/config/addons/email/mails

##
# @var MAIL_IDS
# @brief Ids der Mails.
#
# Die Dateinamen der Mail-Dateien setzen sich wie folgt zusammen:
#  $MAIL_DIR/$id.mail
##
set MAIL_IDS [list 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50]

##
# @var ACCOUNT_FILE
# @brief Datei für Konto-Informationen
##
set ACCOUNT_FILE /etc/config/addons/email/account.conf

##
# @var MSMTP_CONFIG_FILE
# @brief MSMTP Konfigutationsdatei
##
set MSMTP_CONFIG_FILE /etc/config/addons/email/msmtp.conf

##
# @var USER_SCRIPT_FILE
# @brief Benutzerdefinierte Script-Datei
##
set USER_SCRIPT_FILE /etc/config/addons/email/userscript.tcl
