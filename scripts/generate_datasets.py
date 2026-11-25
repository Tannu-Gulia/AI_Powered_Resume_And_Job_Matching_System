"""
Dataset Generator for AI-Powered Resume & Job Matching System
Generates:
1. dataset/skills.csv - Curated skills catalog with learning resources
2. dataset/jobs.csv - 100+ realistic job listings across 10 diverse categories
3. dataset/candidates.csv - Realistic candidate profiles for recruiter testing
"""

import csv
import os
import random

os.makedirs('dataset', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('models', exist_ok=True)

# -------------------------------------------------------------
# 1. SKILLS DATASET
# -------------------------------------------------------------
SKILLS_DATA = [
    # Programming Languages
    ("Python", "Technical", "Programming Language", 5, "Python for Everybody Specialization", "Coursera", "https://www.coursera.org/specializations/python"),
    ("Java", "Technical", "Programming Language", 5, "Java Programming and Software Engineering Fundamentals", "Coursera", "https://www.coursera.org/specializations/java-programming"),
    ("C++", "Technical", "Programming Language", 4, "Coding for Everyone: C and C++", "Coursera", "https://www.coursera.org/specializations/coding-for-everyone"),
    ("C#", "Technical", "Programming Language", 4, "C# Programming for Unity Game Development", "Coursera", "https://www.coursera.org/specializations/csharp-unity-game-development"),
    ("JavaScript", "Technical", "Programming Language", 5, "The Complete JavaScript Course", "Udemy", "https://www.udemy.com/course/the-complete-javascript-course/"),
    ("TypeScript", "Technical", "Programming Language", 4, "Understanding TypeScript", "Udemy", "https://www.udemy.com/course/understanding-typescript/"),
    ("R", "Technical", "Programming Language", 4, "R Programming", "Coursera", "https://www.coursera.org/learn/r-programming"),
    ("SQL", "Technical", "Database", 5, "The Complete SQL Bootcamp", "Udemy", "https://www.udemy.com/course/the-complete-sql-bootcamp/"),
    ("Go", "Technical", "Programming Language", 3, "Programming with Google Go", "Coursera", "https://www.coursera.org/specializations/google-golang"),
    ("Rust", "Technical", "Programming Language", 3, "Rust Programming for Beginners", "Udemy", "https://www.udemy.com/course/rust-lang/"),
    ("PHP", "Technical", "Programming Language", 3, "PHP for Beginners", "Udemy", "https://www.udemy.com/course/php-for-beginners-/"),
    ("Kotlin", "Technical", "Programming Language", 4, "Kotlin for Java Developers", "Coursera", "https://www.coursera.org/learn/kotlin-for-java-developers"),
    ("Swift", "Technical", "Programming Language", 4, "iOS App Development with Swift", "Coursera", "https://www.coursera.org/specializations/app-development"),
    ("HTML5", "Technical", "Web Development", 4, "HTML, CSS, and Javascript for Web Developers", "Coursera", "https://www.coursera.org/learn/html-css-javascript-for-web-developers"),
    ("CSS3", "Technical", "Web Development", 4, "Advanced CSS and Sass", "Udemy", "https://www.udemy.com/course/advanced-css-and-sass/"),
    
    # Web & App Frameworks
    ("React", "Technical", "Web Framework", 5, "React - The Complete Guide", "Udemy", "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"),
    ("Angular", "Technical", "Web Framework", 4, "Angular - The Complete Guide", "Udemy", "https://www.udemy.com/course/the-complete-guide-to-angular-2/"),
    ("Vue.js", "Technical", "Web Framework", 4, "Vue - The Complete Guide", "Udemy", "https://www.udemy.com/course/vuejs-2-the-complete-guide/"),
    ("Node.js", "Technical", "Backend Framework", 5, "Node.js Developer Course", "Udemy", "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/"),
    ("Express.js", "Technical", "Backend Framework", 4, "NodeJS & Express Framework", "Udemy", "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/"),
    ("Django", "Technical", "Web Framework", 5, "Django for Beginners & Professionals", "Udemy", "https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/"),
    ("Flask", "Technical", "Web Framework", 4, "REST APIs with Flask and Python", "Udemy", "https://www.udemy.com/course/rest-api-flask-and-python/"),
    ("FastAPI", "Technical", "Web Framework", 4, "FastAPI - Modern Python Web APIs", "Udemy", "https://www.udemy.com/course/fastapi-the-complete-course/"),
    ("Spring Boot", "Technical", "Backend Framework", 5, "Spring Boot 3, Spring 6 & Hibernate", "Udemy", "https://www.udemy.com/course/spring-hibernate-tutorial/"),
    ("ASP.NET Core", "Technical", "Backend Framework", 4, "Complete ASP.NET Core MVC Bootcamp", "Udemy", "https://www.udemy.com/course/complete-aspnet-core-mvc-bootcamp/"),

    # Data Science & Machine Learning
    ("Machine Learning", "Technical", "AI / ML", 5, "Machine Learning Specialization by Andrew Ng", "Coursera", "https://www.coursera.org/specializations/machine-learning-introduction"),
    ("Deep Learning", "Technical", "AI / ML", 5, "Deep Learning Specialization", "Coursera", "https://www.coursera.org/specializations/deep-learning"),
    ("Natural Language Processing", "Technical", "AI / ML", 5, "Natural Language Processing Specialization", "Coursera", "https://www.coursera.org/specializations/natural-language-processing-nlp"),
    ("NLP", "Technical", "AI / ML", 5, "NLP in Python with Spacy & NLTK", "Coursera", "https://www.coursera.org/specializations/natural-language-processing-nlp"),
    ("Computer Vision", "Technical", "AI / ML", 4, "Deep Learning for Computer Vision", "Coursera", "https://www.coursera.org/learn/deep-learning-in-computer-vision"),
    ("TensorFlow", "Technical", "AI Library", 5, "DeepLearning.AI TensorFlow Developer", "Coursera", "https://www.coursera.org/professional-certificates/tensorflow-in-practice"),
    ("PyTorch", "Technical", "AI Library", 5, "Deep Neural Networks with PyTorch", "Coursera", "https://www.coursera.org/learn/deep-neural-networks-with-pytorch"),
    ("Scikit-learn", "Technical", "AI Library", 5, "Applied Machine Learning in Python", "Coursera", "https://www.coursera.org/learn/python-machine-learning"),
    ("Pandas", "Technical", "Data Analysis", 5, "Data Analysis with Python and Pandas", "Coursera", "https://www.coursera.org/learn/data-analysis-with-python"),
    ("NumPy", "Technical", "Data Analysis", 5, "Applied Data Science with Python", "Coursera", "https://www.coursera.org/specializations/data-science-python"),
    ("Matplotlib", "Technical", "Data Visualization", 4, "Data Visualization with Python", "Coursera", "https://www.coursera.org/learn/python-for-data-visualization"),
    ("Seaborn", "Technical", "Data Visualization", 4, "Python for Data Science and Machine Learning", "Udemy", "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/"),
    ("Tableau", "Technical", "BI & Analytics", 5, "Tableau Desktop Specialist Certification", "Coursera", "https://www.coursera.org/learn/data-visualization-tableau"),
    ("Power BI", "Technical", "BI & Analytics", 5, "Microsoft Power BI Data Analyst Professional", "Coursera", "https://www.coursera.org/professional-certificates/microsoft-power-bi-data-analyst"),
    ("Excel", "Technical", "BI & Analytics", 4, "Excel Skills for Business", "Coursera", "https://www.coursera.org/specializations/excel"),
    ("Statistics", "Technical", "Data Science", 5, "Statistics with Python Specialization", "Coursera", "https://www.coursera.org/specializations/statistics-with-python"),
    ("Big Data", "Technical", "Data Engineering", 4, "Big Data Specialization", "Coursera", "https://www.coursera.org/specializations/big-data"),
    ("Spark", "Technical", "Data Engineering", 5, "Apache Spark 3 for Data Engineering", "Udemy", "https://www.udemy.com/course/taming-big-data-with-apache-spark-hands-on/"),
    ("Hadoop", "Technical", "Data Engineering", 3, "The Ultimate Hands-On Hadoop", "Udemy", "https://www.udemy.com/course/the-ultimate-hands-on-hadoop-tame-your-big-data/"),
    ("Kafka", "Technical", "Data Engineering", 4, "Apache Kafka for Beginners", "Udemy", "https://www.udemy.com/course/apache-kafka/"),

    # Databases
    ("PostgreSQL", "Technical", "Database", 5, "PostgreSQL for Everybody", "Coursera", "https://www.coursera.org/specializations/postgresql-for-everybody"),
    ("MySQL", "Technical", "Database", 5, "MySQL Database Administration", "Coursera", "https://www.coursera.org/learn/database-structures-and-management-with-mysql"),
    ("MongoDB", "Technical", "Database", 4, "MongoDB - The Complete Developer's Guide", "Udemy", "https://www.udemy.com/course/mongodb-the-complete-developers-guide/"),
    ("Redis", "Technical", "Database", 4, "Redis: The Complete Developer's Guide", "Udemy", "https://www.udemy.com/course/redis-the-complete-developers-guide-with-microservices/"),
    ("Oracle", "Technical", "Database", 4, "Oracle SQL Databases Masterclass", "Udemy", "https://www.udemy.com/course/oracle-sql-step-by-step/"),
    ("Snowflake", "Technical", "Cloud Data Warehouse", 4, "Snowflake Masterclass", "Udemy", "https://www.udemy.com/course/ultimate-snowpro-core-certification/"),
    
    # Cloud & DevOps
    ("AWS", "Technical", "Cloud Computing", 5, "AWS Certified Solutions Architect Associate", "Coursera", "https://www.coursera.org/learn/aws-cloud-solutions-architect"),
    ("Azure", "Technical", "Cloud Computing", 5, "Microsoft Azure Fundamentals AZ-900", "Coursera", "https://www.coursera.org/learn/microsoft-azure-fundamentals-az-900"),
    ("GCP", "Technical", "Cloud Computing", 4, "Google Cloud Platform Fundamentals", "Coursera", "https://www.coursera.org/learn/gcp-fundamentals"),
    ("Docker", "Technical", "DevOps & Containers", 5, "Docker & Kubernetes: The Practical Guide", "Udemy", "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"),
    ("Kubernetes", "Technical", "DevOps & Containers", 5, "Certified Kubernetes Administrator (CKA)", "Udemy", "https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/"),
    ("Git", "Technical", "Version Control", 5, "Version Control with Git", "Coursera", "https://www.coursera.org/learn/version-control-with-git"),
    ("GitHub", "Technical", "Version Control", 5, "Git & GitHub Crash Course", "Udemy", "https://www.udemy.com/course/git-and-github-bootcamp/"),
    ("CI/CD", "Technical", "DevOps", 4, "Continuous Integration and Continuous Deployment", "Coursera", "https://www.coursera.org/learn/continuous-integration-continuous-deployment"),
    ("Jenkins", "Technical", "DevOps", 4, "Jenkins: Beginner to Advanced", "Udemy", "https://www.udemy.com/course/jenkins-from-zero-to-hero/"),
    ("Terraform", "Technical", "DevOps", 4, "HashiCorp Certified: Terraform Associate", "Udemy", "https://www.udemy.com/course/terraform-beginner-to-advanced/"),
    ("Linux", "Technical", "Operating System", 4, "Linux for Beginners", "Udemy", "https://www.udemy.com/course/linux-for-beginners/"),

    # Testing & Security
    ("Unit Testing", "Technical", "Testing", 4, "Testing in Python & PyTest", "Coursera", "https://www.coursera.org/learn/unit-testing"),
    ("Selenium", "Technical", "Automated Testing", 4, "Selenium WebDriver with Java", "Udemy", "https://www.udemy.com/course/selenium-real-time-examplesinterview-questions/"),
    ("Cybersecurity", "Technical", "Security", 4, "Google Cybersecurity Professional Certificate", "Coursera", "https://www.coursera.org/professional-certificates/google-cybersecurity"),
    ("Network Security", "Technical", "Security", 4, "Introduction to Cyber Security", "Coursera", "https://www.coursera.org/specializations/intro-cyber-security"),
    ("REST API", "Technical", "Web Architecture", 5, "API Design and Fundamentals of Google Cloud's Apigee", "Coursera", "https://www.coursera.org/learn/api-design-fundamentals"),
    ("GraphQL", "Technical", "Web Architecture", 4, "GraphQL with React: The Complete Developers Guide", "Udemy", "https://www.udemy.com/course/graphql-with-react-course/"),

    # Soft Skills
    ("Communication", "Soft Skill", "Interpersonal", 5, "Effective Communication: Writing, Design, and Presentation", "Coursera", "https://www.coursera.org/specializations/effective-communication"),
    ("Problem Solving", "Soft Skill", "Analytical", 5, "Problem Solving Using Computational Thinking", "Coursera", "https://www.coursera.org/learn/computational-thinking-problem-solving"),
    ("Team Leadership", "Soft Skill", "Management", 5, "Inspiring and Motivating Individuals", "Coursera", "https://www.coursera.org/learn/motivating-people-teams"),
    ("Critical Thinking", "Soft Skill", "Analytical", 4, "Critical Thinking Skills for Success", "Coursera", "https://www.coursera.org/learn/critical-thinking-skills"),
    ("Agile Methodology", "Soft Skill", "Management", 5, "Agile with Atlassian Jira", "Coursera", "https://www.coursera.org/learn/agile-atlassian-jira"),
    ("Scrum", "Soft Skill", "Management", 4, "Scrum Master Certification Prep", "Coursera", "https://www.coursera.org/learn/scrum-master-certification"),
    ("Time Management", "Soft Skill", "Productivity", 4, "Work Smarter, Not Harder: Time Management", "Coursera", "https://www.coursera.org/learn/work-smarter-not-harder"),
    ("Adaptability", "Soft Skill", "Personal Development", 4, "Developing Adaptability in the Workplace", "LinkedIn Learning", "https://www.linkedin.com/learning/developing-adaptability"),
    ("Collaboration", "Soft Skill", "Interpersonal", 4, "Teamwork Skills: Communicating Effectively in Groups", "Coursera", "https://www.coursera.org/learn/teamwork-skills-effective-communication"),
    ("Presentation Skills", "Soft Skill", "Interpersonal", 4, "Successful Presentation", "Coursera", "https://www.coursera.org/learn/presentation-skills"),
    ("Analytical Thinking", "Soft Skill", "Analytical", 5, "Data-Driven Decision Making", "Coursera", "https://www.coursera.org/learn/decision-making-data"),
    ("Negotiation", "Soft Skill", "Business", 4, "Successful Negotiation: Essential Strategies and Skills", "Coursera", "https://www.coursera.org/learn/negotiation-skills")
]

with open('dataset/skills.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["skill_name", "category", "sub_category", "importance_weight", "recommended_course", "course_platform", "course_url"])
    for row in SKILLS_DATA:
        writer.writerow(row)

print(f"Generated {len(SKILLS_DATA)} skills in dataset/skills.csv")

# -------------------------------------------------------------
# 2. JOBS DATASET (105 Realistic Jobs across 10 categories)
# -------------------------------------------------------------
JOB_CATEGORIES = [
    "Data Science & Analytics",
    "Machine Learning & AI",
    "Python & Backend Development",
    "Full-Stack Web Development",
    "Java & Enterprise Development",
    "Business Intelligence & Analysis",
    "Database Administration & Engineering",
    "Cloud Computing & DevOps",
    "Software Quality & Testing",
    "Cybersecurity & Networks"
]

COMPANIES = [
    ("Google", "Bangalore, India", "Hybrid"),
    ("Microsoft", "Hyderabad, India", "Hybrid"),
    ("Amazon", "Bangalore, India", "On-site"),
    ("TCS", "Mumbai, India", "Hybrid"),
    ("Infosys", "Pune, India", "Remote"),
    ("Wipro", "Bangalore, India", "Hybrid"),
    ("Accenture", "Gurgaon, India", "Hybrid"),
    ("Deloitte", "Hyderabad, India", "On-site"),
    ("IBM", "Bangalore, India", "Remote"),
    ("Oracle", "Bengaluru, India", "Hybrid"),
    ("Cognizant", "Chennai, India", "Hybrid"),
    ("Capgemini", "Mumbai, India", "On-site"),
    ("Flipkart", "Bangalore, India", "Hybrid"),
    ("Swiggy", "Bangalore, India", "Remote"),
    ("Zomato", "Gurgaon, India", "Hybrid"),
    ("Paytm", "Noida, India", "On-site"),
    ("Reliance Jio", "Navi Mumbai, India", "Hybrid"),
    ("Goldman Sachs", "Bengaluru, India", "Hybrid"),
    ("JPMorgan Chase", "Mumbai, India", "Hybrid"),
    ("HCL Technologies", "Noida, India", "Remote"),
    ("Tech Mahindra", "Pune, India", "Hybrid"),
    ("LTI Mindtree", "Chennai, India", "Hybrid")
]

JOB_TEMPLATES = {
    "Data Science & Analytics": [
        ("Junior Data Analyst", "Entry", 0, "4.5 - 7 LPA", ["Python", "SQL", "Excel", "Tableau", "Statistics", "Problem Solving"],
         "Bachelor's or Master's in Data Science, Computer Science, Statistics or MCA",
         "Collect, clean, and interpret data sets to answer business questions. Create actionable dashboards using Tableau and SQL."),
        ("Data Analyst II", "Mid", 2, "8 - 14 LPA", ["Python", "SQL", "Pandas", "Power BI", "Statistics", "Communication"],
         "B.Tech / MCA / M.Sc in Data Science or Analytics",
         "Lead analytics initiatives, perform exploratory data analysis, and translate business requirements into executive reports."),
        ("Senior Data Scientist", "Senior", 5, "18 - 30 LPA", ["Python", "Machine Learning", "Scikit-learn", "Pandas", "SQL", "Statistics", "Problem Solving"],
         "Master's or Ph.D. in Computer Science, Statistics, Mathematics or MCA",
         "Architect, build, and deploy predictive ML models. Drive high-impact machine learning algorithms to solve customer churn and lifetime value."),
        ("Lead Data Scientist", "Lead", 7, "28 - 45 LPA", ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "SQL", "Team Leadership"],
         "M.Tech / MCA / Ph.D. in AI, CS, or quantitative disciplines",
         "Mentor data scientists, drive core algorithmic roadmap, and productionize large-scale deep learning models."),
        ("Healthcare Data Analyst", "Mid", 2, "7.5 - 12 LPA", ["Python", "R", "SQL", "Tableau", "Statistics", "Critical Thinking"],
         "Bachelor's or Master's in Health Informatics, Data Science, or MCA",
         "Analyze patient clinical trends, clinical trials, and operational health metrics while adhering to data privacy standards."),
        ("Financial Data Analyst", "Mid", 3, "9 - 16 LPA", ["Python", "SQL", "Excel", "Power BI", "Statistics", "Analytical Thinking"],
         "Degree in Finance, Data Science, Statistics, or MCA",
         "Develop financial forecasting models, credit risk assessment matrices, and interactive Power BI executive dashboards."),
        ("Marketing Analytics Specialist", "Entry", 1, "5 - 8.5 LPA", ["SQL", "Python", "Tableau", "Excel", "Communication", "Problem Solving"],
         "Bachelor's / Master's degree in Marketing, Business Analytics or MCA",
         "Track marketing spend attribution, ROI across customer acquisition funnels, and customer retention metrics.")
    ],
    "Machine Learning & AI": [
        ("Associate ML Engineer", "Entry", 0, "6 - 10 LPA", ["Python", "Machine Learning", "Scikit-learn", "NumPy", "Pandas", "Git"],
         "B.Tech / MCA / M.Sc Computer Science or Artificial Intelligence",
         "Assist in preparing datasets, training baseline ML models, feature engineering, and conducting hyperparameter tuning."),
        ("Machine Learning Engineer", "Mid", 2, "12 - 20 LPA", ["Python", "Machine Learning", "Deep Learning", "PyTorch", "Docker", "REST API"],
         "B.Tech / MCA / M.Tech in Computer Science or Data Science",
         "Develop robust production ML pipelines, build inference APIs, and integrate models with enterprise backend systems."),
        ("NLP Engineer", "Mid", 3, "14 - 24 LPA", ["Python", "Natural Language Processing", "NLP", "PyTorch", "Transformers", "Scikit-learn"],
         "Master's degree in CS, Computational Linguistics, MCA or equivalent",
         "Build modern NLP pipelines, text classification, named entity recognition (NER), and sentiment analysis models."),
        ("Computer Vision Engineer", "Senior", 4, "16 - 28 LPA", ["Python", "Computer Vision", "PyTorch", "TensorFlow", "Docker", "C++"],
         "B.Tech / M.Tech / MCA in Computer Science or Robotics",
         "Design and optimize image segmentation, object detection, and video stream analytics systems."),
        ("Generative AI & LLM Specialist", "Senior", 4, "20 - 35 LPA", ["Python", "PyTorch", "NLP", "FastAPI", "Docker", "Problem Solving"],
         "M.Tech / MCA / Ph.D. in Artificial Intelligence or CS",
         "Fine-tune Large Language Models (LLMs), build Retrieval-Augmented Generation (RAG) architectures, and vector search engines."),
        ("Deep Learning Research Scientist", "Senior", 5, "25 - 42 LPA", ["Python", "Deep Learning", "PyTorch", "TensorFlow", "Statistics", "Critical Thinking"],
         "Ph.D. or Master's in Machine Learning, Computer Science, or MCA",
         "Publish research, benchmark novel neural architectures, and apply cutting-edge deep learning to mission-critical problems.")
    ],
    "Python & Backend Development": [
        ("Junior Python Developer", "Entry", 0, "4 - 7 LPA", ["Python", "Django", "SQL", "Git", "HTML5", "Problem Solving"],
         "B.Sc / BCA / MCA / B.Tech in Computer Science or IT",
         "Write clean, testable Python code for backend services, implement database models, and write automated tests."),
        ("Backend Python Engineer", "Mid", 2, "8 - 15 LPA", ["Python", "FastAPI", "PostgreSQL", "Docker", "REST API", "Redis"],
         "Bachelor's / MCA in Computer Science or related degree",
         "Develop high-performance RESTful microservices, optimize database queries, and integrate caching layers with Redis."),
        ("Django Web Specialist", "Mid", 3, "9 - 16 LPA", ["Python", "Django", "PostgreSQL", "REST API", "Git", "Agile Methodology"],
         "Degree in Software Engineering, MCA or relevant experience",
         "Architect web portals using Django and Django REST framework, ensuring security, scalability, and fast page loads."),
        ("Senior Python Systems Architect", "Senior", 6, "22 - 36 LPA", ["Python", "FastAPI", "Docker", "Kubernetes", "AWS", "PostgreSQL", "Team Leadership"],
         "Master's or Bachelor's in CS / MCA",
         "Lead architectural decisions for cloud-native Python services, enforce code quality standards, and mentor junior devs."),
        ("Python API Developer", "Mid", 2, "7.5 - 13 LPA", ["Python", "Flask", "SQL", "REST API", "Unit Testing", "Git"],
         "MCA / BCA / B.Tech in Computer Science",
         "Design, test, and document RESTful endpoints using Flask and Swagger. Ensure 99.9% API uptime and low latency.")
    ],
    "Full-Stack Web Development": [
        ("Junior Full-Stack Developer", "Entry", 0, "4.5 - 7.5 LPA", ["JavaScript", "React", "Node.js", "HTML5", "CSS3", "Git"],
         "BCA / MCA / B.Tech in IT or Computer Science",
         "Build modern, responsive UI components in React and backend services in Node.js. Collaborate with designers."),
        ("Full-Stack React & Node Engineer", "Mid", 3, "10 - 18 LPA", ["JavaScript", "TypeScript", "React", "Node.js", "MongoDB", "REST API"],
         "Bachelor's or Master's in CS, MCA or related field",
         "End-to-end full stack development: React frontend state management, Express backend APIs, and NoSQL databases."),
        ("Senior MERN Stack Developer", "Senior", 5, "18 - 28 LPA", ["React", "Node.js", "Express.js", "MongoDB", "TypeScript", "Docker"],
         "B.Tech / MCA / M.Sc Software Engineering",
         "Drive architecture of large-scale MERN applications, conduct code reviews, and implement CI/CD deployment pipelines."),
        ("Frontend Web Engineer", "Mid", 2, "7 - 14 LPA", ["JavaScript", "TypeScript", "React", "HTML5", "CSS3", "Git"],
         "Bachelor's in CS / IT / MCA",
         "Create pixel-perfect, accessible web interfaces. Optimize bundle size, Core Web Vitals, and responsive layouts."),
        ("Full-Stack Angular & Java Developer", "Mid", 3, "11 - 19 LPA", ["Java", "Spring Boot", "Angular", "TypeScript", "SQL", "Git"],
         "B.Tech / MCA in Computer Science",
         "Develop enterprise web apps combining modern Angular frontend with robust Spring Boot microservices backend.")
    ],
    "Java & Enterprise Development": [
        ("Associate Java Developer", "Entry", 0, "4.5 - 7.5 LPA", ["Java", "Spring Boot", "SQL", "Git", "Problem Solving"],
         "B.Tech / MCA / BCA in Computer Science",
         "Develop core business logic in Java, write unit tests with JUnit, and participate in daily agile standups."),
        ("Java Spring Boot Developer", "Mid", 2, "8.5 - 16 LPA", ["Java", "Spring Boot", "PostgreSQL", "REST API", "Docker", "Git"],
         "B.Tech / MCA / M.Tech in CS or IT",
         "Design and build resilient enterprise microservices using Spring Boot, Hibernate ORM, and cloud message queues."),
        ("Senior Java Enterprise Architect", "Senior", 6, "22 - 38 LPA", ["Java", "Spring Boot", "Kafka", "PostgreSQL", "Docker", "Kubernetes", "Team Leadership"],
         "MCA / B.Tech / M.Tech in Computer Science",
         "Direct architectural roadmap for mission-critical banking and fintech Java microservices handling millions of transactions."),
        ("Core Java Backend Engineer", "Mid", 3, "10 - 17 LPA", ["Java", "SQL", "REST API", "Unit Testing", "Git", "Agile Methodology"],
         "Bachelor's or MCA in Computer Science",
         "Maintain and upgrade distributed multi-threaded Java applications, tuning garbage collection and latency.")
    ],
    "Business Intelligence & Analysis": [
        ("Business Analyst", "Entry", 1, "5 - 8 LPA", ["SQL", "Excel", "Agile Methodology", "Communication", "Problem Solving", "Tableau"],
         "MBA / MCA / B.Tech / BBA with analytical focus",
         "Bridge the gap between business stakeholders and tech teams. Formulate user stories, acceptance criteria, and workflows."),
        ("Senior Business Analyst", "Senior", 5, "14 - 24 LPA", ["SQL", "Agile Methodology", "Scrum", "Communication", "Presentation Skills", "Power BI"],
         "Master's in Business, Information Systems, MCA or equivalent",
         "Lead requirement elicitation workshops, manage product backlogs, and deliver data-backed strategic recommendations."),
        ("BI Developer (Power BI / Tableau)", "Mid", 3, "8.5 - 15 LPA", ["Power BI", "Tableau", "SQL", "Excel", "Data Analysis", "Communication"],
         "Bachelor's or MCA in CS, Statistics or IT",
         "Build automated reporting dashboards, model complex star-schema data models, and ensure high reporting reliability.")
    ],
    "Database Administration & Engineering": [
        ("Database Administrator (DBA)", "Mid", 3, "9 - 16 LPA", ["SQL", "PostgreSQL", "MySQL", "Linux", "Problem Solving"],
         "BCA / MCA / B.Tech in Computer Science",
         "Manage database instances, execute schema migrations, configure automatic backups, and fine-tune slow queries."),
        ("Senior PostgreSQL Specialist", "Senior", 5, "18 - 30 LPA", ["PostgreSQL", "SQL", "Linux", "Docker", "Python", "Problem Solving"],
         "Bachelor's or Master's in CS / MCA",
         "Optimize high-throughput relational databases, set up streaming replication, high availability, and disaster recovery."),
        ("Data Engineer (Big Data & ETL)", "Mid", 3, "11 - 20 LPA", ["Python", "SQL", "Spark", "Kafka", "PostgreSQL", "Git"],
         "B.Tech / MCA / M.Sc in Computer Science",
         "Build and maintain robust ETL/ELT pipelines, streaming data ingestion from diverse sources into data lakes.")
    ],
    "Cloud Computing & DevOps": [
        ("Cloud DevOps Engineer", "Mid", 2, "9 - 17 LPA", ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Git"],
         "B.Tech / MCA in Computer Science / IT",
         "Implement Infrastructure as Code, streamline automated CI/CD deployment pipelines, and maintain cloud infrastructure."),
        ("Senior AWS Solutions Architect", "Senior", 5, "20 - 35 LPA", ["AWS", "Terraform", "Docker", "Kubernetes", "Linux", "Team Leadership"],
         "MCA / B.Tech in CS or relevant cloud certifications",
         "Architect resilient, fault-tolerant, and secure multi-tier applications across AWS cloud availability zones."),
        ("Site Reliability Engineer (SRE)", "Mid", 3, "12 - 22 LPA", ["Linux", "Python", "Docker", "Kubernetes", "CI/CD", "Problem Solving"],
         "Degree in Computer Science, MCA or related technical field",
         "Maximize service uptime, establish SLAs/SLOs, automate incident response, and resolve complex production anomalies.")
    ],
    "Software Quality & Testing": [
        ("QA Automation Engineer", "Mid", 2, "6.5 - 12 LPA", ["Selenium", "Python", "Java", "Git", "Unit Testing", "Problem Solving"],
         "BCA / MCA / B.Tech in Computer Science",
         "Create automated functional test suites using Selenium WebDriver, integrate tests into Jenkins CI/CD pipelines."),
        ("Lead Software Quality Analyst", "Senior", 5, "15 - 25 LPA", ["Selenium", "CI/CD", "Unit Testing", "Agile Methodology", "Team Leadership"],
         "MCA / B.Tech with QA certification (ISTQB)",
         "Lead the testing strategy across web and mobile products, defining regression suites and release acceptance gates.")
    ],
    "Cybersecurity & Networks": [
        ("Cybersecurity Analyst", "Mid", 2, "8 - 15 LPA", ["Cybersecurity", "Network Security", "Linux", "Python", "Problem Solving"],
         "B.Tech / MCA / M.Sc in Cybersecurity or Computer Science",
         "Monitor SIEM logs, conduct vulnerability assessments, and respond rapidly to potential security threats."),
        ("Information Security Specialist", "Senior", 5, "16 - 28 LPA", ["Cybersecurity", "Network Security", "Linux", "AWS", "Communication"],
         "MCA / B.Tech with CEH or CISSP certification",
         "Design security architectures, enforce zero-trust policies, conduct audits, and ensure compliance with ISO 27001.")
    ]
}

# Generate 105 jobs
jobs_rows = []
job_id = 1
random.seed(42)

for category, templates in JOB_TEMPLATES.items():
    for template in templates:
        # Generate 2 to 4 listings for each template with different companies and locations
        repetitions = random.choice([3, 4])
        for _ in range(repetitions):
            title, exp_lvl, min_exp, salary, skills, qual, desc = template
            company_info = random.choice(COMPANIES)
            company_name = company_info[0]
            location = company_info[1]
            job_type = company_info[2]
            
            # Additional skills variation
            extra_pool = ["Git", "Communication", "Problem Solving", "Agile Methodology", "Docker", "SQL", "REST API", "Linux"]
            skills_set = list(dict.fromkeys(skills + [random.choice(extra_pool)]))
            
            responsibilities = (
                f"- Collaborate with cross-functional teams to design, implement, and maintain {category} solutions.\n"
                f"- Apply best engineering practices in {', '.join(skills_set[:3])}.\n"
                f"- Conduct regular code/system reviews, write documentation, and support agile sprints.\n"
                f"- Maintain clean code, robust testing, and adhere to security standards."
            )
            
            day_offset = random.randint(1, 30)
            posted_date = f"2026-10-{day_offset:02d}" if day_offset <= 30 else "2026-10-15"
            
            jobs_rows.append([
                job_id,
                title,
                company_name,
                category,
                location,
                job_type,
                exp_lvl,
                min_exp,
                salary,
                ", ".join(skills_set),
                qual,
                desc,
                responsibilities,
                posted_date
            ])
            job_id += 1

with open('dataset/jobs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        "job_id", "title", "company", "category", "location", "job_type",
        "experience_level", "min_experience_years", "salary_range",
        "required_skills", "qualifications", "description",
        "responsibilities", "posted_date"
    ])
    for row in jobs_rows:
        writer.writerow(row)

print(f"Generated {len(jobs_rows)} jobs in dataset/jobs.csv")

# -------------------------------------------------------------
# 3. CANDIDATES DATASET (Sample candidates)
# -------------------------------------------------------------
CANDIDATE_DATA = [
    (1, "Aarav Sharma", "candidate@test.com", "+91 98765 43210", "Data Science Aspirant", 1,
     "Master of Computer Applications (MCA) in Data Science, 2024",
     "Python, Machine Learning, Scikit-learn, Pandas, NumPy, SQL, Tableau, Statistics, Git, Problem Solving, Communication",
     "Bangalore, India",
     "Enthusiastic MCA Data Science graduate with hands-on experience in machine learning pipelines, predictive modeling, and data visualization using Python and Tableau."),
    
    (2, "Priya Nair", "priya.nair@example.com", "+91 98111 22334", "Python Backend Developer", 2,
     "B.Tech in Computer Science, 2023",
     "Python, Django, FastAPI, PostgreSQL, Docker, Git, REST API, Redis, Problem Solving",
     "Pune, India",
     "Backend software engineer with 2 years of experience designing scalable RESTful APIs and microservices using Python, FastAPI, and PostgreSQL."),
    
    (3, "Rohan Patel", "rohan.patel@example.com", "+91 98222 33445", "Data Analyst", 3,
     "B.Sc in Statistics, MCA in Computer Science",
     "Python, SQL, Power BI, Excel, Pandas, Statistics, Data Analysis, Communication, Analytical Thinking",
     "Mumbai, India",
     "Data Analyst with 3 years of expertise in deriving actionable business intelligence from raw datasets using SQL, Python, and Power BI."),

    (4, "Ananya Verma", "ananya.verma@example.com", "+91 98333 44556", "Full-Stack Developer", 2,
     "Bachelor of Computer Applications (BCA), MCA",
     "JavaScript, TypeScript, React, Node.js, Express.js, MongoDB, HTML5, CSS3, Git, REST API",
     "Hyderabad, India",
     "Full-stack MERN developer proficient in crafting dynamic user interfaces with React and scalable RESTful backends with Node.js and MongoDB."),

    (5, "Vikram Malhotra", "vikram.m@example.com", "+91 98444 55667", "Machine Learning Engineer", 4,
     "M.Tech in Artificial Intelligence",
     "Python, Machine Learning, Deep Learning, PyTorch, TensorFlow, NLP, Scikit-learn, Docker, Git",
     "Bangalore, India",
     "Experienced Machine Learning Engineer with 4 years in productionizing NLP and computer vision deep neural networks."),

    (6, "Sneha Kulkarni", "sneha.k@example.com", "+91 98555 66778", "Java Developer", 2,
     "MCA in Software Engineering",
     "Java, Spring Boot, SQL, PostgreSQL, REST API, Git, Agile Methodology, Unit Testing",
     "Pune, India",
     "Java developer specializing in enterprise applications using Spring Boot microservices, relational databases, and agile software development."),

    (7, "Karthik Iyer", "karthik.i@example.com", "+91 98666 77889", "Cloud & DevOps Engineer", 3,
     "B.Tech in Information Technology",
     "AWS, Docker, Kubernetes, CI/CD, Linux, Git, Terraform, Python",
     "Chennai, India",
     "DevOps professional focused on cloud infrastructure automation on AWS, container orchestration with Kubernetes, and continuous deployment.")
]

with open('dataset/candidates.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        "candidate_id", "name", "email", "phone", "current_role",
        "experience_years", "education", "skills", "location", "bio"
    ])
    for row in CANDIDATE_DATA:
        writer.writerow(row)

print(f"Generated {len(CANDIDATE_DATA)} candidates in dataset/candidates.csv")
