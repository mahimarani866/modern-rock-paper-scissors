def show_students():
    if len(student_list) == 0:
        print("No students to display.\n")
        return

    print("\n-- All Students --")
    print(f"{'S.No':<5} {'Name':<20} {'Roll No':<10} {'Course':<15}")
    print("-" * 55)

    for idx, s in enumerate(student_list, start=1):
        print(f"{idx:<5} {s['Name']:<20} {s['Roll']:<10} {s['Course']:<15}")
    print()
