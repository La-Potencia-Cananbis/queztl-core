#!/usr/bin/env python3
"""
Chicano & Black Liberation Movement Research
La Raza Unida, Brown Berets, Black Panthers, and allied organizations
"""

CHICANO_LIBERATION = {
    "la_raza_unida": {
        "name": "La Raza Unida Party",
        "founded": 1970,
        "location": "Texas, Southwest US",
        "key_figures": ["José Ángel Gutiérrez", "Rodolfo 'Corky' Gonzales", "Reies López Tijerina"],
        "focus": [
            "Chicano self-determination",
            "Educational reform",
            "Land rights",
            "Political representation",
            "Cultural autonomy",
            "Worker rights"
        ],
        "tactics": [
            "Third party electoral politics",
            "Community organizing",
            "School walkouts",
            "Land grant struggles",
            "Cultural resistance"
        ],
        "key_concepts": [
            "Aztlán (ancestral homeland)",
            "Chicanismo",
            "Cultural nationalism",
            "Self-determination"
        ]
    },
    "brown_berets": {
        "name": "Brown Berets",
        "founded": 1967,
        "location": "Los Angeles, Southwest US",
        "key_figures": ["David Sánchez", "Carlos Montes", "Gloria Arellanes"],
        "focus": [
            "Police brutality opposition",
            "Educational equality",
            "Anti-war (Vietnam)",
            "Community defense",
            "Health clinics",
            "Free breakfast programs"
        ],
        "tactics": [
            "Community patrols",
            "Direct action",
            "Mutual aid programs",
            "Coalition building",
            "Cultural education",
            "Self-defense training"
        ],
        "parallels": "Inspired by Black Panthers, adapted to Chicano liberation",
        "legacy": "Reformed 1990s, continues organizing today"
    }
}

BLACK_LIBERATION = {
    "black_panther_party": {
        "name": "Black Panther Party for Self-Defense",
        "founded": 1966,
        "location": "Oakland, CA (national expansion)",
        "key_figures": [
            "Huey P. Newton",
            "Bobby Seale", 
            "Eldridge Cleaver",
            "Fred Hampton",
            "Kathleen Cleaver",
            "Angela Davis",
            "Assata Shakur"
        ],
        "ten_point_program": [
            "Freedom & power to determine destiny",
            "Full employment",
            "End to robbery of Black community",
            "Decent housing",
            "Education for real history",
            "Free health care",
            "End police brutality",
            "End all wars of aggression",
            "Freedom for political prisoners",
            "Land, bread, housing, education, clothing, justice, peace"
        ],
        "survival_programs": [
            "Free Breakfast for Children",
            "Free health clinics",
            "Liberation schools",
            "Free clothing program",
            "Sickle cell anemia testing",
            "Free ambulance service",
            "Free pest control",
            "Free legal aid"
        ],
        "tactics": [
            "Armed self-defense (legal open carry)",
            "Community patrols (Copwatching)",
            "Political education classes",
            "Coalition building",
            "International solidarity",
            "Revolutionary journalism (The Black Panther paper)"
        ],
        "key_concepts": [
            "Revolutionary intercommunalism",
            "Serve the people",
            "All power to the people",
            "Self-determination",
            "Community control"
        ]
    }
}

MODERN_ALLIES = {
    "democratic_socialists": {
        "DSA": {
            "focus": ["Electoral socialism", "Medicare for All", "Housing justice", "Labor solidarity"],
            "working_groups": ["Ecosocialism", "Labor", "Medicare for All", "Housing justice"]
        }
    },
    "immigrant_rights": {
        "groups": [
            "Mijente (Latinx organizing)",
            "United We Dream (undocumented youth)",
            "NDLON (National Day Laborer Organizing Network)",
            "Cosecha Movement (non-cooperation tactics)"
        ]
    },
    "black_liberation_modern": {
        "groups": [
            "Black Lives Matter (decentralized)",
            "Movement for Black Lives (M4BL coalition)",
            "Black Youth Project 100 (BYP100)",
            "Dream Defenders",
            "Malcolm X Grassroots Movement"
        ],
        "demands": [
            "Defund/abolish police",
            "Reparations",
            "Community control",
            "Economic justice",
            "Political power"
        ]
    },
    "indigenous_sovereignty": {
        "groups": [
            "Indigenous Environmental Network",
            "NDN Collective",
            "Red Nation (indigenous Marxists)",
            "Land Back movement"
        ]
    },
    "labor_organizing": {
        "groups": [
            "United Electrical Workers (UE - independent)",
            "Emergency Workplace Organizing Committee (EWOC)",
            "Amazon Labor Union",
            "Starbucks Workers United",
            "Railroad Workers United"
        ]
    },
    "anti_imperialist": {
        "groups": [
            "ANSWER Coalition",
            "Black Alliance for Peace",
            "Veterans For Peace",
            "CodePink"
        ]
    }
}

def print_movement_data():
    print("🚩 CHICANO & BLACK LIBERATION MOVEMENTS")
    print("=" * 70)
    
    print("\n✊🏽 LA RAZA UNIDA PARTY")
    print("-" * 70)
    lru = CHICANO_LIBERATION["la_raza_unida"]
    print(f"Founded: {lru['founded']}")
    print(f"Key Figures: {', '.join(lru['key_figures'])}")
    print("\nFocus Areas:")
    for focus in lru['focus']:
        print(f"  • {focus}")
    print("\nTactics:")
    for tactic in lru['tactics']:
        print(f"  • {tactic}")
    
    print("\n\n🐻 BROWN BERETS")
    print("-" * 70)
    bb = CHICANO_LIBERATION["brown_berets"]
    print(f"Founded: {bb['founded']}")
    print(f"Key Figures: {', '.join(bb['key_figures'])}")
    print("\nCommunity Programs:")
    for focus in bb['focus']:
        print(f"  • {focus}")
    print("\nTactics:")
    for tactic in bb['tactics']:
        print(f"  • {tactic}")
    
    print("\n\n🐾 BLACK PANTHER PARTY")
    print("-" * 70)
    bpp = BLACK_LIBERATION["black_panther_party"]
    print(f"Founded: {bpp['founded']}")
    print(f"Location: {bpp['location']}")
    print("\nKey Figures:")
    for figure in bpp['key_figures']:
        print(f"  • {figure}")
    
    print("\n📋 10-POINT PROGRAM:")
    for i, point in enumerate(bpp['ten_point_program'], 1):
        print(f"  {i}. {point}")
    
    print("\n🍳 SURVIVAL PROGRAMS (Serve the People):")
    for program in bpp['survival_programs']:
        print(f"  • {program}")
    
    print("\n⚡ REVOLUTIONARY TACTICS:")
    for tactic in bpp['tactics']:
        print(f"  • {tactic}")
    
    print("\n\n🤝 MODERN ALLIED ORGANIZATIONS (2026)")
    print("=" * 70)
    
    print("\n🌹 Socialist Organizations:")
    print("  • PSL (Party for Socialism and Liberation)")
    print("  • DSA (Democratic Socialists of America)")
    print("  • FRSO (Freedom Road Socialist Organization)")
    
    print("\n✊🏿 Black Liberation:")
    for group in MODERN_ALLIES['black_liberation_modern']['groups']:
        print(f"  • {group}")
    
    print("\n✊🏽 Immigrant Rights:")
    for group in MODERN_ALLIES['immigrant_rights']['groups']:
        print(f"  • {group}")
    
    print("\n🪶 Indigenous Sovereignty:")
    for group in MODERN_ALLIES['indigenous_sovereignty']['groups']:
        print(f"  • {group}")
    
    print("\n⚒️  Labor Organizing:")
    for group in MODERN_ALLIES['labor_organizing']['groups']:
        print(f"  • {group}")
    
    print("\n🌍 Anti-Imperialism:")
    for group in MODERN_ALLIES['anti_imperialist']['groups']:
        print(f"  • {group}")
    
    print("\n\n" + "=" * 70)
    print("✓ Liberation movements catalogued")
    print("✓ Coalition building opportunities identified")
    print("✓ Historical tactics documented for study")

if __name__ == "__main__":
    print_movement_data()
