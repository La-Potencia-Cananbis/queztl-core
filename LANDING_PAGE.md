# Quetzal-Core Landing Page

## Overview
Investor-focused landing page showcasing Quetzal-Core's quantum-inspired geospatial AI technology.

## Location
- **File:** `index.html` (repository root)
- **Deployment:** AWS Amplify
- **Configuration:** `amplify.yml`

## Features
- **Hero Section:** Animated agent network visualization with "Quantum AI for Earth" headline
- **Technology Overview:** 6 detailed capability cards
- **Features Showcase:** ROI, speed, accuracy metrics
- **Mission Statement:** Startup story and credentials
- **Investor CTA:** Prominent contact section with founder email

## Contact
**Founder Email:** salvadorsena@live.com

## Navigation Links
- About → `#about`
- Technology → `#technology`
- Features → `#features`
- API Docs → `/backend/README.md`
- Whitepaper → `/backend/SENASAITECH_PITCH_DECK.md`
- Contact → `#contact`

## Design Elements
- **Color Scheme:** Cyan (#00d9ff), Purple (#8b5cf6), Orange (#f59e0b)
- **Typography:** System fonts with gradient headers
- **Animation:** Canvas-based agent network with 50 nodes
- **Responsive:** Mobile-first design with hamburger menu

## Deployment
1. Push to main branch
2. AWS Amplify auto-deploys using `amplify.yml` configuration
3. Mobile app builds from `mobile-app/apps/web/dist`
4. Uses pnpm for dependency management

## Technical Details
- Pure HTML/CSS/JavaScript
- No external dependencies
- Canvas API for animations
- CSS Grid and Flexbox for layout
- Smooth scroll navigation
- Mobile responsive (375px breakpoint)

## Testing
Tested on:
- Desktop browsers (Chrome, Firefox, Safari)
- Mobile viewport (375x667)
- Navigation functionality
- Email links
- Responsive behavior

## Last Updated
January 1, 2026
