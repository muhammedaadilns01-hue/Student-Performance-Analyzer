import json
import sys
from student_manager import StudentManager

# Constants for configuration
DATA_FILE = "students.json"
REPORT_FILE = "student_performance_report.txt"
PASSING_SCORE = 40


def load_student_data(file_path: str) -> list:
    """Safely loads student data from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[Warning] {file_path} not found. Starting with an empty dataset.")
        return []
    except json.JSONDecodeError:
        print(f"[Error] {file_path} is corrupted. Starting with an empty dataset.")
        return []


def display_menu() -> None:
    """Displays the interactive user interface options."""
    print("\n===== MENU =====")
    print("1. View Students")
    print("2. Search Student")
    print("3. Add Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Statistics")
    print("7. Export Report")
    print("8. Exit")


def handle_search(manager: StudentManager) -> None:
    """Handles logic for searching a specific student."""
    search_name = input("\nEnter the name of the student to search for: ").strip()
    if not search_name:
        print("Search name cannot be empty.")
        return

    found = False
    for student in manager.data:
        if student.get("name", "").lower() == search_name.lower():
            print(f"✨ {student['name']} scored {student['score']} marks.")
            found = True
            break
            
    if not found:
        print(f"❌ No record found for student named '{search_name}'")


def handle_export(manager: StudentManager) -> None:
    """Handles computation, sorting, and exporting of the performance report."""
    if not manager.data:
        print("⚠️ No data available to export.")
        return

    try:
        # Business logic computations
        highest_score, second_highest, topper, second_topper, avg_score = manager.calculate_stats()
        ranked_students = sorted(manager.data, key=lambda s: s.get("score", 0), reverse=True)

        print("Exporting final student records to file...")
        
        with open(REPORT_FILE, "w") as file:
            file.write("Student Performance Report\n")
            file.write("==========================\n\n")
            file.write(f"Topper: {topper} ({highest_score} marks)\n")
            file.write(f"Runner-up: {second_topper} ({second_highest} marks)\n")
            file.write(f"Average Score: {avg_score:.2f}\n\n")
            
            file.write("--- Ranked Students ---\n")
            for rank, student in enumerate(ranked_students, 1):
                file.write(f"{rank}. {student['name']} - {student['score']}\n")
                
            file.write("\n--- Failed Students (Below 40) ---\n")
            for student in manager.data:
                if student.get("score", 0) < PASSING_SCORE:
                    file.write(f"• {student['name']} - {student['score']}\n")

        print(f"✅ Report exported to '{REPORT_FILE}' successfully!")
    except Exception as e:
        print(f"❌ Failed to export report due to an unexpected error: {e}")


def main():
    print("🚀 Student Performance Analysis System Initialization...")
    
    # Core Data Injection
    student_data = load_student_data(DATA_FILE)
    manager = StudentManager(student_data)
    
    # Self-healing data optimization on boot
    manager.remove_duplicates()
    manager.save_data()

    while True:
        display_menu()
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            print("\n--- Current Student Records ---")
            if not manager.data:
                print("No records found.")
            for student in manager.data:
                print(f"• {student.get('name', 'Unknown')}: {student.get('score', 0)}")
                
        elif choice == "2":
            handle_search(manager)
            
        elif choice == "3":
            print("\n--- Add New Student Record ---")
            name = input("Enter the name of the student: ").strip()
            if not name:
                print("❌ Name cannot be empty.")
                continue
                
            # Score validation loop handled at the UI layer
            while True:
                try:
                    score = int(input(f"Enter the score for {name}: "))
                    if 0 <= score <= 100:
                        break
                    print("❌ Score must be between 0 and 100.")
                except ValueError:
                    print("❌ Please enter a valid whole number.")
            
            # Send the clean data to your manager
            manager.add_student(name, score)
            manager.save_data()
            print(f"✅ Successfully added {name} with a score of {score}!")
            
        elif choice == "4":
            print("\n--- Update Existing Student Record ---")
            name = input("Enter the name of the student whose score you want to update: ").strip()
            if not name:
                print("❌ Name cannot be empty.")
                continue

            while True:
                try:
                    new_score = int(input(f"Enter the new score for {name}: "))
                    if 0 <= new_score <= 100:
                        break
                    print("❌ Score must be between 0 and 100.")
                except ValueError:
                    print("❌ Please enter a valid whole number.")
            
            # Pass to manager and evaluate the boolean response flag
            success = manager.update_student(name, new_score)
            if success:
                manager.save_data()
                print(f"✅ Successfully updated {name}'s score to {new_score}!")
            else:
                print(f"❌ No record found for a student named '{name}'.")
            
        elif choice == "5":
            print("\n--- Delete Student Record ---")
            name = input("Enter the name of the student you want to delete: ").strip()
            if not name:
                print("❌ Name cannot be empty.")
                continue
                
            success = manager.delete_student(name)
            if success:
                manager.save_data()
                print(f"🗑️ Successfully deleted record for '{name}'.")
            else:
                print(f"❌ No record found for a student named '{name}'.")
            
        elif choice == "6":
            if not manager.data:
                print("⚠️ No student data available to calculate metrics.")
                continue
            highest, second_highest, topper, second_topper, avg = manager.calculate_stats()
            print("\n===== SYSTEM STATISTICS =====")
            print(f"🥇 Topper: {topper} - {highest} marks")
            print(f"🥈 Runner-up: {second_topper} - {second_highest} marks")
            print(f"📊 Average Score: {avg:.2f}")
            
        elif choice == "7":
            handle_export(manager)
            
        elif choice == "8":
            print("\nThank you for using the Student Performance Analyzer! 🎓📈")
            sys.exit(0)
            
        else:
            print("❌ Invalid selection. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()