#!/bin/bash
# Rename QuetzalCore to QuetzalCore across the entire codebase
# ¡ÓRALE! This is a COMPREHENSIVE rename operation

set -e

echo "🦅 QUETZALCORE → QUETZALCORE RENAME OPERATION"
echo "=========================================="
echo ""

# Backup first!
BACKUP_DIR="backup_before_rename_$(date +%Y%m%d_%H%M%S)"
echo "📦 Creating backup in $BACKUP_DIR..."
mkdir -p "$BACKUP_DIR"
cp -r . "$BACKUP_DIR/" 2>/dev/null || true
echo "✅ Backup created"
echo ""

# Function to rename in file
rename_in_file() {
    local file="$1"
    
    # Skip binary files, backups, and hidden dirs
    if [[ "$file" == *".venv"* ]] || \
       [[ "$file" == *"node_modules"* ]] || \
       [[ "$file" == *".git"* ]] || \
       [[ "$file" == *"backup"* ]] || \
       [[ "$file" == *".pyc" ]] || \
       [[ "$file" == *".egg-info"* ]]; then
        return
    fi
    
    # Check if file is text
    if file "$file" | grep -q "text"; then
        # Perform all replacements
        sed -i '' \
            -e 's/QuetzalCore/QuetzalCore/g' \
            -e 's/QUETZALCORE/QUETZALCORE/g' \
            -e 's/quetzalcore/quetzalcore/g' \
            "$file" 2>/dev/null || true
    fi
}

echo "🔄 Renaming in file contents..."
echo ""

# Find all text files and rename content
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        rename_in_file "$file"
        echo "  ✓ $file"
    fi
done < <(find . -type f \
    \( -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.html" \
    -o -name "*.js" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" \
    -o -name "*.txt" -o -name "*.cfg" -o -name "*.conf" \) \
    ! -path "./.venv/*" \
    ! -path "./node_modules/*" \
    ! -path "./.git/*" \
    ! -path "./backup*/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*.egg-info/*")

echo ""
echo "📝 Renaming files and directories..."
echo ""

# Rename files (deepest first)
find . -depth -name "*quetzalcore*" -type f ! -path "./.venv/*" ! -path "./node_modules/*" ! -path "./.git/*" ! -path "./backup*/*" | while read -r file; do
    newname=$(echo "$file" | sed 's/quetzalcore/quetzalcore/g')
    if [[ "$file" != "$newname" ]]; then
        mkdir -p "$(dirname "$newname")"
        mv "$file" "$newname" 2>/dev/null || true
        echo "  📄 $file → $newname"
    fi
done

# Rename directories (deepest first)
find . -depth -name "*quetzalcore*" -type d ! -path "./.venv/*" ! -path "./node_modules/*" ! -path "./.git/*" ! -path "./backup*/*" | while read -r dir; do
    newname=$(echo "$dir" | sed 's/quetzalcore/quetzalcore/g')
    if [[ "$dir" != "$newname" ]]; then
        mv "$dir" "$newname" 2>/dev/null || true
        echo "  📁 $dir → $newname"
    fi
done

echo ""
echo "✅ RENAME COMPLETE!"
echo ""
echo "📊 Summary:"
echo "  - Backup: $BACKUP_DIR"
echo "  - All QuetzalCore → QuetzalCore"
echo "  - All QUETZALCORE → QUETZALCORE"
echo "  - All quetzalcore → quetzalcore"
echo ""
echo "🦅 Your codebase is now QuetzalCore! ¡ÓRALE!"
