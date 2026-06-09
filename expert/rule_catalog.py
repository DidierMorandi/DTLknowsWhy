RULE_CATEGORIES = [
    {
        "id": "network_discovery",
        "title_key": "rule_category_network_discovery",
        "rules": [
            {
                "id": "SMB-001",
                "title_key": "rule_smb_001_title",
                "description_key": "rule_smb_001_desc",
                "requires_target": False,
            },
            {
                "id": "SMB-001-INFO",
                "title_key": "rule_smb_001_info_title",
                "description_key": "rule_smb_001_info_desc",
                "requires_target": False,
            },
            {
                "id": "SMB-002",
                "title_key": "rule_smb_002_title",
                "description_key": "rule_smb_002_desc",
                "requires_target": True,
            },
            {
                "id": "RÈGLE-003",
                "title_key": "rule_003_title",
                "description_key": "rule_003_desc",
                "requires_target": False,
            },
        ],
    },
    {
        "id": "smb_authentication",
        "title_key": "rule_category_smb_authentication",
        "rules": [
            {
                "id": "RÈGLE-005-006-014",
                "title_key": "rule_005_006_014_title",
                "description_key": "rule_005_006_014_desc",
                "requires_target": True,
            },
            {
                "id": "RÈGLE-007-STRICT",
                "title_key": "rule_007_strict_title",
                "description_key": "rule_007_strict_desc",
                "requires_target": False,
            },
            {
                "id": "RÈGLE-007-WEAK",
                "title_key": "rule_007_weak_title",
                "description_key": "rule_007_weak_desc",
                "requires_target": False,
            },
            {
                "id": "RÈGLE-007-INFO",
                "title_key": "rule_007_info_title",
                "description_key": "rule_007_info_desc",
                "requires_target": False,
            },
        ],
    },
    {
        "id": "remote_target",
        "title_key": "rule_category_remote_target",
        "rules": [
            {
                "id": "RÈGLE-008-013",
                "title_key": "rule_008_013_title",
                "description_key": "rule_008_013_desc",
                "requires_target": True,
            },
            {
                "id": "RÈGLE-009",
                "title_key": "rule_009_title",
                "description_key": "rule_009_desc",
                "requires_target": True,
            },
            {
                "id": "RÈGLE-010",
                "title_key": "rule_010_title",
                "description_key": "rule_010_desc",
                "requires_target": True,
            },
            {
                "id": "RÈGLE-011",
                "title_key": "rule_011_title",
                "description_key": "rule_011_desc",
                "requires_target": True,
            },
            {
                "id": "RÈGLE-016",
                "title_key": "rule_016_title",
                "description_key": "rule_016_desc",
                "requires_target": True,
            },
        ],
    },
    {
        "id": "system_security",
        "title_key": "rule_category_system_security",
        "rules": [
            {
                "id": "RÈGLE-012",
                "title_key": "rule_012_title",
                "description_key": "rule_012_desc",
                "requires_target": False,
            },
            {
                "id": "RÈGLE-015",
                "title_key": "rule_015_title",
                "description_key": "rule_015_desc",
                "requires_target": False,
            },
        ],
    },
]


RULES = [
    rule
    for category in RULE_CATEGORIES
    for rule in category["rules"]
]


def all_rule_ids():
    return [rule["id"] for rule in RULES]
