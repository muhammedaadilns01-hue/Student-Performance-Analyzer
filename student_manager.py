import json

with open("students.json", "r") as file:
    student_data = json.load(file)

class StudentManager:

    def __init__(self, data):
        self.data = data
    
    def save_data(self):
        with open("students.json", "w") as file:
            json.dump(self.data, file, indent=4)
     
    def remove_duplicates(self):
        seen = set()
        unique_data = []
        for item in self.data:
            key = (item["name"], item["score"])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        self.data = unique_data
        


    def add_student(self):
        name = input("\nEnter the name of the student to add a new record: ")
        while True:
            try:
                score = int(input(f"Enter the score for {name}: "))
                if 0 <= score <= 100:
                    break
                print("score must be between 0 and 100")
            except ValueError:
                print("Please enter a valid number")
        new_student = {"name": name, "score": score}
        self.data.append(new_student)
        print("\nUpdated Student Records:")
        for student in self.data:
            print(f"{student['name']} - {student['score']} marks")
        return self.data


    def update_student(self):
        print("Updating the score for an existing student...")
        update_name = input("Enter the name of the student whose score you want to update: ")
        updated = False
        while True:
            try:
                new_score = int(input(f"Enter the new score for {update_name}: "))
                if 0 <= new_score <= 100:
                    break
                print("score must be between 0 and 100")
            except ValueError:
                print("Please enter a valid number")

        for student in self.data:
            if student["name"].lower() == update_name.lower():
                student["score"] = new_score
                print(f"Updated {student['name']}'s score to {new_score} marks.")
                updated = True
                break
        if not updated:
            print(f"No record found for student named {update_name}")
        return self.data


    def delete_student(self):
        print("Deleting a student record...")
        delete_name = input("Enter the name of the student you want to delete: ")
        deleted = False
        for i, student in enumerate(self.data):
            if student["name"].lower() == delete_name.lower():
                self.data.pop(i)
                print(f"Deleted record for student named {delete_name}")
                deleted = True
                break
        if not deleted:
            print(f"No record found for student named {delete_name}")
        return self.data


    def calculate_stats(self):
        highest_score = float('-inf')
        second_highest_score = float('-inf')
        topper = None
        second_topper = None
        total = 0
        pass_mark = 40

        for student in self.data:
            score = student["score"]
            total += score

            if score > highest_score:
                second_highest_score = highest_score
                second_topper = topper
                highest_score = score
                topper = student["name"]

            elif second_highest_score < score < highest_score:
                second_highest_score = score
                second_topper = student["name"]

            if score < pass_mark:
                print(f"{student['name']} has failed with {score} marks.")

        average_score = total / len(self.data) if self.data else 0
        return highest_score, second_highest_score, topper, second_topper, average_score