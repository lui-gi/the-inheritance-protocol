#!/bin/sh
# Nightly backup, run by cron as svc-backup.
set -e
STAMP=$(date +%Y-%m-%d)
tar -czf "/var/backups/hub-$STAMP.tar.gz" /opt/blackthorn-hub/config.yaml /var/log
echo "$(date -Iseconds) backup ok hub-$STAMP.tar.gz" >> /var/log/backup.log
find /var/backups -name 'hub-*.tar.gz' -mtime +14 -delete
