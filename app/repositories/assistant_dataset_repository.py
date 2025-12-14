from typing import List, Dict

from sqlmodel import Session, select, delete

from app.models.assistant_dataset_model import AssistantDataset


class AssistantDatasetRepository:
    def __init__(self, session: Session):
        self.session = session

    def sync(
        self,
        assistant_id: int,
        dataset_ids: List[int]
    ) -> Dict[str, List[int]]:
        """
        Полная синхронизация датасетов ассистента.

        Возвращает:
        - added
        - removed
        - unchanged
        - current
        """

        rows = self.session.exec(
            select(AssistantDataset.dataset_id).where(
                AssistantDataset.assistant_id == assistant_id
            )
        ).all()

        current_ids = set(rows)
        incoming_ids = set(dataset_ids)

        added = list(incoming_ids - current_ids)
        removed = list(current_ids - incoming_ids)
        unchanged = list(current_ids & incoming_ids)

        if removed:
            self.session.exec(
                delete(AssistantDataset).where(
                    AssistantDataset.assistant_id == assistant_id, # type: ignore
                    AssistantDataset.dataset_id.in_(removed) # type: ignore
                )
            )

        for dataset_id in added:
            self.session.add(
                AssistantDataset(
                    assistant_id=assistant_id,
                    dataset_id=dataset_id
                )
            )

        self.session.commit()

        current = sorted(incoming_ids)

        return {
            "added": sorted(added),
            "removed": sorted(removed),
            "unchanged": sorted(unchanged),
            "current": current,
        }

    def get_datasets(self, assistant_id: int) -> List[int]:
        rows = self.session.exec(
            select(AssistantDataset.dataset_id).where(
                AssistantDataset.assistant_id == assistant_id
            )
        ).all()

        return list(rows)
