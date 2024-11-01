from dataclasses import dataclass, field
from typing import Any, DefaultDict, Dict, Optional

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

from bot.modules.database import db


@dataclass
class MemoryStorageRecord:
    data: Dict[str, Any] = field(default_factory=dict)
    state: Optional[str] = None


class StorageDict(DefaultDict):
    def __init__(self, default_factory=None) -> None:
        if type(db.fsm.get("fsm")) is not dict:
            db.fsm["fsm"] = dict()

        super().__init__(default_factory, db.fsm["fsm"])

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        db.fsm["fsm"] = dict(self)


class InDbStorage(BaseStorage):
    def __init__(self) -> None:
        self.storage: StorageDict[StorageKey, MemoryStorageRecord] = StorageDict(
            MemoryStorageRecord
        )

    async def close(self) -> None:
        pass

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        self.storage[key].state = state.state if isinstance(state, State) else state

    async def get_state(self, key: StorageKey) -> Optional[str]:
        return self.storage[key].state

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        self.storage[key].data = data.copy()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        return self.storage[key].data.copy()
