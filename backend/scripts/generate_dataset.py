import json
import os

# Define the topics, subtopics, categories, difficulties, and concepts
dataset_config = {
    "Technology": {
        "Artificial Intelligence": {
            "subtopic": "AI Fundamentals",
            "concepts": [
                "natural language processing", "reinforcement learning", "heuristic search", "large language models",
                "semantic web", "expert systems", "knowledge representation", "computer vision", "speech recognition",
                "artificial general intelligence", "turing test", "agent-based modeling", "prompt engineering",
                "fine-tuning LLMs", "generative adversarial networks", "AI ethics", "explainable AI", "bias in AI systems",
                "cognitive computing", "pattern recognition", "automated reasoning", "symbolic AI", "fuzzy logic",
                "genetic algorithms", "machine translation", "chatbot architecture", "Retrieval-Augmented Generation (RAG)",
                "vector databases in AI", "parameter-efficient fine-tuning (PEFT)", "hallucination in LLMs", "zero-shot learning",
                "few-shot learning", "semantic search", "sentiment analysis", "named entity recognition", "speech-to-text",
                "text-to-speech", "AI safety guardrails", "RLHF (Reinforcement Learning from Human Feedback)", "intelligent agents",
                "swarm intelligence", "decision trees in AI", "ontologies in AI", "deep reinforcement learning",
                "multi-agent systems", "autonomous driving systems", "AI-driven diagnostics", "conversational agents",
                "search algorithms in AI", "knowledge graphs", "recommendation systems", "adversarial attacks",
                "AI policy and governance", "edge AI", "robotic process automation (RPA)", "cognitive agents",
                "logical reasoning agents", "contextual understanding in LLMs", "transformer models", "supervised pre-training"
            ]
        },
        "Machine Learning": {
            "subtopic": "ML Core Concepts",
            "concepts": [
                "supervised learning", "unsupervised learning", "semi-supervised learning", "active learning",
                "linear regression", "logistic regression", "support vector machines", "decision trees",
                "random forests", "gradient boosting machines", "XGBoost", "k-nearest neighbors",
                "k-means clustering", "hierarchical clustering", "dimensionality reduction", "principal component analysis (PCA)",
                "feature engineering", "cross-validation", "overfitting and underfitting", "regularization techniques (L1/L2)",
                "bias-variance tradeoff", "model evaluation metrics", "confusion matrix", "precision and recall",
                "F1-score", "ROC-AUC curve", "hyperparameter tuning", "grid search and random search",
                "ensemble learning", "bagging and boosting", "naive Bayes classifier", "association rule learning",
                "Apriori algorithm", "anomaly detection", "t-SNE visualization", "recommender systems algorithms",
                "collaborative filtering", "content-based filtering", "matrix factorization", "gradient descent optimization",
                "stochastic gradient descent", "learning rate scheduling", "backpropagation", "loss functions",
                "mean squared error loss", "cross-entropy loss", "model deployment pipeline", "data preprocessing steps",
                "missing value imputation", "feature scaling and normalization", "one-hot encoding", "label encoding",
                "class imbalance handling", "synthetic minority oversampling (SMOTE)", "time series forecasting",
                "autoregressive models (ARIMA)", "statistical learning theory", "PAC learning framework", "kernel trick", "linear discriminant analysis"
            ]
        },
        "Deep Learning": {
            "subtopic": "Neural Networks & Deep Architectures",
            "concepts": [
                "artificial neural networks", "multilayer perceptrons", "activation functions", "sigmoid activation",
                "ReLU activation function", "LeakyReLU activation", "softmax activation function", "backpropagation algorithm",
                "vanishing gradient problem", "exploding gradient problem", "convolutional neural networks (CNNs)",
                "pooling layers in CNNs", "convolution operations", "recurrent neural networks (RNNs)",
                "long short-term memory (LSTM)", "gated recurrent units (GRU)", "attention mechanisms", "self-attention layers",
                "transformer architectures", "bidirectional encoder representations (BERT)", "generative pre-trained transformers (GPT)",
                "generative adversarial networks (GANs)", "autoencoders", "variational autoencoders (VAEs)",
                "transfer learning in deep learning", "fine-tuning pre-trained networks", "word embeddings", "Word2Vec embeddings",
                "GloVe embeddings", "fastText embeddings", "dense embeddings", "dropout regularization",
                "batch normalization", "layer normalization", "optimization algorithms", "Adam optimizer",
                "RMSprop optimizer", "tensor operations", "GPU acceleration in deep learning", "deep belief networks",
                "feedforward neural networks", "residual neural networks (ResNet)", "sequence-to-sequence models", "encoder-decoder networks",
                "unsupervised pre-training", "contrastive learning", "self-supervised learning", "neural architecture search",
                "multimodal deep learning", "diffusion models", "latent spaces", "vector quantization",
                "backpropagation through time (BPTT)", "spatial pyramid pooling", "dilated convolutions", "depthwise separable convolutions",
                "attention pooling", "multi-head attention", "positional encodings", "vision transformers (ViT)", "few-shot learning in neural networks"
            ]
        },
        "Data Science": {
            "subtopic": "Data Analysis & Visualization",
            "concepts": [
                "exploratory data analysis", "descriptive statistics", "inferential statistics", "hypothesis testing",
                "p-value significance", "confidence intervals", "probability distributions", "normal distribution",
                "central limit theorem", "correlation and covariance", "Pearson correlation", "Spearman rank correlation",
                "data cleaning techniques", "handling outliers", "data visualization principles", "histograms",
                "scatter plots", "box plots", "heatmaps", "line charts",
                "bar charts", "pie charts and usage warnings", "interactive dashboards", "Tableau visualization",
                "PowerBI dashboards", "matplotlib plotting library", "seaborn visualization library", "pandas dataframes",
                "data aggregation", "group by operations", "joining and merging datasets", "pivot tables",
                "feature selection methods", "collinearity and multicollinearity", "variance inflation factor (VIF)", "dimensionality reduction methods",
                "principal component analysis (PCA)", "exploratory factor analysis", "A/B testing methodologies", "statistical power",
                "chi-square test", "t-test comparison", "ANOVA (Analysis of Variance)", "non-parametric tests",
                "Mann-Whitney U test", "Kruskal-Wallis test", "data wrangling", "ETL pipelines",
                "data warehousing concepts", "SQL queries for data science", "NoSQL databases usage", "big data frameworks",
                "Apache Spark", "Hadoop ecosystem", "predictive modeling", "feature importance analysis",
                "data science lifecycle", "CRISP-DM methodology", "reproducible research in data science", "Jupyter notebook workflows"
            ]
        },
        "Programming": {
            "subtopic": "Languages & Algorithms",
            "concepts": [
                "object-oriented programming", "classes and objects", "inheritance", "polymorphism",
                "encapsulation", "abstraction", "functional programming", "recursion",
                "data structures", "arrays and linked lists", "stacks and queues", "trees and graphs",
                "binary search trees", "hash tables", "sorting algorithms", "bubble sort",
                "quick sort", "merge sort", "heap sort", "searching algorithms",
                "binary search", "linear search", "depth-first search (DFS)", "breadth-first search (BFS)",
                "Dijkstra's shortest path algorithm", "greedy algorithms", "dynamic programming", "divide and conquer",
                "time complexity and Big O notation", "space complexity analysis", "pointers and memory management", "garbage collection",
                "exception handling", "concurrency and multithreading", "asynchronous programming", "APIs design patterns",
                "Python decorators", "Python generators", "Java interfaces", "JavaScript closures",
                "JavaScript prototypes", "C++ templates", "compiler design basics", "interpreters vs compilers",
                "regular expressions", "string manipulation algorithms", "bit manipulation", "matrix multiplication algorithms",
                "cryptographic hashing algorithms", "version control concepts", "Git branching models", "test-driven development (TDD)",
                "unit testing frameworks", "design patterns (Singleton, Factory)", "refactoring techniques", "software development lifecycle"
            ]
        },
        "Web Development": {
            "subtopic": "Frontend, Backend & APIs",
            "concepts": [
                "HTML5 semantic structure", "CSS3 styling and layouts", "CSS grid systems", "CSS flexbox layouts",
                "responsive web design", "media queries", "JavaScript DOM manipulation", "modern JavaScript (ES6+)",
                "asynchronous JavaScript (promises, async/await)", "React library", "React components state and props", "React hooks (useState, useEffect)",
                "React context API", "Redux state management", "single page applications (SPA)", "client-side routing",
                "server-side rendering (SSR)", "static site generation (SSG)", "Next.js framework", "Node.js runtime",
                "Express.js framework", "RESTful API design", "GraphQL APIs", "WebSocket communication",
                "JSON web tokens (JWT) authentication", "session-based authentication", "cross-origin resource sharing (CORS)", "HTTP request methods",
                "HTTP status codes", "cookies and local storage", "web security basics", "cross-site scripting (XSS) prevention",
                "cross-site request forgery (CSRF) protection", "content security policy (CSP)", "web performance optimization", "lazy loading assets",
                "bundlers and build tools", "Webpack and Vite", "npm and yarn package managers", "CSS preprocessors (SASS/SCSS)",
                "TailwindCSS utility framework", "Bootstrap framework", "accessibility standards (WCAG)", "SEO best practices",
                "Progressive Web Apps (PWA)", "service workers", "web hosting options", "serverless functions",
                "API rate limiting", "database integration in web apps", "middleware in backend routing", "templating engines",
                "MVC architecture pattern", "single-origin policy", "web browsers rendering engine", "virtual DOM vs real DOM",
                "state hydration", "event bubbling and capturing", "AJAX requests", "fetch API usage"
            ]
        },
        "Database": {
            "subtopic": "SQL & NoSQL Management",
            "concepts": [
                "relational databases", "non-relational databases (NoSQL)", "Structured Query Language (SQL)", "database schemas",
                "primary keys and foreign keys", "entity-relationship diagrams (ERD)", "database normalization (1NF, 2NF, 3NF)", "denormalization",
                "database indexing", "B-tree indexes", "hash indexes", "composite indexes",
                "database transactions", "ACID properties", "concurrency control", "database locks",
                "stored procedures", "triggers", "database views", "subqueries and joins",
                "inner join, left join, right join", "aggregate functions in SQL", "MongoDB database", "document-store database model",
                "MongoDB collections and documents", "MongoDB aggregation framework", "MongoDB indexing strategies", "replica sets in MongoDB",
                "sharding and horizontal scaling", "CAP theorem", "BASE properties", "key-value stores",
                "column-family stores", "graph databases", "database replication", "database backups and recovery",
                "query optimization techniques", "explain plan analysis", "database migration strategies", "connection pooling",
                "object-relational mapping (ORM)", "Mongoose ODM", "SQL injection vulnerabilities", "prepared statements",
                "NoSQL document validation", "data warehousing vs databases", "OLAP vs OLTP", "distributed databases",
                "consistent hashing", "database sharding keys", "write-ahead logging", "MVCC (Multi-Version Concurrency Control)"
            ]
        },
        "Cybersecurity": {
            "subtopic": "Security Protocols & Encryption",
            "concepts": [
                "symmetric encryption", "asymmetric encryption", "public key cryptography", "hash functions (SHA-256)",
                "digital signatures", "digital certificates", "SSL/TLS handshake", "HTTPS protocol",
                "multi-factor authentication (MFA)", "biometric authentication", "role-based access control (RBAC)", "least privilege principle",
                "firewall technologies", "intrusion detection systems (IDS)", "intrusion prevention systems (IPS)", "virtual private networks (VPN)",
                "malware classification", "ransomware defense", "phishing attacks mitigation", "social engineering tactics",
                "denial of service (DoS) attacks", "distributed denial of service (DDoS)", "SQL injection prevention", "cross-site scripting (XSS) defense",
                "buffer overflow attacks", "zero-day exploits", "penetration testing methodologies", "vulnerability scanning",
                "security auditing", "risk assessment frameworks", "OWASP Top 10 vulnerabilities", "incident response plans",
                "disaster recovery planning", "security information and event management (SIEM)", "network packet sniffing", "Wireshark packet analysis",
                "port scanning concepts", "man-in-the-middle (MitM) attacks", "brute force attacks", "dictionary attacks",
                "salting and hashing passwords", "OAuth 2.0 authorization framework", "SAML authentication standard", "directory services (Active Directory)",
                "identity and access management (IAM)", "zero trust network architecture", "network segmentation", "endpoint security",
                "secure software development lifecycle (SSDLC)", "threat modeling", "security policies and governance", "compliance standards (GDPR, HIPAA)"
            ]
        },
        "Cloud Computing": {
            "subtopic": "Cloud Infrastructure & Services",
            "concepts": [
                "infrastructure as a service (IaaS)", "platform as a service (PaaS)", "software as a service (SaaS)", "public, private, and hybrid clouds",
                "Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "cloud virtualization technologies",
                "hypervisors", "cloud storage options", "object storage (Amazon S3)", "block storage (Amazon EBS)",
                "cloud database services", "Amazon RDS", "Azure SQL database", "cloud computing scalability",
                "horizontal vs vertical scaling", "load balancing algorithms", "auto-scaling groups", "serverless computing concepts",
                "AWS Lambda", "Azure Functions", "cloud networking architectures", "virtual private clouds (VPC)",
                "subnets and routing tables", "cloud security groups", "identity and access management (IAM) in cloud", "cloud billing models",
                "pay-as-you-go pricing", "cloud resource provisioning", "infrastructure as code (IaC)", "Terraform scripting",
                "AWS CloudFormation templates", "cloud migration strategies", "lift and shift migration", "disaster recovery in the cloud",
                "multi-region deployment", "cloud monitoring tools", "Amazon CloudWatch", "cloud service level agreements (SLAs)",
                "edge computing concepts", "content delivery networks (CDN)", "Amazon CloudFront", "cloud container orchestration",
                "AWS ECS", "Azure Kubernetes Service (AKS)", "cloud configuration management", "cloud elasticity principles"
            ]
        },
        "DevOps": {
            "subtopic": "CI/CD & Automation",
            "concepts": [
                "continuous integration (CI)", "continuous delivery (CD)", "CI/CD pipeline automation", "Jenkins automation server",
                "GitHub Actions workflows", "GitLab CI/CD", "containerization technologies", "Docker container engine",
                "Dockerfiles construction", "Docker Compose multi-container tools", "container image registries", "Docker Hub",
                "Kubernetes orchestration engine", "Kubernetes pods and services", "Kubernetes deployments and replicas", "Kubernetes namespaces",
                "Helm chart package manager", "configuration management systems", "Ansible automation engine", "Puppet configuration tool",
                "Chef orchestration systems", "infrastructure monitoring", "Prometheus monitoring toolkit", "Grafana dashboards visualization",
                "logging centralization", "ELK stack (Elasticsearch, Logstash, Kibana)", "site reliability engineering (SRE)", "incident management system",
                "blue-green deployment strategy", "canary deployment strategy", "rolling updates deployment", "infrastructure drift detection",
                "GitOps delivery pipelines", "ArgoCD automation tool", "secrets management systems", "HashiCorp Vault security",
                "build automation scripts", "Maven project management", "Gradle build automation", "package registry management",
                "devops cultural transformation", "collaboration tools integration", "feedback loops in software delivery", "automated testing pipelines",
                "linting and static code analysis", "vulnerability scanning in pipelines", "infrastructure provisioning speed", "zero-downtime deployments"
            ]
        }
    },
    "Education": {
        "Physics": {
            "subtopic": "Mechanics & Core Physics",
            "concepts": [
                "Newton's laws of motion", "first law of motion (inertia)", "second law of motion (F=ma)", "third law of motion (action-reaction)",
                "universal law of gravitation", "gravitational acceleration constant", "work-energy theorem", "conservation of energy",
                "kinetic energy equation", "potential energy calculations", "linear momentum conservation", "impulse and force interactions",
                "rotational dynamics", "torque and angular momentum", "centripetal acceleration forces", "Kepler's laws of planetary motion",
                "simple harmonic motion", "pendulum oscillations properties", "wave mechanics basics", "longitudinal vs transverse waves",
                "electromagnetic spectrum characteristics", "speed of light measurements", "reflection and refraction indexes", "Snell's law of refraction",
                "thermodynamics first law", "thermodynamics second law", "entropy principles in systems", "heat transfer mechanisms (conduction)",
                "convection heat transfer", "radiation heat transfer", "Coulomb's law of electrostatic force", "electric field strength",
                "Ohm's law of electrical resistance", "electric current flow", "magnetic field lines creation", "Faraday's law of electromagnetic induction",
                "Lenz's law of induced current direction", "Maxwell's equations compilation", "special relativity postulates", "time dilation effects",
                "length contraction phenomenon", "mass-energy equivalence equation (E=mc^2)", "quantum mechanics wave-particle duality", "Heisenberg's uncertainty principle",
                "Schrodinger wave equation", "photoelectric effect experiments", "Bohr model of hydrogen atom", "nuclear fission processes",
                "nuclear fusion energy generation", "radioactive decay pathways", "half-life calculation methods", "fluid mechanics principles",
                "Archimedes' buoyancy principle", "Bernoulli's fluid dynamics equation", "viscosity definitions", "speed of sound in mediums",
                "Doppler effect wave frequency shift", "Hooke's law of elasticity", "surface tension properties", "thermodynamic efficiency limits",
                "vector addition in kinematics", "projectile motion trajectories", "static equilibrium conditions", "friction coefficients (static vs kinetic)"
            ]
        },
        "Chemistry": {
            "subtopic": "Atoms, Molecules & Reactions",
            "concepts": [
                "atomic theory milestones", "subatomic particle charges (proton, neutron, electron)", "atomic number and mass number", "isotopes of elements",
                "periodic table arrangement", "periodic trends (atomic radius, electronegativity)", "valence electrons count", "octet rule principles",
                "ionic bonding mechanisms", "covalent bonding electron sharing", "metallic bonding electron seas", "Lewis dot structures drawing",
                "molecular geometry configurations", "VSEPR theory predictions", "chemical nomenclature rules", "balancing chemical equations",
                "stoichiometry mole calculations", "limiting reactant determinations", "theoretical yield calculations", "types of chemical reactions",
                "synthesis chemical reactions", "decomposition chemical reactions", "single displacement reactions", "double displacement reactions",
                "combustion reaction pathways", "acid-base neutralization reactions", "oxidation-reduction (redox) reactions", "oxidation states rules",
                "chemical equilibrium dynamics", "Le Chatelier's equilibrium principle", "equilibrium constant calculations (Kc)", "solubility product constant (Ksp)",
                "Arrhenius acids and bases", "Bronsted-Lowry acid-base theory", "Lewis acid-base definitions", "pH and pOH scale calculations",
                "buffer solutions action", "titration analysis curves", "kinetics reaction rate factors", "activation energy thresholds",
                "catalysis reaction accelerators", "ideal gas law calculations (PV=nRT)", "Boyle's gas pressure-volume law", "Charles's gas volume-temperature law",
                "Dalton's law of partial pressures", "thermochemistry enthalpy changes", "endothermic vs exothermic processes", "Gibbs free energy equations",
                "spontaneous reaction conditions", "organic chemistry carbon skeleton functional groups", "alkanes, alkenes, and alkynes", "isomers in organic chemistry",
                "polymers synthesis pathways", "periodic table group properties", "transition metal characteristic properties", "intermolecular force types",
                "hydrogen bonding strengths", "dipole-dipole interactions", "London dispersion forces", "colligative properties of solutions",
                "boiling point elevation calculations", "freezing point depression formulas", "osmotic pressure principles", "electrochemistry galvanic cells",
                "electrolytic cell reactions", "Nernst equation calculations", "Faraday's laws of electrolysis", "hybridization of carbon orbitals"
            ]
        },
        "Biology": {
            "subtopic": "Cells, Genetics & Ecology",
            "concepts": [
                "cell theory principles", "prokaryotic vs eukaryotic cell structures", "nucleus structure and functions", "ribosome protein factories",
                "mitochondria energy production organelles", "chloroplast structures and photosynthesis", "endoplasmic reticulum types", "Golgi apparatus packaging systems",
                "lysosome digestive enzymes", "cell membrane fluid mosaic model", "passive transport mechanisms (diffusion, osmosis)", "active transport protein pumps",
                "mitosis cell division stages", "meiosis cell division processes", "photosynthesis light-dependent reactions", "Calvin cycle carbon fixation",
                "cellular respiration glycolysis steps", "Krebs citric acid cycle", "electron transport chain ATP synthesis", "anaerobic respiration fermentation",
                "DNA structure double helix configuration", "RNA types and functions (mRNA, tRNA, rRNA)", "DNA replication semi-conservative mechanism", "transcription RNA synthesis process",
                "translation protein synthesis codon decoding", "Mendelian genetics laws", "dominant and recessive allele interactions", "monohybrid and dihybrid genetic crosses",
                "punnett square probability predictions", "non-Mendelian inheritance types", "incomplete dominance vs codominance", "sex-linked genetic traits",
                "gene mutation types", "natural selection evolutionary theory", "adaptation mechanisms of species", "speciation process types",
                "fossil record evidence", "homologous vs analogous structures", "phylogenetic tree structures", "taxonomic classification hierarchy",
                "kingdom classification systems", "ecosystem trophic level dynamics", "food web structures", "biogeochemical cycles (carbon, nitrogen)",
                "symbiotic relationship types (mutualism)", "parasitism vs commensalism", "ecological succession stages", "carrying capacity limits",
                "human anatomy system overviews", "circulatory system heart chambers", "respiratory system gas exchange", "digestive system enzyme locations",
                "nervous system neuron communication", "endocrine system hormone actions", "immune system defense lines", "photosynthesis pigments",
                "enzymatic reaction lock and key model", "homeostasis maintenance systems", "chromosomal abnormalities detection", "genetic engineering technologies"
            ]
        },
        "Mathematics": {
            "subtopic": "Algebra, Calculus & Statistics",
            "concepts": [
                "linear equations solving", "quadratic equation factoring", "quadratic formula applications", "systems of equations elimination",
                "matrix determinant calculations", "matrix inverse applications", "vector operations geometry", "function domains and ranges",
                "polynomial factorization strategies", "exponential growth equations", "logarithmic property rules", "trigonometric function values",
                "unit circle representations", "trigonometric identity proofs", "limit definitions in calculus", "limit evaluation techniques",
                "derivative definition limits", "derivative power rule shortcut", "derivative product rule applications", "derivative quotient rule formulas",
                "derivative chain rule operations", "implicit differentiation techniques", "optimization modeling problems", "related rates word problems",
                "fundamental theorem of calculus", "indefinite integral calculations", "definite integral area calculations", "integration by parts method",
                "integration by substitution rules", "partial fraction decomposition integration", "double integrals in calculus", "differential equations separation",
                "infinite series convergence tests", "Taylor series approximations", "mean, median, and mode metrics", "variance and standard deviation",
                "probability permutations formula", "probability combinations formula", "conditional probability equations", "Bayes' theorem applications",
                "binomial probability distributions", "normal distribution z-score conversions", "linear regression slope equations", "correlation coefficient calculation (r)",
                "population parameter estimations", "sample statistic calculations", "central limit theorem calculations", "confidence interval margin of error",
                "null and alternative hypothesis statements", "Type I and Type II errors statistics", "t-distribution hypothesis testing", "chi-square test of independence",
                "arithmetic sequence formulas", "geometric series sum formulas", "complex numbers operations", "Euler's formula representation",
                "polar coordinates conversion equations", "conic sections geometric forms", "set theory union and intersection", "mathematical induction proofs"
            ]
        },
        "History": {
            "subtopic": "Civilizations & Historical Eras",
            "concepts": [
                "Mesopotamian civilization advancements", "Ancient Egyptian empire dynasties", "Indus Valley civilization cities", "Ancient Greek city-states characteristics",
                "Roman Republic governance structures", "Roman Empire expansion and decline", "feudalism hierarchy in medieval Europe", "Crusades religious campaigns motivations",
                "Black Death plague consequences", "Renaissance intellectual movement origin", "scientific revolution discovery milestones", "Protestant Reformation religious fractures",
                "Age of Exploration maritime routes", "Columbian Exchange global impacts", "Transatlantic slave trade legacy", "Enlightenment philosophical thought ideas",
                "French Revolution political causes", "American Revolutionary War battles", "Industrial Revolution factory innovations", "Imperialism colonial expansion justifications",
                "World War I alliance triggers", "trench warfare conditions WWI", "Treaty of Versailles outcomes WWI", "Russian Revolution political shifts",
                "Great Depression global economic failures", "Rise of totalitarian regimes Europe", "World War II Axis vs Allied campaigns", "Holocaust human rights violations",
                "Atomic bomb deployment debates WWII", "United Nations creation aims", "Cold War superpower rivalries", "Marshall Plan reconstruction Europe",
                "Decolonization movements Asia and Africa", "Chinese Communist Revolution shifts", "Korean War conflict boundaries", "Vietnam War political implications",
                "Berlin Wall construction and fall", "Collapse of the Soviet Union timeline", "Middle East conflicts origins", "Globalization economic integrations",
                "Information Age technological revolutions", "Ancient Maya civilization achievements", "Aztec Empire city planning structures", "Inca Empire road network engineering",
                "Magna Carta constitutional significance", "French and Indian War alliances", "Meiji Restoration modernization Japan", "Industrialization environmental changes",
                "Suffrage movements women voting rights", "Civil Rights Movement struggles America", "Apartheid regime collapse South Africa", "Sumerian cuneiform writing writing origins",
                "Ottoman Empire expansion battles", "Byzantine Empire capital survival", "Silk Road trade network routes", "Mongol Empire conquest strategies"
            ]
        }
    }
}

# Questions templates (6 per concept to generate 60 * 6 = 360 questions per topic)
templates = [
    {
        "q": "What is {concept}?",
        "a": "{concept} refers to a core element in {topic} (under {subtopic}). In the context of {category}, it acts as a fundamental framework for understanding advanced theories and systems."
    },
    {
        "q": "How does {concept} work?",
        "a": "In practice, {concept} works by applying specific principles defined in {topic}. This helps organize processes, optimize outputs, and structure models in {category} applications."
    },
    {
        "q": "Explain the significance of {concept}.",
        "a": "The significance of {concept} in {topic} lies in its ability to solve key problems. Within {category}, it establishes standard workflows and drives efficiency."
    },
    {
        "q": "Why is {concept} important?",
        "a": "{concept} is crucial because it bridges the gap between basic concepts and practical implementation. In {category} study, it provides the baseline logic for {topic} systems."
    },
    {
        "q": "Can you describe the main applications of {concept}?",
        "a": "Common applications of {concept} include modeling, optimization, and system design in {category}. It forms a key part of the modern approach to {topic}."
    },
    {
        "q": "What are the key challenges associated with {concept}?",
        "a": "Primary challenges with {concept} involve scalability, precision, and integration. Solving these challenges in {topic} requires robust methods aligned with {category} standards."
    }
]

# Generate the questions
questions_dataset = []

for category, topics in dataset_config.items():
    for topic, config in topics.items():
        subtopic = config["subtopic"]
        concepts = config["concepts"]
        
        # Determine difficulty based on concept index
        for idx, concept in enumerate(concepts):
            if idx < len(concepts) // 3:
                difficulty = "Beginner"
            elif idx < (2 * len(concepts)) // 3:
                difficulty = "Intermediate"
            else:
                difficulty = "Advanced"
            
            # Generate questions using all 6 templates
            for template in templates:
                q_text = template["q"].format(concept=concept, topic=topic, subtopic=subtopic, category=category)
                # Capitalize first letter of the question
                q_text = q_text[0].upper() + q_text[1:]
                
                a_text = template["a"].format(concept=concept, topic=topic, subtopic=subtopic, category=category)
                a_text = a_text[0].upper() + a_text[1:]
                
                doc = {
                    "question": q_text,
                    "answer": a_text,
                    "topic": topic,
                    "subtopic": subtopic,
                    "category": category,
                    "difficulty": difficulty,
                    "source": "dataset"
                }
                questions_dataset.append(doc)

# Save the dataset to the required directory
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
output_dir = os.path.join(backend_dir, "datasets")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "education_technology_questions.json")

with open(output_file, "w") as f:
    json.dump(questions_dataset, f, indent=2)

print(f"Generated {len(questions_dataset)} questions successfully at {output_file}.")
