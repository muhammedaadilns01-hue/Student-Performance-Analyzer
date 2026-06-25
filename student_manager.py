import json
from typing import List, Dict, Tuple, Optional


class StudentManager:
    def __init__(self, data: List[Dict]) -> None:
        """
        Initializes the manager with an in-memory student dataset.
        Ensures internal structural data integrity.
        """
        self.data: List[Dict] = data if isinstance(data, list) else []

    def save_data(self, file_path: str = "students.json") -> bool:
        """Saves current state back to the persistence layer."""
        try:
            with open(file_path, "w") as file:
                json.dump(self.data, file, indent=4)
            return True
        except IOError as e:
            print(f"[Error] Failed to persist data to disk: {e}")
            return False

    def remove_duplicates(self) -> None:
        """Removes records sharing identical name and score attributes."""
        seen = set()
        unique_data = []
        for item in self.data:
            # Using defensive .get() with lower casing to uniquely identify natural identities
            name_key = str(item.get("name", "")).strip().lower()
            score_key = item.get("score", 0)
            
            identifier = (name_key, score_key)
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(item)
        self.data = unique_data

    def add_student(self, name: str, score: int) -> None:
        """Business Logic: Appends a pre-validated student into state memory."""
        new_student = {"name": name.strip(), "score": score}
        self.data.append(new_student)

    def update_student(self, target_name: str, new_score: int) -> bool:
        """
        Business Logic: Updates an existing record by name query.
        Returns True on success, False if record is missing.
        """
        target_clean = target_name.strip().lower()
        for student in self.data:
            if student.get("name", "").lower() == target_clean:
                student["score"] = new_score
                return True
        return False

    def delete_student(self, target_name: str) -> bool:
        """
        Business Logic: Removes a record matching target criteria from state.
        Returns True on successful deletion, False if match is not found.
        """
        target_clean = target_name.strip().lower()
        for i, student in enumerate(self.data):
            if student.get("name", "").lower() == target_clean:
                self.data.pop(i)
                return True
        return False

    def calculate_stats(self) -> Tuple[float, float, Optional[str], Optional[str], float]:
        """
        Computes analytical performance aggregates.
        Handles standard fallback values when handling sparse datasets.
        """
        if not self.data:
            return 0, 0, None, None, 0.0

        highest_score = float('-inf')
        second_highest_score = float('-inf')
        topper = "N/A"
        second_topper = "N/A"
        total = 0

        for student in self.data:
            name = student.get("name", "Unknown")
            score = student.get("score", 0)
            total += score

            if score > highest_score:
                second_highest_score = highest_score
                second_topper = topper
                highest_score = score
                topper = name
            elif score > second_highest_score:
                second_highest_score = score
                second_topper = name

        average_score = total / len(self.data)
        
        # Clean up edge-case fallbacks if there's only 1 student in the system
        if second_highest_score == float('-inf'):
            second_highest_score = 0
            second_topper = "None"

        return highest_score, second_highest_score, topper, second_topper, average_score