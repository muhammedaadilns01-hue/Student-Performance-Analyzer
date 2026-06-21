import json
from student_manager import StudentManager

with open("students.json", "r") as file:
    student_data = json.load(file)

manager = StudentManager(student_data)
manager.remove_duplicates()

manager.save_data()

def main():
        manager = StudentManager(student_data)
        
        print("Student Performance Analysis ( Out of 100 )\n")
        manager.remove_duplicates()
        manager.save_data()
        while True:

            print("\n===== MENU =====")
            print("1. View Students")
            print("2. Search Student")
            print("3. Add Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Statistics")
            print("7. Export Report")
            print("8. Exit")
            

            choice = input("Enter choice: ").strip()
            print("DEBUG:", repr(choice))
            if choice == "1":
                print("Choice 1 selected")
                for student in manager.data:
                    print(student)
            elif choice == "2":
                search_name = input("\nEnter the name of the student to search for their score: ")
                found = False
                for student in manager.data:
                    if student["name"].lower() == search_name.lower():
                        print(f"{student['name']} scored {student['score']} marks")
                        found = True
                        break
                if not found:
                    print(f"No record found for student named {search_name}")
            elif choice == "3":
                manager.add_student()
                manager.save_data()
        
            elif choice == "4":
                manager.update_student()
                manager.save_data()
            elif choice == "5":
                manager.delete_student()
                manager.save_data()
            elif choice == "6":
                highest_score, second_highest_score, topper, second_topper, average_score = manager.calculate_stats()
                print("\n===== STATISTICS =====")
                print(f"Topper: {topper} - {highest_score} marks")
                print(f"Runner-up: {second_topper} - {second_highest_score} marks")
                print(f"Average Score: {average_score:.2f}")
                manager.save_data()
            elif choice == "7":
                highest_score, second_highest_score, topper, second_topper, average_score = manager.calculate_stats()
                print("Exporting the final student records to a file...")
                # Always recompute here
                ranked_students = sorted( manager.data, key=lambda student: student["score"],reverse=True)
                with open("student_performance_report.txt", "w") as file:
            
                        file.write("Student Performance Report\n")
                        file.write("--------------------------\n\n")
                        file.write(f"Topper: {topper} - {highest_score}\n")
                        file.write(f"Runner-up: {second_topper} - {second_highest_score}\n")
                        file.write(f"Average Score: {average_score:.2f}\n\n")
                        file.write("Ranked Students:\n")
                        rank = 1
                        for student in ranked_students:
                            file.write(f"{rank}. {student['name']} - {student['score']}\n")
                            rank += 1

                        pass_mark = 40
                        file.write("\nFailed Students:\n")
                        for student in manager.data:
                            if student["score"] < pass_mark:
                                file.write(f"{student['name']} - {student['score']}\n")
                print("Report exported to student_performance_report.txt successfully!")
            elif choice == "8":
                print("\nThank you for using the Student Performance Analyzer! 🎓📈")
                break

if __name__ == "__main__":
        main()



