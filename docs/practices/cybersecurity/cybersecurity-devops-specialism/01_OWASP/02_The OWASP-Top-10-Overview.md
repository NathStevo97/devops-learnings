# 2.0 - The OWASP Top 10 - An Overview

## 2.1 - Introduction to APIs

### 2.1.1 - What are APIs?

- Application Programming Interface
- Rules/Protocols that allow programs and applications to communicate with each other
- Variety of use cases including web-based systems, operating systems, hardware, software, devices, etc
- Practical Example:
  - Restaurant customer reviews menu and asks the waiter for x y z courses
  - Waiter instructs kitchen to produce x y z courses, and returns them when it's ready
- API requests account for ~83% of all web traffic
- Protocols include SOAP, REST, and GraphQL - only REST will be considered here

### 2.1.2 - Security Concerns

- APIs account for 90% of the attack surface and are the most frequent attack vector
- Common targets are social media, health, financial, and travel
- Underprotected APIs are highly at risk of data breaches
- APIs are high-risk targets as:
  - They access large amounts of data and info at any given point
  - APIs grant privileges to access sensitive data and can grant elevated privileges
  - API access can be different to standard web app access
- With traditional web app access, it's often: open app -> authenticate -> get resource access upon success
- With APIs, there's many endpoints, parameters, etc to consider, so traditional web app access methods may be bypassable
- APIs are generally easy to find
- APIs undergo constant changes and releases

### 2.1.3 - OWASP and the OWASP API Security Project

- Security is often an afterthought in development compared to new features, stakeholder deadlines, etc.
- Open Web Application Security Project (OWASP) is a nonprofit organization dedicated to improving the security of web applications and software
- It's best known for its top 10 of security vulnerabilities in applications.

## 2.2 - The OWASP Security API Top 10

### 2.2.1 - Broken Object-Level Authorization (BOLA)

- Occurs due to APIs exposing endpoints that handle object identfiiers
  - This creates a wide attack surface level access control issue
  - Object authorization checks should be considered in every function that accesses a data source using input from users
- Also known as Insecure Direct Object Referebces (IDORs)
- Access control vulnerabilities when user-supplied inputs allow abnormal access
- Example: User substitutes their user id with that of another user to access resources they shouldn't have access to normally
- No "elite" hacking skills required - often just a case of misconfigured access controls
- **Protecting against BOLAs Attacks:**
  - Add authorization checks iwth user policies and hierarchy
  - Avoid including user ids in API requests
  - Utilise session IDs or tokens
  - Use random unguessable IDs, or unique universal identifiers (UUIDs)
  - Regularly check authorization for clients requesting access
  - Implement a zero-trust model
  - **Regularly test all services and APIs**

### 2.2.2 - Broken Authentication

- Occurs when authentication mechanisms are implemented inocrrectly
- Allows attackers to compromise authentication tokens or exploit implementation flaws
- **Causes of Broken User Authentication:**
  - Applications displaying sensitive details e.g. tokens in URLs
  - Pemitting weak passwords
  - Misconfiguring token usage e.g JWT (JSON Web Tokens)
-

### 2.2.3 - Excessive Data Exposure

### 2.2.4 - Lack of Resource and Rate Limiting

### 2.2.5 - Broken Function-Level Authorization

### 2.2.6 - Mass Assignment

### 2.2.7 - Security Misconfigurations

### 2.2.8 - Injection

### 2.2.9 - Improper Assets Management

### 2.2.10 - Insufficient Logging and Monitoring
