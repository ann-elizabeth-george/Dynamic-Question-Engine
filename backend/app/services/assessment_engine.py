from typing import List, Optional, Tuple
from app.models.mapping import CategoryQuestionMapping

class AssessmentEngine:
    @staticmethod
    def get_next_question_details(
        mappings: List[CategoryQuestionMapping],
        current_index: int
    ) -> Tuple[bool, int, Optional[int]]:
        """
        Takes list of mappings ordered by display_order and the current question index.
        Returns:
            (is_completed: bool, next_index: int, next_question_id: Optional[int])
        """
        total = len(mappings)
        next_index = current_index + 1
        
        if next_index >= total:
            return True, next_index, None
            
        next_mapping = mappings[next_index]
        return False, next_index, next_mapping.question_id

    @staticmethod
    def calculate_progress(current_index: int, total_questions: int) -> float:
        if total_questions == 0:
            return 100.0
        progress = (current_index / total_questions) * 100.0
        return round(min(progress, 100.0), 2)
