#!/bin/bash
# Version Management Script
# Script de Gestión de Versiones
#
# Copyright (c) 2025 Queztl-Core Project
# CONFIDENTIAL - PATENT PENDING

set -e

VERSION_FILE="VERSION"
CURRENT_VERSION=$(cat "$VERSION_FILE" 2>/dev/null || echo "1.0.0")

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

show_help() {
    cat << EOF
╔══════════════════════════════════════════════════════════════╗
║         VERSION MANAGEMENT - GESTIÓN DE VERSIONES            ║
╚══════════════════════════════════════════════════════════════╝

Usage / Uso:
  ./version.sh <command> [options]

Commands / Comandos:

  current             Show current version / Mostrar versión actual
  
  bump <type>         Bump version number / Incrementar número versión
                      Types: major, minor, patch
                      
  tag                 Create git tag for current version
                      Crear etiqueta git para versión actual
                      
  release <version>   Create full release / Crear lanzamiento completo
                      Example: ./version.sh release 1.1.0
                      
  list                List all versions / Listar todas versiones
  
  check               Check version consistency / Verificar consistencia versión

Examples / Ejemplos:

  # Show current version
  ./version.sh current

  # Bump patch version (1.0.0 → 1.0.1)
  ./version.sh bump patch

  # Bump minor version (1.0.0 → 1.1.0)
  ./version.sh bump minor

  # Bump major version (1.0.0 → 2.0.0)
  ./version.sh bump major

  # Create release
  ./version.sh release 1.1.0

  # List all versions
  ./version.sh list

🔒 CONFIDENTIAL - PATENT PENDING
EOF
}

get_version_parts() {
    local version=$1
    IFS='.' read -r major minor patch <<< "$version"
    echo "$major $minor $patch"
}

bump_version() {
    local bump_type=$1
    local parts=($(get_version_parts "$CURRENT_VERSION"))
    local major=${parts[0]}
    local minor=${parts[1]}
    local patch=${parts[2]}
    
    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo -e "${RED}Error: Invalid bump type. Use: major, minor, or patch${NC}"
            exit 1
            ;;
    esac
    
    echo "$major.$minor.$patch"
}

update_version_file() {
    local new_version=$1
    echo "$new_version" > "$VERSION_FILE"
    echo -e "${GREEN}✅ Updated VERSION file to $new_version${NC}"
}

update_changelog() {
    local new_version=$1
    local date=$(date +%Y-%m-%d)
    
    # Add new version entry to CHANGELOG.md
    sed -i.bak "s/## \[Unreleased\]/## [Unreleased]\n\n---\n\n## [$new_version] - $date/" CHANGELOG.md
    rm CHANGELOG.md.bak 2>/dev/null || true
    
    echo -e "${GREEN}✅ Updated CHANGELOG.md${NC}"
}

update_package_json() {
    local new_version=$1
    
    if [ -f dashboard/package.json ]; then
        # Update version in package.json
        sed -i.bak "s/\"version\": \".*\"/\"version\": \"$new_version\"/" dashboard/package.json
        rm dashboard/package.json.bak 2>/dev/null || true
        echo -e "${GREEN}✅ Updated dashboard/package.json${NC}"
    fi
}

create_git_tag() {
    local version=$1
    local date=$(date +%Y-%m-%d)
    
    # Commit version changes
    git add VERSION CHANGELOG.md dashboard/package.json 2>/dev/null || true
    git commit -m "chore: Bump version to $version" 2>/dev/null || true
    
    # Create annotated tag
    git tag -a "v$version" -m "Release v$version ($date)"
    
    echo -e "${GREEN}✅ Created git tag: v$version${NC}"
    echo -e "${YELLOW}   Push with: git push origin v$version${NC}"
}

create_release() {
    local new_version=$1
    
    echo -e "${BLUE}Creating release for version $new_version...${NC}"
    echo ""
    
    # Update version files
    update_version_file "$new_version"
    update_changelog "$new_version"
    update_package_json "$new_version"
    
    # Create backup
    echo -e "${BLUE}Creating pre-release backup...${NC}"
    ./backup.sh
    
    # Create git tag
    create_git_tag "$new_version"
    
    # Build Docker images
    echo -e "${BLUE}Building Docker images...${NC}"
    docker-compose build
    
    # Tag Docker images
    docker tag hive-backend:latest "hive-backend:v$new_version"
    docker tag hive-dashboard:latest "hive-dashboard:v$new_version"
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              ✅ RELEASE COMPLETE / COMPLETO                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Version / Versión: $new_version"
    echo "📅 Date / Fecha: $(date)"
    echo ""
    echo "📋 Next Steps / Próximos Pasos:"
    echo ""
    echo "  1. Push git tag / Subir etiqueta git:"
    echo "     git push origin v$new_version"
    echo "     git push origin --tags"
    echo ""
    echo "  2. Push Docker images / Subir imágenes Docker:"
    echo "     docker push hive-backend:v$new_version"
    echo "     docker push hive-dashboard:v$new_version"
    echo ""
    echo "  3. Deploy to production / Desplegar a producción:"
    echo "     ./deploy-backend.sh"
    echo ""
    echo "  4. Update documentation / Actualizar documentación:"
    echo "     - Update README.md with new features"
    echo "     - Update API_CONNECTION_GUIDE.md if APIs changed"
    echo ""
    echo "  5. Notify team / Notificar equipo:"
    echo "     - Send release notes"
    echo "     - Update status page"
    echo ""
}

check_version_consistency() {
    echo -e "${BLUE}Checking version consistency...${NC}"
    echo ""
    
    local issues=0
    
    # Check VERSION file
    if [ ! -f "$VERSION_FILE" ]; then
        echo -e "${RED}❌ VERSION file not found${NC}"
        issues=$((issues + 1))
    else
        echo -e "${GREEN}✅ VERSION file: $CURRENT_VERSION${NC}"
    fi
    
    # Check git tags
    local latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
    echo -e "${GREEN}✅ Latest git tag: $latest_tag${NC}"
    
    # Check package.json
    if [ -f dashboard/package.json ]; then
        local pkg_version=$(grep -o '"version": *"[^"]*"' dashboard/package.json | grep -o '"[0-9.]*"' | tr -d '"')
        if [ "$pkg_version" = "$CURRENT_VERSION" ]; then
            echo -e "${GREEN}✅ package.json version: $pkg_version (matches)${NC}"
        else
            echo -e "${RED}❌ package.json version: $pkg_version (does NOT match)${NC}"
            issues=$((issues + 1))
        fi
    fi
    
    # Check CHANGELOG.md
    if grep -q "\[$CURRENT_VERSION\]" CHANGELOG.md; then
        echo -e "${GREEN}✅ CHANGELOG.md contains version $CURRENT_VERSION${NC}"
    else
        echo -e "${YELLOW}⚠️  CHANGELOG.md does not contain version $CURRENT_VERSION${NC}"
    fi
    
    echo ""
    if [ $issues -eq 0 ]; then
        echo -e "${GREEN}✅ All version checks passed!${NC}"
    else
        echo -e "${RED}❌ Found $issues version inconsistencies${NC}"
        exit 1
    fi
}

list_versions() {
    echo -e "${BLUE}Version History / Historial de Versiones:${NC}"
    echo ""
    echo "Git Tags / Etiquetas Git:"
    git tag -l --sort=-version:refname | head -10
    echo ""
    echo "Releases in CHANGELOG.md:"
    grep -E "^## \[" CHANGELOG.md | head -10
}

# Main command handler
case "${1:-help}" in
    current)
        echo "Current version / Versión actual: $CURRENT_VERSION"
        ;;
    
    bump)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Specify bump type (major, minor, or patch)${NC}"
            exit 1
        fi
        NEW_VERSION=$(bump_version "$2")
        echo "Bumping $2 version: $CURRENT_VERSION → $NEW_VERSION"
        update_version_file "$NEW_VERSION"
        echo -e "${GREEN}✅ Version bumped to $NEW_VERSION${NC}"
        echo -e "${YELLOW}   Don't forget to update CHANGELOG.md${NC}"
        ;;
    
    tag)
        create_git_tag "$CURRENT_VERSION"
        ;;
    
    release)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Specify version number (e.g., 1.1.0)${NC}"
            exit 1
        fi
        create_release "$2"
        ;;
    
    list)
        list_versions
        ;;
    
    check)
        check_version_consistency
        ;;
    
    help|--help|-h)
        show_help
        ;;
    
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

exit 0
