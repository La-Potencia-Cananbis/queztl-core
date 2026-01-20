#!/usr/bin/env python3
"""
PSL Research & Integration Module
Study Party for Socialism and Liberation resources
"""

# PSL Resources to study and integrate
PSL_RESOURCES = {
    "liberation_school": {
        "name": "Liberation School",
        "url": "https://liberationschool.org",
        "topics": [
            "Marxist economics",
            "Anti-imperialism",
            "Black liberation",
            "Women's liberation",
            "LGBTQ+ rights",
            "Labor organizing",
            "Revolutionary strategy"
        ],
        "priority": "high"
    },
    "breaking_the_chains": {
        "name": "Breaking the Chains Magazine",
        "topics": [
            "Current struggles",
            "Revolutionary analysis",
            "Workers' rights",
            "Anti-war movement"
        ],
        "priority": "high"
    },
    "psl_program": {
        "name": "PSL Program",
        "url": "https://pslweb.org/program",
        "topics": [
            "Socialist reconstruction",
            "Democratic rights",
            "International solidarity",
            "Environmental justice"
        ],
        "priority": "essential"
    },
    "key_texts": [
        "Imperialism in the 21st Century",
        "The Struggle for Socialism in the United States",
        "Marxism and the Revolutionary Party",
        "National Liberation and Socialism",
        "Women and Socialism",
        "Racism, National Oppression and Self-Determination"
    ]
}

# Networking & Organizing Focus
PSL_ORGANIZING = {
    "campaigns": [
        "Anti-war movement",
        "Housing rights (Homes Guarantee)",
        "Palestinian solidarity",
        "Cuba solidarity",
        "Workers' rights",
        "Police abolition"
    ],
    "study_groups": [
        "Marxism 101",
        "Imperialism studies",
        "Revolutionary history",
        "Current events analysis"
    ],
    "alliance_building": [
        "Labor unions",
        "Community organizations",
        "Student movements",
        "International solidarity groups"
    ]
}

def integrate_psl_content():
    """Add PSL resources to theory library"""
    print("🚩 PSL RESEARCH MODULE")
    print("=" * 60)
    print("Party for Socialism and Liberation")
    print("Revolutionary Marxist organization")
    print()
    
    print("📚 Key Resources:")
    for key, resource in PSL_RESOURCES.items():
        if isinstance(resource, dict):
            print(f"\n  • {resource['name']}")
            if 'url' in resource:
                print(f"    URL: {resource['url']}")
            print(f"    Priority: {resource.get('priority', 'normal').upper()}")
            if 'topics' in resource:
                print(f"    Topics: {', '.join(resource['topics'][:3])}...")
    
    print("\n\n🔥 Current Campaigns:")
    for campaign in PSL_ORGANIZING['campaigns']:
        print(f"  • {campaign}")
    
    print("\n\n📖 Study Groups:")
    for group in PSL_ORGANIZING['study_groups']:
        print(f"  • {group}")
    
    print("\n\n🤝 Alliance Building:")
    for alliance in PSL_ORGANIZING['alliance_building']:
        print(f"  • {alliance}")
    
    print("\n" + "=" * 60)
    print("✓ PSL resources catalogued")
    print("✓ Ready for AI training integration")
    print("✓ Networking opportunities identified")

if __name__ == "__main__":
    integrate_psl_content()
