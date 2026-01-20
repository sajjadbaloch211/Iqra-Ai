
import os

def compact_policies():
    path = 'policies.txt'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Aggressive replacement
    content = content.replace("---", "")
    content = content.replace("Schedule:", "Sched:")
    content = content.replace("Monday", "Mon").replace("Tuesday", "Tue").replace("Wednesday", "Wed")
    content = content.replace("Thursday", "Thu").replace("Friday", "Fri").replace("Saturday", "Sat")
    content = content.replace("Sunday", "Sun")
    content = content.replace("Student Counseling", "Counseling").replace("Lecture Preparation", "Prep")
    content = content.replace("Research Work", "Research").replace("Departmental Work", "DeptWork")
    content = content.replace("OFF DAY", "OFF")
    content = content.replace("Senior Lecturer", "Sr.Lec").replace("Lecturer", "Lec")
    content = content.replace("Assistant Professor", "Asst.Prof")
    
    # Remove large fluff sections
    skip_sections = [
        "8. NOTABLE ALUMNI", 
        "10. STUDENT SOCIETIES & CLUBS", 
        "12. INTERNSHIP & CAREER PLACEMENT",
        "13. CODE OF CONDUCT",
        "7. FACILITIES & STUDENT LIFE"
    ]
    
    lines = content.split('\n')
    filtered_lines = []
    current_skip = False
    
    for line in lines:
        s = line.strip()
        if any(sec in s for sec in skip_sections):
            current_skip = True
        elif s.startswith("1") or s.startswith("2") or s.startswith("3") or s.startswith("4") or s.startswith("5") or s.startswith("6") or s.startswith("15"):
             if any(sec in s for sec in skip_sections):
                 current_skip = True
             else:
                 current_skip = False
        
        if not current_skip and s:
            filtered_lines.append(line)
            
    final_content = "\n".join(filtered_lines)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Aggressive Compact size: {len(final_content)} bytes")

if __name__ == "__main__":
    compact_policies()
