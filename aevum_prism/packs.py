"""
Lumenfall pack simulation with rarity chances, pity system, and lifetime logging.
"""

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from aevum_prism.instances import ELEMENTS, InstanceStore, get_max_tier

CardPool = Dict[str, Sequence[str]]
Pull = Tuple[str, str]

# Rarity configuration (chances sum ~1.0 for standard pulls).
RARITIES = [
    {"name": "Common", "chance": 0.60, "pity": False},
    {"name": "Uncommon", "chance": 0.25, "pity": False},
    {"name": "Rare", "chance": 0.10, "pity": False},
    {"name": "Epic", "chance": 0.039, "pity": True},
    {"name": "Legendary", "chance": 0.001, "pity": True},
    {"name": "Mythic", "chance": 0.00001, "pity": True},
    {"name": "Secret", "chance": 0.000001, "pity": False},
    {"name": "Astral", "chance": 0.0000001, "pity": False},
    {"name": "Divine", "chance": 0.0000005, "pity": False},
]

# Card pools by rarity.
CARD_POOL: CardPool = {
    "Common": [f"Common_{i+1:03d}" for i in range(150)],
    "Uncommon": [f"Uncommon_{i+1:02d}" for i in range(100)],
    "Rare": [f"Rare_{i+1:02d}" for i in range(60)],
    "Epic": [f"Epic_{i+1:02d}" for i in range(30)],
    "Legendary": [f"Legendary_{i+1:02d}" for i in range(10)],
    "Mythic": [f"Mythic_{i+1:02d}" for i in range(5)],
    "Secret": [f"Secret_{i+1:02d}" for i in range(3)],
    "Astral": [f"Astral_{i+1:02d}" for i in range(2)],
    "Divine": ["Aevum's Prism"],
}

# Pity thresholds (counts of pulls without that rarity).
PITY_THRESHOLDS = {
    "Epic": 200,
    "Legendary": 2000,
    "Mythic": 200_000,
}

PACK_SIZE = 5  # default; adjust when simulating boxes/events as needed.

# Paths
SUMMARY_PATH = Path("logs/pulls_summary.log")
TOTAL_PACKS_PATH = Path("logs/packs_total.txt")
RARITY_TOTALS_PATH = Path("logs/rarity_totals.json")
PITY_STATE_PATH = Path("logs/pity_state.json")


def ensure_log_dir() -> None:
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def read_rarity_totals() -> Dict[str, int]:
    data = read_json(RARITY_TOTALS_PATH, {})
    return {r: int(data.get(r, 0)) for r in CARD_POOL.keys()}


def write_rarity_totals(totals: Dict[str, int]) -> None:
    ensure_log_dir()
    RARITY_TOTALS_PATH.write_text(json.dumps(totals, indent=2), encoding="utf-8")


def read_total_packs() -> int:
    if TOTAL_PACKS_PATH.exists():
        try:
            return int(TOTAL_PACKS_PATH.read_text(encoding="utf-8").strip() or "0")
        except ValueError:
            return 0
    return 0


def write_total_packs(total: int) -> None:
    TOTAL_PACKS_PATH.write_text(str(total), encoding="utf-8")


def read_pity_state() -> Dict[str, int]:
    data = read_json(PITY_STATE_PATH, {})
    return {k: int(data.get(k, 0)) for k in PITY_THRESHOLDS.keys()}


def write_pity_state(state: Dict[str, int]) -> None:
    ensure_log_dir()
    PITY_STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def roll_secret_rare(rng: random.Random) -> None:
    """
    Placeholder for future secret rare logic.
    """
    return None


def roll_slot(rng: random.Random, pity_state: Dict[str, int]) -> Pull:
    """
    Roll a single card slot. Returns (card_name, rarity).
    """
    # Pity check from highest to lowest.
    for rarity in ["Mythic", "Legendary", "Epic"]:
        if pity_state.get(rarity, 0) >= PITY_THRESHOLDS[rarity]:
            card = rng.choice(CARD_POOL[rarity])
            return card, rarity

    # Normal roll by chance.
    roll = rng.random()
    cumulative = 0.0
    for rarity in RARITIES:
        cumulative += rarity["chance"]
        if roll < cumulative:
            name = rarity["name"]
            if name == "Secret":
                roll_secret_rare(rng)
            card = rng.choice(CARD_POOL[name])
            return card, name

    # Fallback
    card = rng.choice(CARD_POOL["Common"])
    return card, "Common"


def open_pack(rng: random.Random | None = None) -> List[Pull]:
    """
    Simulate opening a pack and return list of (card_name, rarity).
    """
    r = rng if rng is not None else random
    pity_state = read_pity_state()
    pack: List[Pull] = []
    inst_store = InstanceStore()

    for _ in range(PACK_SIZE):
        card, rarity = roll_slot(r, pity_state)
        pack.append((card, rarity))
        max_tier = get_max_tier(rarity)
        if rarity in {"Common", "Uncommon"}:
            tier = 0
        elif rarity == "Divine":
            tier = max_tier
        else:
            tier = min(1, max_tier)
        element = r.choice(ELEMENTS)
        inst_store.add_instance(card_id=card, rarity=rarity, tier=tier, element=element, charges=None, locked=False)
        # Update pity counters
        for pity_rarity in PITY_THRESHOLDS.keys():
            if rarity == pity_rarity:
                pity_state[pity_rarity] = 0
            else:
                pity_state[pity_rarity] = pity_state.get(pity_rarity, 0) + 1

    write_pity_state(pity_state)
    return pack


def format_pull(card: str, rarity: str) -> str:
    if rarity == "Divine":
        return f"{card} - {rarity} (5★)"
    if rarity in {"Secret", "Astral"}:
        return f"{card} - {rarity} (???)"
    return f"{card} - {rarity}"


def print_pack(pack: List[Pull]) -> None:
    print("Opening a pack!")
    print("-----------------")
    for card, rarity in pack:
        line = format_pull(card, rarity)
        print(line)
        if rarity == "Divine":
            print(">> AEVUM'S PRISM PULLED! << ミ.ミ.ミ.ミ.ミ.")
    print("-----------------")


def write_summary(packs_opened: int, rarity_counts: Counter[str]) -> None:
    ensure_log_dir()
    lifetime_packs = read_total_packs() + packs_opened
    write_total_packs(lifetime_packs)

    lifetime_rarity = read_rarity_totals()
    for rarity, count in rarity_counts.items():
        lifetime_rarity[rarity] = lifetime_rarity.get(rarity, 0) + count
    write_rarity_totals(lifetime_rarity)
    lifetime_cards = sum(lifetime_rarity.values())

    lines = []
    lines.append("----------------------")
    lines.append(f"Packs opened (this run): {packs_opened}")
    lines.append(f"Packs opened (lifetime): {lifetime_packs}")
    lines.append(f"Cards pulled (this run): {sum(rarity_counts.values())}")
    lines.append(f"Cards pulled (lifetime): {lifetime_cards}")
    lines.append("This run:")
    for rarity in CARD_POOL.keys():
        lines.append(f"- {rarity}: {rarity_counts.get(rarity, 0)}")
    lines.append("Lifetime totals:")
    for rarity in CARD_POOL.keys():
        lines.append(f"- {rarity}: {lifetime_rarity.get(rarity, 0)}")
    lines.append("----------------------")

    summary = "\n".join(lines)
    with SUMMARY_PATH.open("w", encoding="utf-8") as f:
        f.write(summary + "\n")
    print(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate opening Lumenfall card packs.")
    parser.add_argument(
        "--packs",
        type=int,
        default=1,
        help="Number of packs to open (default: 1).",
    )
    args = parser.parse_args()

    rng = random.Random()
    rarity_counts: Counter[str] = Counter()

    for _ in range(args.packs):
        pack = open_pack(rng)
        if args.packs == 1:
            print_pack(pack)
        for _, rarity in pack:
            rarity_counts[rarity] += 1

    write_summary(args.packs, rarity_counts)
