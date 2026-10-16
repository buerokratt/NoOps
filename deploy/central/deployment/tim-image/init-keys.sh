#!/bin/sh
set -eu
umask 077
mkdir -p /keys
if [ -f /keys/jwtkeystore.jks ]; then
  keytool -list -alias jwtsign -keystore /keys/jwtkeystore.jks -storepass:file /run/keypass >/dev/null 2>&1
  test -f /keys/initialized
  sha256sum -c /keys/initialized >/dev/null 2>&1
  exit 0
fi
# Never replace a partial/unknown keystore or a completed installation.
test ! -e /keys/initialized
test ! -e /keys/jwtkeystore.tmp
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 3072 -storetype JKS -keystore /keys/jwtkeystore.tmp -dname 'CN=central-byk-test JWT signer' -storepass:file /run/keypass -keypass:file /run/keypass -validity 3650 >/dev/null 2>&1
mv /keys/jwtkeystore.tmp /keys/jwtkeystore.jks
sha256sum /keys/jwtkeystore.jks > /keys/initialized
