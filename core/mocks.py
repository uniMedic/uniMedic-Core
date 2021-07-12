from hip import HealthIntelProviderLocal

full_topics = [
    "xr_elbow",
    "xr_forearm",
    "xr_hand",
    "xr_hummerus",
    "xr_shoulder",
    "xr_wrist",
    "xr_chest",
    "scan_brain",
    "scan_breast",
    "scan_eyes",
    "scan_heart",
]


def generate_mocks():
    return [
        HealthIntelProviderLocal("Hospital Solidaridad", {"vqa": ["scan_brain"]}),
        HealthIntelProviderLocal(
            "Hospital del niño",
            {"vqa": ["scan_brain", "xr_chest"], "segmentation": ["scan_brain"]},
        ),
        HealthIntelProviderLocal("Hospital Hipólito", {"vqa": ["xr_chest"]}),
        HealthIntelProviderLocal("Hospital ESSALUD", {"vqa": ["xr_chest"]}),
        HealthIntelProviderLocal(
            "Hospital Rezola", {"segmentation": ["scan_brain"]}
        ),
    ]
