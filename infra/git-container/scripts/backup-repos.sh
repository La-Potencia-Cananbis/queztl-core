#!/bin/bash
# Backup all Git repositories

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Backing up Git repositories..."
echo "Backup location: $BACKUP_DIR"

# Backup Gitea data
docker exec queztl-git tar czf - /data/git/repositories 2>/dev/null | tar xzf - -C "$BACKUP_DIR"

# Backup database
docker exec queztl-git-db pg_dump -U gitea gitea > "$BACKUP_DIR/database.sql"

# Create manifest
cat > "$BACKUP_DIR/manifest.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "gitea_version": "$(docker exec queztl-git gitea --version | head -1)",
  "database": "postgres",
  "files": [
    "data/git/repositories",
    "database.sql"
  ]
}
EOF

echo "✅ Backup complete: $BACKUP_DIR"
echo "Size: $(du -sh $BACKUP_DIR | cut -f1)"
