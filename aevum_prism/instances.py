"""
Card instance and essence persistence utilities.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

ELEMENTS = ["Fire", "Ice", "Nature", "Light", "Void", "Metal", "Arcane", "Astral"]


MAX_TIER_BY_RARITY: Dict[str, int] = {
    "Common": 0,
    "Uncommon": 0,
    "Rare": 5,
    "Epic": 5,
    "Legendary": 5,
    "Mythic": 5,
    "Secret": 5,
    "Astral": 8,
    "Divine": 5,
}


def get_max_tier(rarity: str) -> int:
    return MAX_TIER_BY_RARITY.get(rarity, 0)


class InstanceStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path("saves/card_instances.json")
        self.data: Dict[str, object] = {"instances": [], "essence": {r: 0 for r in MAX_TIER_BY_RARITY.keys()}}
        self._ensure_dir()
        self._load()

    def _ensure_dir(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        if not self.path.exists():
            self._save()
            return
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                self.data["instances"] = loaded.get("instances", [])
                essence = loaded.get("essence", {})
                self.data["essence"] = {r: int(essence.get(r, 0)) for r in MAX_TIER_BY_RARITY.keys()}
        except Exception:
            # Keep defaults on error.
            pass

    def _save(self) -> None:
        self._ensure_dir()
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def add_instance(
        self,
        card_id: str,
        rarity: str,
        tier: int,
        element: str,
        charges: Optional[int] = None,
        locked: bool = False,
    ) -> Dict[str, object]:
        inst = {
            "instance_id": str(uuid.uuid4()),
            "card_id": card_id,
            "rarity": rarity,
            "tier": int(tier),
            "element": element,
            "charges": charges,
            "locked": bool(locked),
        }
        self.data["instances"].append(inst)
        self._save()
        return inst

    def instances_for_card(self, card_id: str) -> List[Dict[str, object]]:
        return [inst for inst in self.data.get("instances", []) if inst.get("card_id") == card_id]

    def toggle_lock(self, instance_id: str, locked: bool) -> None:
        for inst in self.data.get("instances", []):
            if inst.get("instance_id") == instance_id:
                inst["locked"] = bool(locked)
                break
        self._save()

    def exchange_instance(self, instance_id: str, collection) -> int:
        """Exchange an instance for essence; removes from collection and returns essence gained."""
        instances = self.data.get("instances", [])
        for idx, inst in enumerate(instances):
            if inst.get("instance_id") == instance_id:
                rarity = inst.get("rarity")
                tier = int(inst.get("tier", 0))
                card_id = inst.get("card_id")
                if rarity not in self.data["essence"]:
                    return 0
                if tier < 2:
                    return 0
                self.data["essence"][rarity] += tier
                instances.pop(idx)
                if hasattr(collection, "remove_card"):
                    collection.remove_card(rarity, card_id, count=1)
                self._save()
                return tier
        return 0

    def record_wither(self, instance_id: str, collection) -> None:
        """Remove instance when it withers (charges drop to 0)."""
        instances = self.data.get("instances", [])
        for idx, inst in enumerate(instances):
            if inst.get("instance_id") == instance_id:
                card_id = inst.get("card_id")
                rarity = inst.get("rarity")
                instances.pop(idx)
                if hasattr(collection, "remove_card"):
                    collection.remove_card(rarity, card_id, count=1)
                self._save()
                return

