#!/bin/sh

# Backup Verzeichnis
BACKUP=/usr/local/etc/config/addons/email/backup

# Zu kopierende Files/Folder
MAIL_DIR=/usr/local/etc/config/addons/email/mails
MSMTP_CONF=/usr/local/etc/config/addons/email/msmtp.conf
ACCOUNT_CONF=/usr/local/etc/config/addons/email/account.conf
USER_SCRIPT=/usr/local/etc/config/addons/email/userscript.tcl

# Files/Folder nach Backup kopieren
cp -p -R $MAIL_DIR $BACKUP
cp -p -R $MSMTP_CONF $BACKUP
cp -p -R $ACCOUNT_CONF $BACKUP
cp -p -R $USER_SCRIPT $BACKUP

# Backup erstellen
cd /usr/local/etc/config/addons/email/backup
tar -czf /usr/local/etc/config/addons/email/email-backup.tar.gz *
chmod 644 /usr/local/etc/config/addons/email/email-backup.tar.gz

# Datum anhängen
#datum=$(date +'%d-%m-%Y')
#mv /usr/local/etc/config/addons/email/backuptmp/email-backup.tar.gz /usr/local/etc/config/addons/email/backuptmp/email-backup-$datum.tar.gz

# Aufräumen
rm -r $BACKUP/mails
rm -r $BACKUP/msmtp.conf
rm -r $BACKUP/account.conf
rm -r $BACKUP/userscript.tcl

sync