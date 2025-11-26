# 1.0 - Learning the OWASP Top 10

## 1.1 - Broken Access Control

- Occurs when confidential information is viewed by a user who should not have access to that data.
- **Access control:** Making sure people have access to what they're supposed to and don't have access to what they shouldn't
- A person with unintended access might read, edit or delete private data

- Scenario 1: HR rep leaves performance evaluation document in printer for anyone to pick up
- Sensitive information is exposed to an unauthorised person
- Roles may range in permissions from admins, developers, users, anonymous
- Broken access control occurs when a user is able to act beyond the permissions of their role
- Example: consider a social media account that's private - only approved friends and family should be able to see content

- One must ensure all private data is kept as such.

Scenario 2:

- Information gets accidentally sent to someone who shouldn't have it
- This differs to scenario 1 as a specific action has exposed the data to another party, rather than it being out in the open for anyone to look at
- Reference example 1: The HR rep accidentally sends the performance evaluations to the entire organisation rather than another colleague in HR
- An alternative would be medical record mixups at doctors appointments

- Wehn sending private information - make sure you are sending it to the right person.

- When building web applications, often the postive path is only tested, the negative/alternative paths are often neglected, which can lead to proble,s.
- Be intentional about building solid access control into systems.

## 1.2 - Cryptographic Failures

- Determine the protection needs of data in transit and at rest. For example, passwords, credit card numbers, health records, personal information, and business secrets require extra protection
- Vulnerability technicall split into 2 parts:
  - Part 1: Think about the data that's being collected, stored, and used
    - More sensitive / restricted / regulated / private data needs to be more protected
    - Encrypt data to protect it
  - Part 2: Follow well-known, proven procedures to ensure data is encrypted effectively
- Steps to implement additional protection:
  - If you don't have to store sensitive data, don't do it
  - If storing sensitive data, encrypt it at rest and in transit
  - If encrypting data, use known, strong cryptographic algorithms e.g. favour AES over md5
- Reference [OWASP Documentation](https://owasp.org) for further reading

- If you hae data that needs protecting in a web app - encrypt it
- If encrypting / protecting data, ensure best practices are followed

## 1.3 - Injection

- Code can be data or an instruction
- Injection: an application accepts data as input and processes it as an instruction
- An application is vulnerable to attack when hostile data is used
- Example: adopting a dog and giving it a name like a command "sit" - this confuses the dog as it does not know to process the instruction like a command or respond to the data
- Injection occurs where there is an opportunity for a user to provide input
  - Application may incorrectly handle the input
  - A bad actor could inject malicious code in this input that ends up being interpreted as instruction

- Injection may be achieved via cross-site-scripting:
  - Application does not neutralize user input
  - Does not verify that input is safe, legitimate, and in the correct format
- Reverting to the dog name analogy - the rescue could check the entered name against a "forbidden" list and reject if it's matched
- Ensure data is entered in the correct format e.g. lock dates in DD/MM/YYYY format
- Injections can also be used against web apps that connect to backend databases
  - SQL injection attacks are common - they look to create, read, update or delete information in backend SQL database
  - They also take advantage of unmonitored user input fields to trick applications
- Ensure user input in web apps is neutralized or verified

## 1.4 - Insecure Design

- OWASP: A new category focusing on risks relating to design and architectural flaws
- Consider issues in a house:
  - Small house problems == bugs (broken dishwasher seal, broken lightbulb, etc) - all can be fixed and don't cause long-term issues
  - Large house problems == design errors (weak foundation, fundamentally unstable) - large scale problems that cause long-term issues or require wholesale changes to fix
- Examples of insecure design:
  - Error messages that show sensitive information
  - Typically, error mesages are useful in development for troubleshooting
  - The error messages should be reviewed before code is deployed
  - Unsanitised messages may contain developer-specific information that can help malicious actors craft an attack
- A prime example of this would be an error message that displays the path for an important config file - hackers could use this to target the file and make harmful changes
- Another is passwords stored in plaintext

- Security matters not only in development and production, but design as well
- Consult with security expersts to ensure appropriate requirements and design decisions are made early on

## 1.5 - Security Misconfiguration

- An application might be vulnerable if the application is without a concerted, repeatable application security configuration process
- Hardened: A securely configured technology, software, or application
- Common security misconfigurations:
  - Not using a password on mobile devices
  - Failing to change default passwords
  - Enable unnecessary services or features
  - Insecurely configuring cloud permission services
  - Failing to update software
  - Failing to use strong passwords
- To address security misconfigurations:
  - Identify and evaluate each setting or configuration for security
  - Use center for internet security (CIS) guidelines
  - Comply with CIS hardening standards
  - Address your unique organizational risk tolerance and requirements
- All teams need to understand the fundamental concept of security misconfiguration
- Teams should make decisions purposefully with knowledge of the security risks involved

## 1.6 - Vulnerable and Outdated Components

- The majority of web apps are built via open-source or third party components - if they're vulnerable, so is the application(s)
- Often these updates can be neglected, as they need stakeholder buy-in, team collaboration, etc.
- Any time addressing a vulnerability is time NOT spent on features
- Organisations should take steps to prevent vulnerabilities:
  - Know what the available assets are
  - Know if each component is vulnerable or not - research known vulnerabilities and proactively test applications
  - Update out-of-date software and patch known vulnerabilities
- Vulnerabilities and outdated components are often not a technical problem - instead a people and process problem
  - Stakeholder buy-in is often needed
  - A robust and repeatable process that covers asset inventory, vulnerability discovery, and remediation is needed.

## 1.7 - Identification and Authentication Failures

## 1.8 - Software and Data Integrity Failures

## 1.9 - Security Logging and Monitoring Failures

## 1.10 - Server-Side Request Forgery
