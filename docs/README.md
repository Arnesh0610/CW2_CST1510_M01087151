
Video link:https://drive.google.com/drive/folders/1mlv-g48NOVlGgtSJdRa832N5LbLY9h7F?usp=drive_link
GitHub link:https://github.com/Arnesh0610/CW2_CST1510_M01087151/tree/main

# Week 7: Secure Authentication System
Student Name: Arneshrai Tarushsingh Lochun
Student ID: M01087151
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform
## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)

# Week 8: Database Migration & CRUD functionality
## Project Description
Developed a relational database system with SQLite to consolidate data from three separate domains and manage user authentication. The project incorporated CRUD operations and automated the transfer of data, from flat files (CSV, TXT) into organized tables.

## Features
-Created a robust SQLite database schema with normalized tables for each domain and user management.
-Automated data pipeline scripts to ingest, validate, and load data from CSV files and user.txt into the database.
-Implemented and rigorously tested a complete set of CRUD operations (Create, Read, Update, Delete) for each data entity.
-Verified database integrity through validation checks to ensure data consistency and referential accuracy.

## Technical Implementation
-Database design and creation using the SQLite3 module in Python.
-Wrote parameterized SQL queries to execute all CRUD operations, preventing SQL injection vulnerabilities.
-Developed data migration scripts using Python's CSV module and file I/O to populate tables from external sources.
-Established the primary data access layer for the entire application stack.

# Week 9: Streamlit & Plotly/Matplotlib
## Project Description
Transformed the core application into an interactive, multi-page web platform using the Streamlit framework. Implemented a Model-View-Controller (MVC) pattern, secure user authentication, and dynamic data visualizations to deliver a comprehensive dashboard experience.

## Features
-Built a structured multi-page web application with dedicated sections for login, analytics dashboard, and settings.
-Implemented a secure login and registration system with session management, restricting page access based on authentication state.
-Developed an interactive analytics dashboard with rich, domain-specific data visualizations (charts, graphs, tables).
-Developed an user interface that allows users to add, modify and remove records directly via the web platform.
-Added a user settings page for account management and secure logout functionality.

## Technical Implementation
-Utilized Streamlit as the primary web framework for rapid UI development and deployment.
-Managed application state and user sessions using st.session_state.
-Generated interactive charts and graphs with Plotly Express and Streamlit's native visualization components.
-Implemented input validation and error handling for all user interactions to ensure data quality.
-Enforced page access control by checking authentication status before rendering sensitive routes.

# Week 10: Integrating AI using python
## Project Description
Implemented the Google Gemini AI model to develop three distinct domain-focused virtual assistants. This functionality offers context-aware analysis and Q&A features right inside the application improving data interaction.

## Features
-Introduced a dedicated AI Assistant page with a tabbed interface for the three domains (Cybersecurity, IT Operations, Data Science).
-Developed specialized AI agents, each fine-tuned with a domain-specific system prompt and relevant dataset context.
-Activated natural language querying, enabling users to pose questions and obtain expert-grade insights derived from the loaded information.
-Implemented conversation memory to maintain context within each chat session.
-Provided a control to clear conversation history for a fresh start.

## Technical Implementation
-Integrated the Google Generative AI SDK (google-generativeai) to connect with the Gemini API.
-Engineered context-aware system prompts by dynamically loading and formatting domain data from the database into the AI's context window.
-Structured the application logic to manage multiple AI assistants within a single interface using session state and dictionary data structures.
-Handled API communication, response parsing, and error management for a seamless user experience.

# Week 11: OOP Refactoring
## Project Description
-Transformed the applications codebase from a procedural script, into a structured maintainable Object-Oriented Programming (OOP) design. This overhaul enhances code structure, reusability and scalability.

## Technical Implementation
-Designed and implemented a User class to encapsulate user data (username, password hash, email) and related authentication methods, separating concerns from the main application logic.
-Created tailored domain-specific AI classes derived from the base class. These classes handle their system prompts, domain-specific data and data manipulation tasks (insert, update, delete).
-Restructured the data access layer, promoting cleaner separation of concerns, improved testability, and easier future enhancements.


