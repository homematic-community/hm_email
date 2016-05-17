#!/bin/sh
mkdir -p tmp
cp -a account.conf tmp/
cp -a addon tmp/
cp -a ccu1 tmp/
cp -a ccu2 tmp/
cp -a ccupi tmp/
cp -a email tmp/
cp -a mails tmp/
cp -a msmtp.conf tmp/
cp -a update_script tmp/
cp -a userscript.tcl tmp/
cp -a www tmp/
cp -a VERSION tmp/addon/
cd tmp
tar --owner=root --group=root -czvf ../email-$(cat ../VERSION).tar.gz *
cd ..
rm -rf tmp
