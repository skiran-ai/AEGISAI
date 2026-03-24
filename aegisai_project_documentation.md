# AEGISAI – Cyber Security and Crime Reporting System
## Comprehensive Project Documentation

---

### 1. ABSTRACT

In an era characterized by an unprecedented surge in digital interconnectivity, the proliferation of cyber threats has become a critical concern for both individuals and institutional frameworks. The traditional paradigms of crime reporting and incident response are heavily reliant on fragmented, manual, and often asynchronous processes, leaving a vast disparity between the occurrence of a cybercrime and its subsequent resolution. To address this glaring deficiency, this project introduces "AEGISAI – Cyber Security and Crime Reporting System," a sophisticated, unified digital platform designed to completely revolutionize the methodology of reporting, analyzing, and mitigating cybercrimes. 

The primary purpose of AEGISAI is to provide a seamless, secure, and centralized portal that bridges the communication gap between everyday citizens, law enforcement agencies, and system administrators. The existing problem landscape is dominated by disjointed platforms where victims struggle to navigate complex reporting procedures, while law enforcement (the police module) grapples with organizing scattered data. Furthermore, the submission of digital evidence is fraught with risks, as current systems rarely implement automated security checks, potentially exposing police networks to malicious software embedded within victim-submitted files.

AEGISAI comprehensively solves these operational bottlenecks by integrating advanced cybersecurity measures directly into the crime reporting workflow. The core features of the system include an intuitive, centralized crime reporting module, strict role-based access control (User, Admin, Police), and a dedicated file-sharing mechanism fortified with automated malware scanning capabilities. This ensures that any evidentiary files uploaded by victims or shared among police personnel are actively screened, mitigating the risk of secondary infections. Additionally, the system incorporates real-time threat logging and a structured feedback mechanism to continuously adapt to emerging security landscapes. 

The profound impact of AEGISAI lies in its ability to streamline the investigative workflow for law enforcement while simultaneously empowering citizens with a transparent, responsive reporting tool. By minimizing administrative overhead and maximizing data security, the project establishes a robust, proactive cybersecurity ecosystem. It not only accelerates the detection and resolution of cyber offenses but also fortifies the infrastructural integrity of the reporting system itself, proving to be an indispensable asset for modern digital policing environments.

---

### 2. INTRODUCTION

The rapid evolution of information technology and the ubiquitous adoption of the internet have undeniably transformed global communication, commerce, and governance. However, this digital paradigm shift has simultaneously birthed sophisticated vectors for criminal activity, ranging from financial fraud and identity theft to distributed denial-of-service (DDoS) attacks and systemic data breaches. As these cybercrimes become increasingly prevalent and complex, the necessity for a resilient, responsive, and secure infrastructure to report and combat them is of paramount importance. The AEGISAI system is conceptualized as a definitive response to these modern challenges, offering a technologically advanced framework tailored specifically for structured cybercrime management.

The importance of cybersecurity in contemporary society cannot be overstated. A single vulnerability can compromise vast amounts of sensitive personal or organizational data, leading to severe financial and reputational repercussions. Concurrently, the efficacy of addressing these threats depends entirely on the swiftness and accuracy of the reporting mechanisms available to victims. Without a reliable channel to alert authorities, critical forensic evidence is often lost or degraded. AEGISAI addresses this fundamental need by emphasizing not just the reporting of crimes, but the absolute security of the data and evidence being handled throughout the investigative lifecycle.

Modern policing operations increasingly rely on digital systems to parse, categorize, and act upon vast quantities of intelligence. The role of digital systems in this context is to shift law enforcement strategies from reactive, paper-based operations to proactive, data-driven forensics. AEGISAI facilitates this transition by providing law enforcement personnel with dedicated, analytical dashboards that organize incoming reports logically and securely. By integrating automated threat detection protocols directly into the evidential chain of custody, the system represents a significant leap forward in secure policing technology, establishing a new standard for how digital incidents are managed from initial submission to final resolution.

---

### 3. EXISTING SYSTEM

The existing landscape of crime reporting is largely characterized by a reliance on outdated, manual methodologies and disparate digital portals that lack cohesive integration. Currently, a victim of a cybercrime is often required to navigate a convoluted path to register a complaint. This frequently involves physically visiting a local police station, a process that is intimately tied to jurisdictional constraints and geographical limitations. In cases where digital portals do exist, they are often fragmented across different state or national departmental domains, lacking a unified front-end interface, which inherently discourages victims from submitting timely reports.

Operationally, the current digital systems primarily act as passive repositories. A user submits a plain-text form, which is then sequentially added to an unorganized database. These systems exhibit an alarming lack of automated security screening. When victims submit supporting evidence, such as financial transaction logs, email headers, or screenshots, these files are transferred and processed without any intermediary malware scanning. Consequently, law enforcement networks opening these files are exposed to significant security risks, potentially executing concealed malicious payloads. Furthermore, the communication loop is fundamentally broken; victims rarely receive real-time updates regarding the status of their reports, and administrators lack holistic oversight of recurring threat vectors, making it nearly impossible to identify systemic attack patterns proactively.

---

### 4. LIMITATIONS OF EXISTING SYSTEM

1. Highly fragmented and disjointed reporting portals leading to confusion and deterrence among civilian victims.
2. Complete lack of integrated automated malware scanning during the submission of digital evidence, risking police networks.
3. Absence of a centralized, unified database accessible instantaneously by cross-jurisdictional law enforcement departments.
4. Tedious, error-prone manual entry and transcription processes still required at physical police stations.
5. Inability for end-users to effectively track the real-time operational status or progress of their submitted reports.
6. Delayed and inefficient horizontal communication methodologies between different law enforcement and administrative branches.
7. High risk of evidence tampering and degradation due to the reliance on insecure, unencrypted file-sharing methods.
8. Severe lack of automated threat and intrusion logging to help administrators identify and preempt recurring attack patterns.
9. Poor, non-intuitive user interfaces that make it exceedingly difficult for non-technical individuals to file comprehensive reports.
10. No dedicated or isolated modules for system administrators to actively oversee, manage, and maintain platform security.
11. Insufficient and unstructured feedback mechanisms, hindering continuous system evolution and user experience improvement.
12. Heavy dependence on physical paper trails and temporary local storage, leading to frequent data loss and archiving difficulties.
13. Complete lack of role-based, specialized dashboards tailored to the specific daily workflows of different operational users.
14. High administrative overhead and bottlenecking involved in the manual classification, sorting, and assignment of incoming complaints.
15. Inadequate architectural scalability, causing system crashes or severe latency during periods of sudden spikes in cybercrime reporting.

---

### 5. PROPOSED SYSTEM

To effectively dismantle the severe limitations of current methodologies, "AEGISAI – Cyber Security and Crime Reporting System" is proposed as a comprehensive, end-to-end framework. AEGISAI is engineered to be a singular, authoritative platform that completely digitizes and aggressively secures the cybercrime reporting lifecycle. By centralizing the intake, processing, and management of reports, it eliminates geographical and procedural friction, ensuring that law enforcement receives clean, structured data instantaneously.

The proposed system addresses fundamental operational flaws through the incorporation of the following specialized features:
*   **Centralized Reporting:** AEGISAI provides a single unified portal for all cybercrime complaints, standardized to collect precise, legally actionable information (such as incident type, timestamps, and descriptive narratives) directly from the victim.
*   **Role-Based Access Control:** The architecture inherently segregates the platform into distinct, isolated operational zones for Users, Administrators, and Police personnel. Each role is authenticated securely and served a dedicated dashboard tailored to their specific data requirements and clearance levels.
*   **Automated Malware Scanning:** A critical innovation of the proposed system is the integration of algorithmic scanning protocols. Any file or piece of digital evidence uploaded via the platform is automatically subjected to rigorous malware detection before it is permitted to be stored or opened by law enforcement, ensuring complete network safety.
*   **Threat Logging:** The system features background telemetry that actively monitors the platform itself, logging potential intrusion attempts, abnormal datasets, and security threats. Administrators are provided detailed logs to maintain total oversight of the system's integrity.
*   **Secure File Sharing:** AEGISAI provides an encrypted channel for file exchange not just from user to police, but interconnecting various administrative and law enforcement entities, ensuring strict chain-of-custody for digital artifacts.
*   **Feedback Mechanism:** A structured communication loop is established, allowing users to provide actionable feedback regarding system usability and police response times, facilitating iterative operational improvements.

---

### 6. ADVANTAGES OF PROPOSED SYSTEM

1. Delivers a unified, single-window platform that significantly bridges the operational gap between citizens, law enforcement, and administrators.
2. Uniquely guarantees digital evidence integrity and network safety through automated, real-time malware scanning protocols during all file uploads.
3. Facilitates highly accelerated incident response timelines via dedicated, role-specific dashboards equipped with priority-based complaint queues.
4. Substantially enhances internal system security by maintaining comprehensive threat logs and actively monitoring for potential dataset anomalies or intrusions.
5. Streamlines critical inter-agency and intra-agency communication frameworks with inherently secure, trackable file-sharing capabilities.
6. Presents a highly scalable, robust architecture built upon modern web frameworks (Django), easily accommodating future increases in data load and geographical expansion.

---

### 7. FEASIBILITY ANALYSIS

**Technical Feasibility**
The technical feasibility of AEGISAI evaluates the readiness of the chosen technological stack to meet the complex requirements of the platform. The system is built utilizing the Django framework (Python), which inherently provides robust security features, excellent scalability, and built-in administrative tools. The front-end leverages standard HTML, CSS, and JavaScript, ensuring high compatibility across varying web browsers and devices. The integration of Python-based scripting for automated malware scanning and threat logging is highly practical given Python's extensive cybersecurity libraries. As these technologies are well-documented, mature, and actively maintained, the project is technically sound and highly feasible, presenting no insurmountable engineering barriers.

**Operational Feasibility**
Operational feasibility assesses how well the proposed system resolves the specific problems of the intended users and integrates into their daily workflows. AEGISAI is designed with distinct, specialized modules for Users, Police, and Admins, ensuring that interfaces are uncluttered and highly relevant to the respective actor. The automated nature of evidence scanning and structured reporting directly reduces the manual administrative burden currently placed on police officers, allowing them to focus on active investigation rather than data entry. Because the system mimics standard, intuitive web application flows, the learning curve for both citizens and law enforcement personnel is minimized, guaranteeing high operational adoption and overall feasibility.

**Schedule Feasibility**
Schedule feasibility determines if the project can be successfully developed, tested, and deployed within the designated academic timeframe. The modular architecture of the Django framework significantly accelerates development by enabling parallel implementation of distinct components (e.g., the User module can be finalized while the File Scanning logic is still under construction). By utilizing SQLite as the preliminary database, early-stage configuration overhead is drastically reduced. With clear module definitions, established data flow constraints, and a highly structured architectural plan, the AEGISAI project easily fits within the standard final-year academic project timeline, ensuring timely delivery.

**Economic Feasibility**
Economic feasibility involves the cost-benefit analysis of developing and deploying the system. AEGISAI is entirely built upon robust, open-source technologies. Python, Django, SQLite, and base front-end technologies require zero licensing fees. The development phase requires only standard computing hardware and an internet connection. Furthermore, the operational cost of the system once deployed is limited to standard web server hosting and potential PostgreSQL scaling, which are highly cost-effective compared to the massive financial inefficiencies, labor costs, and security risks associated with maintaining the existing manual reporting infrastructures. Therefore, the project is highly economically feasible.

---

### 8. HARDWARE REQUIREMENTS

**Development Level**
*   **Processor:** Intel Core i5 / AMD Ryzen 5 or equivalent modern multi-core processor
*   **Memory (RAM):** 8 GB Minimum (16 GB recommended for smooth multi-tasking and server emulation)
*   **Storage:** 256 GB SSD (Solid State Drive preferred for faster read/write processes during development)
*   **Input Devices:** Standard Keyboard and Mouse
*   **Display:** 15-inch monitor or larger, supporting HD resolution (1920x1080) for clear interface rendering

**Deployment Level (Server/Hosting)**
*   **Processor:** Minimum 2 to 4 vCPU cores (Virtual Private Server)
*   **Memory (RAM):** 4 GB Minimum (8 GB recommended for handling concurrent database queries and file scanning operations)
*   **Storage:** 50 GB SSD minimum (Expanding dynamically based on uploaded evidentiary file volume)
*   **Network:** High-speed broadband/fiber connection with appropriate bandwidth to handle multiple concurrent secure file uploads

---

### 9. SOFTWARE REQUIREMENTS

*   **Operating System:** Windows 10/11, macOS, or Linux (Development) / Linux (Ubuntu 20.04+ preferred for deployment)
*   **Programming Languages:** Python 3.x (Backend Core), JavaScript (Frontend Logic)
*   **Markup and Styling:** HTML5, CSS3 
*   **Web Framework:** Django 4.x or 5.x (High-level Python Web framework)
*   **Database Management System:** SQLite (Development/Initial Phase) scalable seamlessly to PostgreSQL (Production)
*   **Integrated Development Environment (IDE):** Visual Studio Code, PyCharm, or equivalent
*   **Web Browser:** Google Chrome, Mozilla Firefox, or Microsoft Edge (For testing and client access)

---

### 10. MODULE DESCRIPTION

**User Module**
The User Module is the primary intersection point between the civilian victim and the AEGISAI platform. It is engineered to be highly intuitive and completely secure. Within this module, individuals can register for an account using verified credentials. Once authenticated, users access a personalized dashboard where they can submit detailed cybercrime reports, categorized by offense type. Crucially, this module allows users to track the real-time status of their submitted complaints, securely upload evidentiary files, and update their personal profiles, effectively removing the ambiguity often experienced by victims in the aftermath of a cyber incident.

**Admin Module**
The Admin Module serves as the overarching control center for the entire platform architecture. Administrators govern the system, possessing the highest level of clearance. This module facilitates the management of all registered entities, allowing the admin to approve or revoke access for Police and User accounts to maintain platform integrity. The Admin Module is uniquely positioned to view overarching system metrics, oversee all active operations, review threat logs generated by the security subsystems, and manage holistic database health. This ensures the application remains secure, heavily monitored, and functionally pristine.

**Police Module**
The Police Module is meticulously crafted for law enforcement personnel to receive, process, and investigate reported cybercrimes efficiently. Officers log into their specific dashboard to view priority queues of complaints submitted by the User Module. This module allows police to securely review digital evidence (post-malware scan), update the status of active investigations (e.g., Pending, Investigating, Resolved), and communicate secure findings. The architecture replaces disorganized paper files with a highly searchable, categorized digital repository of active cases, significantly accelerating the investigative workflow.

**Crime Reporting Module**
Functioning as the core data-intake engine of the system, the Crime Reporting Module handles the structured acquisition of incident details. It governs the validation of form submissions, ensuring that vital metadata—such as time of incident, type of attack, and descriptive narratives—is correctly logically enforced before database insertion. This module is responsible for bridging the User's input directly into the Police queue, ensuring that no complaint is lost, miscategorized, or corrupted during transmission. 

**File Sharing & Malware Detection Module**
This is the pivotal security mechanism of the AEGISAI project. Whenever a user or an officer transfers a file—be it evidence, documents, or reports—this module intercepts the transaction. It automatically executes a programmatic layer of malware detection algorithms against the file payload. If an anomaly, malicious signature, or executable threat is identified, the file is immediately quarantined, the transfer is blocked, and an alert is logged to the system. Only verified, clean files are permitted to enter the secure local file-sharing system, thereby totally immunizing the platform from embedded cyberattacks.

**Feedback Module**
The Feedback Module is dedicated to capturing user sentiment and operational suggestions regarding the platform's efficiency. It allows registered users to submit structured qualitative and quantitative feedback concerning the resolution of their cases or the usability of the software itself. This data is securely routed to the Admin dashboard, providing developers and administrators with direct, actionable insights to iteratively refine system UI, improve response protocols, and ensure the continuous evolution of the service.

---

### 11. DFD (DATA FLOW DIAGRAM)

**A. LEVEL 0 (Context Diagram)**
*   **Central Process:** [0.0] AEGISAI System
*   **Entities:** USER, POLICE, ADMIN
*   **Data Flow Description:** 
    *   The **USER** entity sends "Registration Details", "Login Credentials", "Crime Report Data", and "Evidence Files" to the AEGISAI System. 
    *   The AEGISAI System responds to the USER with "Status Updates", "Scan Results", and "System Notifications".
    *   The AEGISAI System forwards "Verified Crime Reports" and "Clean Evidence Files" directly to the **POLICE** entity.
    *   The **POLICE** entity returns "Case Status Updates" and "Investigation Notes" back to the system.
    *   The **ADMIN** entity interacts with the system by receiving "Global System Logs", "Threat Logs", and "User Data", while sending "Management Commands" and "Verification Approvals" to control the central process.

**B. LEVEL 1**
*   **Sub-Processes:**
    *   **Process 1.0 (Authentication):** Receives Login Details from Entities, checks against the Database, and routes to respective Role Dashboards (Process 2.0, 3.0, 4.0).
    *   **Process 2.0 (Handle User Operations):** Accepts Crime Report Data from the User. It forwards text data to the Database and sends files to Process 5.0 (File Scanning).
    *   **Process 3.0 (Handle Police Operations):** Pulls Pending Reports from the Database and displays them to Police. Police send Status Updates which are written back to the Database.
    *   **Process 4.0 (Handle Admin Operations):** Pulls Threat Logs and User Lists from the database, allowing Admins to alter user status parameters.
    *   **Process 5.0 (Malware Scanning Engine):** Receives Raw Files from Process 2.0, performs security checks. If clean, it pushes the "Safe File" to the Secure File Storage. If infected, it pushes "Threat Alert" to the Threat Log Database and notifies the user.
*   **Data Flow Explanation:** Data moves synchronously from authentication to designated dashboards. User input is split; text goes to the Database, files go to the Scanning Engine. Only sanitized files reach Police interfaces, ensuring a secure flow of evidence.

---

### 12. ER DIAGRAM

*   **Entities:**
    *   **USER_REGISTER:** Represents the civilian victim.
    *   **POLICE_REGISTER:** Represents the law enforcement official.
    *   **CYBER_CRIME_REPORT:** Represents the submitted incident.
    *   **FILEDATA:** Represents uploaded digital evidence.
    *   **THREAT_LOG / ATTACK:** Represents logged system security events.
*   **Attributes:**
    *   **USER_REGISTER:** User_ID (Primary Key), Name, Email, Password, Phone, Address.
    *   **POLICE_REGISTER:** Police_ID (Primary Key), Badge_Number, Name, Station, Email, Password.
    *   **CYBER_CRIME_REPORT:** Report_ID (Primary Key), User_ID (Foreign Key), Incident_Type, Description, Timestamp, Status.
    *   **FILEDATA:** File_ID (Primary Key), Report_ID (Foreign Key), Filename, Upload_Date, Malware_Status.
    *   **THREAT_LOG:** Log_ID (Primary Key), Timestamp, IP_Address, Threat_Type, Severity.
*   **Relationships:**
    *   One **USER_REGISTER** *submits* Many **CYBER_CRIME_REPORTs** (1:N).
    *   One **CYBER_CRIME_REPORT** *contains* Many **FILEDATA** uploads (1:N).
    *   One **POLICE_REGISTER** *manages/investigates* Many **CYBER_CRIME_REPORTs** (1:N).
    *   (Optional depending on exact arch) The system implicitly generates the THREAT_LOG based on interactions across the environment.

---

### 13. USE CASE DIAGRAM

*   **Actors:** User, Police, Admin.
*   **Use Cases:**
    *   **User:** Register Account, Login, Submit Crime Report, Upload Evidence Files, View Report Status, Submit Feedback.
    *   **Police:** Login, View Assigned Complaints, Download Secure Evidence, Update Case Status.
    *   **Admin:** Login, Manage Users (Approve/Reject Police/Users), View System Analytics, Monitor Threat Logs, Review User Feedback.
    *   *(System Level Includes)*: "Upload Evidence Files" uses `<<include>>` on "Execute Malware Scan".
*   **Relationships:**
    *   All actors share association with the generic "Login" use case. 
    *   The User is directly associated with the reporting and feedback use cases.
    *   The Admin is strictly associated with platform management and log review use cases.

---

### 14. DATABASE DESIGN

**Table: USER_REGISTER**
*   `id` (Integer, Primary Key, Auto-increment): Unique identifier.
*   `full_name` (Varchar): User's legal name.
*   `email` (Varchar, Unique): Contact email used for login.
*   `password` (Varchar): Hashed authentication string.
*   `phone` (Varchar): Contact number.
*   `created_at` (Datetime): Registration timestamp.

**Table: POLICE_REGISTER**
*   `id` (Integer, Primary Key, Auto-increment): Unique identifier.
*   `badge_number` (Varchar, Unique): Verification identifier for the officer.
*   `name` (Varchar): Officer name.
*   `department` (Varchar): Specific division or station.
*   `email` (Varchar, Unique): Login email.
*   `is_approved` (Boolean): Managed by Admin to authorize the account.

**Table: CYBER_CRIME_REPORT**
*   `report_id` (Integer, Primary Key, Auto-increment).
*   `user_id` (Integer, Foreign Key -> USER_REGISTER.id): Link to the complainant.
*   `incident_category` (Varchar): e.g., Financial Fraud, Identity Theft.
*   `report_title` (Varchar): Short summary.
*   `detailed_description` (Text): Full narrative of the event.
*   `status` (Varchar): Default "Pending", updatable to "Investigating", "Resolved".
*   `submission_date` (Datetime).

**Table: FILEDATA (Evidence)**
*   `file_id` (Integer, Primary Key, Auto-increment).
*   `report_id` (Integer, Foreign Key -> CYBER_CRIME_REPORT.report_id): Link to the parent report.
*   `file_name` (Varchar): Actual name of the file.
*   `file_path` (Varchar): Secure storage location on the server.
*   `is_safe` (Boolean): Flag set by the malware scanning module.

**Table: FEEDBACK**
*   `feedback_id` (Integer, Primary Key).
*   `user_id` (Integer, Foreign Key -> USER_REGISTER.id).
*   `rating` (Integer): Numeric satisfaction score.
*   `comments` (Text): Qualitative review.

---

### 15. FORM DESIGN

**Registration Form**
*   *Fields:* Full Name (Text), Email Address (Email), Phone Number (Number), Password (Password), Confirm Password (Password), Role Selection (Dropdown - User/Police).
*   *Validation Logic:* Email format must be strictly regex verified. Passwords must match and enforce minimum complexity (e.g., length). Phone numbers must contain valid digits.
*   *Purpose:* Securely onboard distinct entities onto the platform while segregating basic privileges.

**Login Form**
*   *Fields:* Email Address (Email), Password (Password).
*   *Validation Logic:* Rejects unauthorized or blank inputs. Checks hashed credentials against the database. Flags consecutive failed attempts.
*   *Purpose:* Serves as the primary security gateway to authenticate and route the user to their respective dashboard tier.

**Report Submission Form**
*   *Fields:* Report Title (Text), Incident Category (Dropdown), Date of Incident (Date Picker), Detailed Description (Text Area).
*   *Validation Logic:* All fields are strictly mandatory. Prevents extreme character limits or harmful script injections in the text area (XSS prevention).
*   *Purpose:* Standardizes the intake of crime data to ensure the Police Module receives perfectly formatted, actionable intelligence.

**File Upload Form (Evidence Submission)**
*   *Fields:* File Selection (File Input Box).
*   *Validation Logic:* Enforces strict file size limits (e.g., Max 10MB). Restricts allowed database extensions entirely (e.g., blocking `.exe` or `.bat`), passing all intakes directly to the backend scanning engine.
*   *Purpose:* To securely funnel visual or data-driven evidence into the system without compromising the underlying server architecture.

**Feedback Form**
*   *Fields:* Overall Satisfaction (Radio Buttons/Stars), Detailed Comments (Text Area).
*   *Validation Logic:* Comments must not be blank if poor rating is given. Protected against SQL injection.
*   *Purpose:* To harvest structured analytical data for system iteration and administrative review, closing the operational loop.
