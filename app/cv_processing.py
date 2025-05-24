import PyPDF2
import spacy
import re
from collections import Counter

import matplotlib.pyplot as plt
import base64
from io import BytesIO
import random


import matplotlib
matplotlib.use('Agg')  # Use this to prevent Tkinter GUI issues


nlp = spacy.load("en_core_web_sm")





def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text


def extract_contact_info(text):
    email = re.findall(r'\S+@\S+', text)
    github = re.findall(r'https?://(?:www\.)?github\.com/[^\s]+', text)
    linkedin = re.findall(r'https?://(?:www\.)?linkedin\.com/[^\s]+', text)
    return {
        'email': email[0] if email else None,
        'github': github[0] if github else None,
        'linkedin': linkedin[0] if linkedin else None
    }




# Define dictionaries for technical skills
skills_keywords = {
    'Programming Languages': [
        'Python', 'Java', 'C', 'C++', 'C#', 'JavaScript', 'TypeScript', 'PHP', 'Ruby', 'Go', 'Swift', 'Kotlin', 'Rust'
    ],
    'Frameworks and Libraries': [
        'React', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring', 'Laravel', 'Vue.js', 'Bootstrap', 'TensorFlow',
        'Keras', 'PyTorch', 'jQuery', 'Express', 'Next.js', 'Spring Boot', 'Material UI', 'Hibernate', 'FastAPI'
    ],
    'Databases': [
        'MySQL', 'MongoDB', 'PostgreSQL', 'SQLite', 'Oracle', 'SQL Server', 'Firebase', 'DynamoDB', 'Redis'
    ],
    'Cloud Platforms': [
        'AWS', 'Azure', 'Google Cloud', 'Firebase', 'Heroku', 'DigitalOcean', 'Cloudflare', 'IBM Cloud'
    ],
    'Tools and Technologies': [
        'Docker', 'Kubernetes', 'Git', 'GitHub', 'GitLab', 'JIRA', 'Bitbucket', 'Jenkins', 'Ansible', 'Terraform',
        'CI/CD', 'Serverless', 'Kibana', 'Elasticsearch', 'Logstash', 'Splunk', 'Figma', 'Postman'
    ],
    'Development Methodologies': [
        'Agile', 'Scrum', 'Kanban', 'DevOps', 'Waterfall', 'Test-Driven Development', 'Behavior-Driven Development'
    ]
}

# Combine all technical skills into a single list for easier matching
all_technical_skills = [skill for category in skills_keywords.values() for skill in category]

    

# Function to extract technical skills from project descriptions
def extract_technical_skills_from_projects(text):

    
    doc = nlp(text.lower())
    extracted_technical_skills = []
    for sentence in doc.sents:
        sentence_text = sentence.text.strip()
        for skill in all_technical_skills:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', sentence_text):
                extracted_technical_skills.append(skill)
    return extracted_technical_skills

# Function to generate and return the base64-encoded skills bar chart
def generate_and_store_skills_chart(skill_counts):
    # Extract skill names and their counts
    skills = list(skill_counts.keys())
    counts = list(skill_counts.values())

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(skills, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Technical Skills')
    plt.title('Technical Skills Extracted from Resume')
    plt.tight_layout()

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the image to base64
    chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return chart_base64

def extract_programming_languages(text):
    programming_languages = [
        'Python', 'Java', 'C', 'C\\+\\+', 'C#', 'JavaScript', 'Ruby', 'Go', 'Swift', 'Kotlin', 'PHP',
        'TypeScript', 'R', 'Perl', 'Objective-C', 'Rust', 'Scala', 'Dart', 'Haskell', 'MATLAB',
        'Shell', 'PowerShell', 'SQL', 'Bash', 'HTML', 'CSS', 'SASS', 'Fortran', 'COBOL'
    ]
    
    found_languages = []

    programming_languages_escaped = [re.escape(lang) for lang in programming_languages]
    pattern = re.compile(r'\b(' + '|'.join(programming_languages_escaped) + r')\b', re.IGNORECASE)
    matches = pattern.findall(text)
    found_languages.extend(set(matches))

    doc = nlp(text)
    for sent in doc.sents:
        sentence_text = sent.text.lower()
        for lang in programming_languages:
            if lang.lower() in sentence_text and lang not in found_languages:
                found_languages.append(lang)

    return len(found_languages)

def extract_website_development_technologies(text):
    web_technologies = [
        'HTML', 'CSS', 'JavaScript', 'TypeScript', 'PHP', 'Ruby', 'Python', 'Java', 'C#', 
        'React', 'Angular', 'Vue.js', 'Svelte', 'Bootstrap', 'Tailwind CSS', 'jQuery', 
        'Node.js', 'Express', 'Next.js', 'Nuxt.js', 'Django', 'Flask', 'Laravel', 'ASP.NET',
        'Ruby on Rails', 'Spring', 'WordPress', 'Magento', 'Shopify', 'Joomla', 'Drupal',
        'Firebase', 'MongoDB', 'MySQL', 'PostgreSQL', 'SQLite', 'Redis', 'GraphQL', 'REST API',
        'WebSockets', 'Webpack', 'Gulp', 'Grunt', 'Parcel', 'Sass', 'LESS', 'JSON', 'AJAX',
        'WebAssembly', 'Three.js', 'Babel', 'Handlebars', 'Pug', 'Materialize', 'Foundation'
    ]
    
    found_web_technologies = []

    pattern = re.compile(r'\b(' + '|'.join(web_technologies) + r')\b', re.IGNORECASE)
    matches = pattern.findall(text)
    found_web_technologies.extend(set(matches))

    doc = nlp(text)
    for sent in doc.sents:
        sentence_text = sent.text.lower()
        if 'web development' in sentence_text or 'website' in sentence_text:
            for tech in web_technologies:
                if tech.lower() in sentence_text and tech not in found_web_technologies:
                    found_web_technologies.append(tech)

    return len(found_web_technologies)

def extract_programming_frameworks(text):
    frameworks = [
        'Django', 'Flask', 'React', 'Angular', 'Vue.js', 'Spring', 'Express', 'Rails', 'Ruby on Rails',
        'Laravel', 'ASP.NET', 'Node.js', 'Next.js', 'Bootstrap', 'Tailwind CSS', 'Foundation',
        'jQuery', 'Svelte', 'Nuxt.js', 'Redux', 'Keras', 'TensorFlow', 'Pandas', 'Hadoop',
        'Spark', 'Vue', 'Symfony', 'Zend', 'CakePHP', 'Meteor', 'FastAPI', 'Quasar', 'Phoenix', 'Ionic',
        'React Native', 'Electron', 'Flutter', 'Backbone.js', 'Alpine.js', 'NestJS', 'Struts', 'Sequelize',
        'CodeIgniter', 'Play Framework', 'Vaadin', 'Gatsby', 'Ember.js', 'MobX', 'CouchDB', 'RxJava'
    ]
    
    found_frameworks = []

    pattern = re.compile(r'\b(' + '|'.join(frameworks) + r')\b', re.IGNORECASE)
    matches = pattern.findall(text)
    found_frameworks.extend(set(matches))

    doc = nlp(text)
    for sent in doc.sents:
        sentence_text = sent.text.lower()
        for framework in frameworks:
            if framework.lower() in sentence_text and framework not in found_frameworks:
                found_frameworks.append(framework)

    return len(found_frameworks)

def extract_cloud_technologies(text):
    cloud_technologies = [
        'AWS', 'Amazon Web Services', 'Azure', 'Google Cloud', 'GCP', 'IBM Cloud', 'Oracle Cloud',
        'DigitalOcean', 'Alibaba Cloud', 'Salesforce', 'SAP Cloud', 'Cloud Foundry', 'Heroku', 
        'Red Hat OpenShift', 'VMware Cloud', 'Rackspace', 'Linode', 'Cloudflare', 'Backblaze',
        'Kubernetes', 'Docker', 'Terraform', 'Ansible', 'CloudFormation', 'Pulumi', 'Spinnaker', 
        'Vault', 'Consul', 'Istio', 'Anthos', 'Cloud Functions', 'Lambda', 'Azure Functions', 
        'Google Cloud Functions', 'Serverless', 'ECS', 'EKS', 'Fargate', 'AKS', 'OpenStack', 'VPC',
        'EC2', 'S3', 'RDS', 'BigQuery', 'Cloud Storage', 'Cloud Run', 'Elastic Beanstalk', 
        'CloudWatch', 'CloudTrail', 'CloudFront', 'IAM', 'Load Balancer', 'Auto Scaling', 'S3 Buckets'
    ]
    
    found_technologies = []

    pattern = re.compile(r'\b(' + '|'.join(cloud_technologies) + r')\b', re.IGNORECASE)
    matches = pattern.findall(text)
    found_technologies.extend(set(matches))

    doc = nlp(text)
    for sent in doc.sents:
        sentence_text = sent.text.lower()
        if 'cloud' in sentence_text or 'deployment' in sentence_text:
            for tech in cloud_technologies:
                if tech.lower() in sentence_text and tech not in found_technologies:
                    found_technologies.append(tech)

    return len(found_technologies)

def extract_devops_technologies(text):
    devops_tools = [
        'Jenkins', 'GitLab CI', 'GitHub Actions', 'Travis CI', 'CircleCI', 'TeamCity', 'Bamboo',
        'ArgoCD', 'Spinnaker', 'Flux', 'Harness', 'Azure DevOps', 'Octopus Deploy', 'CodePipeline',
        'Docker', 'Kubernetes', 'Ansible', 'Terraform', 'Chef', 'Puppet', 'Nagios', 'Prometheus',
        'Grafana', 'Elastic Stack', 'ELK Stack', 'Splunk', 'New Relic', 'AppDynamics', 'Sentry',
        'Consul', 'Vault', 'Istio', 'Linkerd', 'Nginx', 'Apache Kafka', 'AWS CodeDeploy', 'CloudFormation',
        'SaltStack', 'OpenShift', 'Vagrant'
    ]
    
    found_tools = []

    pattern = re.compile(r'\b(' + '|'.join(devops_tools) + r')\b', re.IGNORECASE)
    matches = pattern.findall(text)
    found_tools.extend(set(matches))

    doc = nlp(text)
    for sent in doc.sents:
        sentence_text = sent.text.lower()
        if 'ci/cd' in sentence_text or 'devops' in sentence_text:
            for tool in devops_tools:
                if tool.lower() in sentence_text and tool not in found_tools:
                    found_tools.append(tool)

    return len(found_tools)

def extract_version_control_technologies(cv_text):
    version_control_tools = [
        "Git", "SVN", "Subversion", "Mercurial", "Perforce", "Bazaar", 
        "GitHub", "GitLab", "Bitbucket", "Azure DevOps", "SourceForge",
        "TortoiseSVN", "SmartGit", "GitKraken", "SourceTree"
    ]
    
    vc_pattern = re.compile(r'\b(' + '|'.join(re.escape(tool) for tool in version_control_tools) + r')\b', re.IGNORECASE)
    found_tools = set(vc_pattern.findall(cv_text))

    doc = nlp(cv_text)
    verified_tools = []
    for sent in doc.sents:
        sentence_text = sent.text.strip()
        for tool in found_tools:
            if tool.lower() in sentence_text.lower():
                verified_tools.append(tool)
    
    verified_tools = list(set(verified_tools))
    return len(verified_tools)

def extract_database_technologies(cv_text):
    database_technologies = [
        "MySQL", "PostgreSQL", "SQLite", "Oracle Database", "SQL Server", "MongoDB", "Cassandra",
        "DynamoDB", "CouchDB", "Redis", "Firebase", "Snowflake", "Redshift", "BigQuery",
        "Neo4j", "JanusGraph", "ArangoDB", "Elasticsearch", "MariaDB", "CockroachDB", 
        "HBase", "ClickHouse"
    ]
    
    db_pattern = re.compile(r'\b(' + '|'.join(re.escape(db) for db in database_technologies) + r')\b', re.IGNORECASE)
    found_databases = set(db_pattern.findall(cv_text))
    
    doc = nlp(cv_text)
    verified_databases = []
    for sent in doc.sents:
        sentence_text = sent.text.strip()
        for db in found_databases:
            if db.lower() in sentence_text.lower():
                verified_databases.append(db)
    
    verified_databases = list(set(verified_databases))
    return len(verified_databases)


def extract_software_development_methodologies(cv_text):
    methodologies = [
        'Agile', 'Scrum', 'Kanban', 'Waterfall', 'Lean', 
        'Extreme Programming (XP)', 'DevOps', 'Spiral', 'RAD', 
        'V-Model', 'Incremental Development', 'Iterative Development', 
        'Prototyping'
    ]

    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(method) for method in methodologies) + r')\b', re.IGNORECASE)

    found_methodologies = pattern.findall(cv_text)

    return len(list(dict.fromkeys(found_methodologies)))








technology_categories = {
    'Databases': ['MySQL', 'MongoDB', 'PostgreSQL', 'SQLite', 'Oracle', 'SQL Server', 'Firebase', 'DynamoDB', 'Redis'],
    'Programming Languages': ['Python', 'Java', 'C', 'C++', 'C#', 'JavaScript', 'Ruby', 'Go', 'Swift', 'Kotlin', 'PHP'],
    'Frameworks': ['React', 'Angular', 'Django', 'Flask', 'Spring', 'Laravel', 'Vue.js', 'TensorFlow', 'Keras', 'PyTorch'],
    'DevOps Tools': ['Docker', 'Kubernetes', 'Git', 'Jenkins', 'Ansible', 'Terraform', 'CI/CD', 'Grafana', 'Prometheus'],
    'Cloud Platforms': ['AWS', 'Azure', 'Google Cloud', 'Firebase', 'Heroku', 'DigitalOcean', 'Cloudflare'],
    'Version Control': ['Git', 'SVN', 'Bitbucket', 'GitHub', 'GitLab', 'Mercurial'],
    'Software Development Methodologies': ['Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'TDD', 'BDD'],
    'Software Architectures': ['Microservices', 'Monolithic', 'Serverless', 'Event-driven', 'Layered', 'MVC'],
}

# Function to extract technologies and their counts
def extract_technologies(text, category):
    extracted = {tech: 0 for tech in technology_categories[category]}  # Ensure all technologies are represented
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, technology_categories[category])) + r')\b', re.IGNORECASE)
    matches = pattern.findall(text)
    counts = Counter(matches)
    
    for tech in extracted.keys():
        extracted[tech] = counts.get(tech, 0)
    
    return extracted

# Function to generate and return base64-encoded chart
def generate_chart(technologies, title):
    if not technologies:
        return None
    
    labels = list(technologies.keys())
    counts = list(technologies.values())
    
    colors = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in labels]
    
    plt.figure(figsize=(12, 6))
    plt.barh(labels, counts, color=colors)
    plt.xlabel('Frequency')
    plt.ylabel(title)
    plt.title(f'{title} Distribution')
    plt.xticks(range(max(counts) + 1))
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Function to generate and store all charts
def generate_all_charts(cv_text):
    charts = {}
    
    for category in technology_categories.keys():
        extracted = extract_technologies(cv_text, category)
        charts[category] = {
            'data': extracted,
            'chart': generate_chart(extracted, category)
        }
    
    return charts



import re
from typing import List, Dict
import spacy

# ─────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────
nlp = spacy.load("en_core_web_sm")

# ALL high-level sections we might meet
_SECTION_BREAKERS = {
    # core sections
    "profile", "summary", "objective",
    "professional experience", "work experience", "experience", "employment",
    "projects", "technical projects", "side projects", "academic projects", "project experience",
    "research projects", "industry based project",
    "courses", "courses & certifications", "certifications", "training",
    "achievements", "awards", "honors", "accomplishments",
    "skills", "technical skills", "languages", "employment history","other experience",
    "education",
    # extras
    "publications", "volunteering", "volunteer",
    "interests", "hobbies",
    "references", "referees", "contact", "extra-curricular"
}

def _is_section_break(line: str) -> bool:
    """Return True if the line looks like a high-level heading."""
    l = line.strip()
    if len(l) > 70:
        return False
    plain = re.sub(r"[^A-Za-z &]", "", l).lower().strip()
    return plain in _SECTION_BREAKERS or l.isupper()

def _dedupe(items: List[str]) -> List[str]:
    seen, out = set(), []
    for itm in items:
        key = re.sub(r"\s+", " ", itm.strip().lower())
        if key and key not in seen:
            seen.add(key)
            out.append(itm.strip())
    return out

def _capture_by_heading(cv_text: str,
                        heading_keywords: List[str],
                        min_words: int = 4) -> List[str]:
    """
    Grab *every* section whose heading contains any keyword.
    """
    lines = cv_text.splitlines()
    blocks, current, capture = [], [], False

    for raw in lines:
        line = raw.rstrip()
        lower = line.lower().strip()

        # Start a wanted section?
        if any(k in lower for k in heading_keywords):
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            capture = True
            continue

        # End of current section?
        if capture and (_is_section_break(line) or not line.strip()):
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            capture = False
            continue

        if capture:
            current.append(line)

    if current:
        blocks.append("\n".join(current).strip())

    return [b for b in blocks if len(b.split()) >= min_words]



def _find_bullets_matching(cv_text: str,
                           include_kw: List[str],
                           exclude_kw: List[str] = None,
                           min_words: int = 4) -> List[str]:
    """
    Look for single-line bullets that contain *any* include_kw and *no* exclude_kw.
    """
    if exclude_kw is None:
        exclude_kw = []
    lines, hits, i = cv_text.splitlines(), [], 0

    # pre-compile for speed
    inc_re = re.compile("|".join([re.escape(k.lower()) for k in include_kw]))
    exc_re = re.compile("|".join([re.escape(k.lower()) for k in exclude_kw])) if exclude_kw else None

    while i < len(lines):
        line_raw = lines[i]
        line = line_raw.lstrip("•–—-•* ").strip()           # drop leading bullet/dash
        lower = line.lower()

        if (inc_re.search(lower) and not (exc_re and exc_re.search(lower))):
            block = [line.strip()]
            j = i + 1
            while (j < len(lines) and lines[j].strip()
                   and not _is_section_break(lines[j])
                   and not re.match(r"^[\u2022•\-–—*]", lines[j].lstrip())):
                block.append(lines[j].strip())
                j += 1
            if len(" ".join(block).split()) >= min_words:
                hits.append(" ".join(block))
            i = j
        else:
            i += 1
    return hits




# ─────────────────────────────────────────────────────────────
# Split a long Experience block into per-job chunks
# ─────────────────────────────────────────────────────────────

# Accept headings of the form:
# • Senior Software Engineer – Payments – Square
#   Trainee Software Engineer | Fortunaglobal | Aug 2019 – Feb 2020
#   Software Engineering Intern at WSO2
_JOB_HEADER = re.compile(
    r"""^(?:[\u2022•\-–—*]\s*)?                 # optional bullet
        [A-Z][\w &/().+'\-]{2,}                # role (starts with cap)
        (?:\s+(?:–|—|\-|‒|–|—| at | \| ))      # separator
        .+?$                                   # company / team text
    """,
    re.VERBOSE
)

def _split_jobs_in_block(block: str) -> List[str]:
    """
    Inside one long Professional Experience block, slice it
    into separate jobs by detecting header lines.
    """
    lines = block.splitlines()
    jobs, current = [], []

    for line in lines:
        if _JOB_HEADER.match(line.strip()):
            if current:
                jobs.append("\n".join(current).strip())
                current = []
        current.append(line)
    if current:
        jobs.append("\n".join(current).strip())

    return jobs

# ─────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────

def extract_work_experience(cv_text: str) -> List[str]:
    # 1. Capture every Experience-type section
    raw_blocks = _capture_by_heading(
        cv_text,
        ["professional experience", "work experience", "experience",
         "employment", "employment history", "career history"]
    )

    # 2. Split those blocks into distinct jobs
    jobs = []
    for blk in raw_blocks:
        jobs.extend(_split_jobs_in_block(blk))

    # 3. Find any stray job bullets elsewhere
    date_pattern = r"\b(20\d{2}|19\d{2})"

    extra_bullets = _find_bullets_matching(
        cv_text,
        include_kw=[
            # roles & levels
            "engineer", "developer", "programmer", "architect", "analyst",
            "consultant", "scientist", "technician", "administrator",
            "specialist", "lead", "senior", "principal", "staff",
            "associate", "intern", "trainee", "co-founder", "founder",
            "lecturer", "mentor", "manager", "director",
            "undergraduate trainee", 
            "software engineer intern",
            "software engineering", "software engineer","associate software engineer",

            "principal software engineer","techlead","senior software engineer",
            "software architect","senior software developer","junior software engineer","backend engineer","mobile app developer",
            " lead software engineer","full stack developer",

            # domains
            "full-stack", "backend", "front-end", "devops", "mobile",
            "data", "machine learning", "ai", "blockchain", "cloud"
        ],
        exclude_kw=[
            "course", "courses","project", "projects"," tools and technologies", "tools", "tools used","technologies", "technologies used",
            "certificate", "certification", "training", "workshop","technial projects",
            "award","Certified", "achievement", "honor", "hobbies", "interests",
            "objective", "summary", "profile", "skills", "languages",
            "volunteer", "volunteering", "publication", "publications",
            "reference", "referees", "contact", "competition", "club", "university",
            "school", "college", "degree"
        ]
    )

    # Keep only bullets that reference a calendar year (strong signal of a job)
    extra_bullets = [b for b in extra_bullets if re.search(date_pattern, b)]

    return _dedupe(jobs + extra_bullets)


# ─────────────────────────────────────────────────────────────
# 2. Courses & Certifications  (unchanged)
# ─────────────────────────────────────────────────────────────
def extract_courses_certifications_achievements(cv_text: str) -> List[Dict[str, str]]:
    heading_blocks = _capture_by_heading(
        cv_text,
        ["certification", "course", "training", "workshop", "license"]
    )
    bullet_blocks = _find_bullets_matching(
        cv_text,
        include_kw=["certificate", "courses & certifications", "certification", "certified",
                    "course", "training", "workshop", "bootcamp", "practitioner"],
        exclude_kw=["award", "achievement", "honor", "Excellence", "project", "experience","projects", "tools and technologies", "tools", "work experience","internship", "other experience", "references", "referee", "contact", "about", "Senior Software Engineer", "Software Engineer"]
    )
    combined = _dedupe(heading_blocks + bullet_blocks)
    return [{"type": "Courses/Certifications", "content": item} for item in combined]





# ─────────────────────────────────────────────────────────────
#  KEYWORD TABLES — ***ONLY PARTS THAT CHANGED*** 
#  (expanded to cover every phrase visible in your screenshots)
# ─────────────────────────────────────────────────────────────

_PROJECT_KEYWORDS = (
    # generic
    "project", "projects", "prototype", "system", "application", "app",
    "platform", "framework", "engine", "tool", "solution", "portal",
    "service", "microservice", "component", "module",
    "optimizer", "replicator", "detector", "assistant",
    # domain-specific additions from samples
    "website", "web site", "web app", "mobile application", "mobile app",
    "e-commerce", "inventory", "management system", "monitoring",
    "booking", "timetable", "gateway", "calculator", "language",
    "compiler", "etl", "iot", "ai", "device", "robot", "sensor",
    "middleware", "chatbot", "data lake", "analytics", "dashboard"
)

_ACTION_VERBS = (
    # core
    "built", "developed", "created", "implemented", "engineered", "designed",
    "crafted", "modernised", "constructed", "delivered", "refactored",
    "automated", "optimised", "prototyped", "integrated", "migrated",
    # extra verbs that appeared in samples
    "architected", "contributed", "launched", "deployed",
    "led", "rolled", "designed", "assembled", "customised"
)

_EXCLUDE_RE = re.compile(
    r"(email|phone|address|linkedin|referee?s?|references?|"
    r"\bcourses?\b|\bcertifications?\b|\bawards?\b|\bachievements?\b|"
    r"\bexperience\b|https?://|@\w+)",
    re.I
)

_PROJECT_HEADINGS = [
    "project", "projects", "project experience",
    "technical project", "technical projects",
    "academic project", "academic projects",
    "industry based project", "industry based projects",
    "research project", "research projects",
    "side project", "side projects", "other projects"
]

def _word_found(text: str, words) -> bool:
    return any(re.search(rf"\b{re.escape(w)}\b", text, re.I) for w in words)

# ─────────────────────────────────────────────────────────────
#  Loose-bullet scanner
# ─────────────────────────────────────────────────────────────
def _find_project_bullets(cv_text: str,
                          min_words: int = 5) -> List[str]:
    lines = cv_text.splitlines()
    bullets, i = [], 0

    while i < len(lines):
        line = lines[i].strip()
        if (_word_found(line, _PROJECT_KEYWORDS) and
                not _EXCLUDE_RE.search(line)):
            block = [line]
            j = i + 1
            while (j < len(lines) and lines[j].strip()
                   and not _is_section_break(lines[j])
                   and not re.match(r"^[\u2022•\-–]", lines[j].lstrip())):
                block.append(lines[j].strip())
                j += 1
            joined = " ".join(block)
            if (len(joined.split()) >= min_words and
                    _word_found(joined, _ACTION_VERBS)):
                bullets.append(joined)
            i = j
        else:
            i += 1
    return bullets



def extract_project_experiences(cv_text: str) -> List[str]:
    """
    Return only project descriptions (academic, industry, hobby).
    Steps:
      1. Capture blocks under headings that match any of _PROJECT_HEADINGS.
      2. Find stray project bullets anywhere in the text.
      3. Split each heading block on:
         • blank lines, or
         • lines beginning with “Technologies:”, “Technologies used:”, or “Tools and Technologies:”
      4. Deduplicate and return.
    """
    # a. Heading-based capture
    heading_blocks = _capture_by_heading(cv_text, _PROJECT_HEADINGS)

    # b. Bullet capture
    bullet_blocks = _find_project_bullets(cv_text)

    # c. Split big heading blocks into individual project items
    project_items = []
    split_pattern = (
        r"(?:\n\s*\n)"                            # blank line
        r"|(?:\n\s*(?:Technologies"
           r"|Technologies used"
           r"|Tools and Technologies):)"          # any of those labels + colon
    )
    for blk in heading_blocks:
        for para in re.split(split_pattern, blk, flags=re.IGNORECASE):
            t = para.strip()
            if (len(t.split()) >= 5
                    and _word_found(t, _PROJECT_KEYWORDS)
                    and not _EXCLUDE_RE.search(t)):
                project_items.append(t)

    # d. Merge and remove duplicates
    return _dedupe(project_items + bullet_blocks)

# ─────────────────────────────────────────────────────────────
#  Achievements extractor (unchanged)
# ─────────────────────────────────────────────────────────────
def extract_achievements(cv_text: str) -> List[str]:
    heading_blocks = _capture_by_heading(
        cv_text,
        heading_keywords=["achievement", "awards", "honor",
                          "accomplishment", "distinction"]
    )

    ach_kw = {
        "achievement", "accomplishment", "award", "recognition", "honor",
        "winner", "finalist", "ranked", "scholarship", "grant", "medal",
        "best", "top", "prize", "distinction"
    }

    doc = nlp(cv_text)
    sent_hits = [s.text.strip() for s in doc.sents
                 if len(s.text.strip()) >= 15 and
                 any(k in s.text.lower() for k in ach_kw)]

    combined = _dedupe(heading_blocks + sent_hits)

    # prune phrases like “Best practices …”
    return [s for s in combined
            if not re.search(r"\b(best practices?|job|project|experience)\b", s, re.I)]





# ─────────────────────────────────────────────────────────────
# 4. Achievements / Awards
# ─────────────────────────────────────────────────────────────
def extract_achievements(cv_text: str) -> List[str]:
    """
    Returns list[str] of notable awards / honors.
    """
    heading_blocks = _capture_by_heading(
        cv_text,
        heading_keywords=["achievement", "awards", "honor", "accomplishment", "distinction"]
    )

    # sentence-level scan using a curated keyword list
    achievement_keywords = {
        "achievement", "accomplishment", "award", "recognition", "honor",
        "winner", "finalist", "ranked", "scholarship", "grant", "medal",
        "best", "top", "prize", "distinction"
    }

    doc = nlp(cv_text)
    sent_hits = []
    for sent in doc.sents:
        s = sent.text.strip()
        if len(s) < 15:
            continue
        lower = s.lower()
        if any(k in lower for k in achievement_keywords):
            sent_hits.append(s)

    combined = _dedupe(heading_blocks + sent_hits)

    # final filter to avoid false positives like “Best practices”
    final = [s for s in combined
             if not re.search(r"\b(best practices?|job|project|experience)\b", s, re.I)]
    return final
