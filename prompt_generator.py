import json

# Topics and their respective sub-topics
topics = {
    "Java": [
        "Java Basics", "JVM and JRE", "Data Types and Variables", "Operators in Java", "Control Statements",
        "Object-Oriented Programming", "Classes and Objects", "Constructors", "Inheritance", "Polymorphism",
        "Abstraction", "Encapsulation", "Interfaces", "Exception Handling", "Collections Framework",
        "Multithreading", "File I/O", "Generics", "Lambda Expressions", "Streams API", "Serialization",
        "JDBC", "Garbage Collection", "Java 8 Features", "Design Patterns"
    ],
    "Python": [
        "Python Basics", "Data Types and Variables", "Operators", "Control Flow", "Functions", "Classes and Objects",
        "Inheritance", "Polymorphism", "Exception Handling", "File Handling", "Modules and Packages",
        "Libraries (Pandas, NumPy)", "Decorators", "Generators", "Comprehensions", "Regular Expressions",
        "Data Visualization", "Database Connectivity", "Multithreading", "Asyncio in Python",
        "Python Web Frameworks", "APIs in Python", "Python Scripts in DevOps", "Machine Learning Libraries",
        "Python Debugging"
    ],
    "React": [
        "React Basics", "JSX (JavaScript XML)", "Components and Props", "State Management", "Lifecycle Methods",
        "React Hooks", "React Router", "Event Handling", "Forms in React", "Conditional Rendering",
        "Lists and Keys", "Context API", "Redux Basics", "Middleware in Redux", "React-Redux Integration",
        "React Fragments", "Higher-Order Components (HOCs)", "React Performance Optimization", "React Portals",
        "Error Boundaries", "Testing in React", "Server-Side Rendering (SSR)", "React with APIs",
        "Material-UI and Styled Components", "React Deployment"
    ],
    "SQL Databases": [
        "SQL Basics", "SQL Syntax", "Data Types in SQL", "DDL Commands", "DML Commands", "TCL Commands",
        "DCL Commands", "Joins in SQL", "Subqueries", "Views", "Indexing", "Stored Procedures", "Triggers",
        "Transactions", "Constraints", "Keys (Primary, Foreign)", "Normalization", "ACID Properties",
        "Aggregate Functions", "Group By and Having", "Window Functions", "SQL Optimization", "SQL Injection",
        "Database Design", "Backup and Recovery"
    ],
    "Linux": [
        "Linux Basics", "File System", "Commands in Linux", "File Permissions", "User and Group Management",
        "Process Management", "Shell Scripting", "Editors (Vim/Nano)", "Package Management", "Networking in Linux",
        "System Logs", "Cron Jobs", "File Compression", "Disk Partitioning", "Boot Process", "Kernel and Shell",
        "Pipes and Redirection", "Linux Daemons", "Environment Variables", "Signals in Linux", "System Monitoring",
        "Troubleshooting", "SSH and Remote Access", "Security in Linux", "Linux Performance Tuning"
    ],
    "Computer Networks": [
        "OSI Model", "TCP/IP Model", "IP Addressing", "Subnetting", "Routing Protocols", "Switching Concepts",
        "DNS", "DHCP", "HTTP and HTTPS", "ARP", "TCP and UDP", "Firewalls", "Network Security", "VPN",
        "Proxy Servers", "LAN and WAN", "VLAN", "NAT", "Network Devices", "Wi-Fi Standards", "Bandwidth and Latency",
        "Packet Sniffing", "Network Troubleshooting", "Port Forwarding", "Cloud Networking"
    ],
    "Operating Systems": [
        "OS Basics", "Process Management", "Threads and Concurrency", "Scheduling Algorithms", "Memory Management",
        "Virtual Memory", "Paging and Segmentation", "Deadlocks", "File Systems", "Disk Management",
        "Input/Output Management", "Shell and Commands", "System Calls", "Interprocess Communication",
        "Semaphores and Mutex", "Signals", "Distributed Systems", "OS Security", "OS Virtualization",
        "Linux vs Windows OS", "Device Drivers", "Process Synchronization", "Booting Process", "Kernel Architecture",
        "OS Debugging Tools"
    ],
    "OOPS (Scenario-Based)": [
        "Class and Object Scenarios", "Constructor Scenarios", "Method Overloading", "Method Overriding",
        "Inheritance Scenarios", "Abstract Classes", "Interface Scenarios", "Encapsulation Examples",
        "Polymorphism Examples", "Composition and Aggregation", "Object Lifecycle", "Static Methods",
        "Final Keyword Usage", "Access Modifiers", "Multiple Inheritance", "Diamond Problem",
        "SOLID Principles", "Design Patterns", "Object Cloning", "Exception Handling Scenarios",
        "Serialization Scenarios", "Overriding vs Overloading", "Real-World OOP Examples", "Thread Safety in OOP",
        "Memory Leaks"
    ]
}

# Generate the prompts
output = []
for topic, sub_topics in topics.items():
    for sub_topic in sub_topics:
        prompt = {
            "topic": topic,
            "sub_topic": sub_topic,
            "question_prompt": f"Generate 20 questions about {sub_topic} with their difficulty level. List the question followed by its difficulty level (e.g., Easy, Medium, Hard). only list the question and difficulty level. in json"
        }
        output.append(prompt)

# Save to JSON file
output_file_path = r"C:\Kanak\BootCoding\Consume GPT APIs\Json Files\Generated_Prompts.json"
with open(output_file_path, "w") as file:
    json.dump(output, file, indent=4)

print(f"Prompts saved successfully to {output_file_path}")