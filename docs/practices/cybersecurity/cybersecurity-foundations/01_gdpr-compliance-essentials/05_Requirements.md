# 5.0 - Requirements

## 5.1 - Legal Basis

- Organisations must identify their need to gather and process data in order to determine a lawful basis
- Basis: The minimum, fundamental support of a thing or system
- Lawful basis: a reason for processing that is justified by law
  - Has regulatory provisions to govern it
- GDPR Basis for Processing Data:
  
1. Consent
   1. Given by the data subject, and can be revoked at any time
2. Contractual Necessity
   1. Required when organisations are entering or performing a contract, or responding to a data subject request
3. Complicance with Legal Obligation
   1. Applies to EU member states only
4. Protect Vital Interest
   1. All data should remain private unless the information may lead to external harm if not acted on
5. Legitimate Interest
   1. Complies with proportionality and subsidarity
   2. Not absolute
   3. Needs compelling ground that overrides freedoms of data subject
   4. Data is required to exercise legal rights
6. Public Interest
   1. When an official authority vested in controller
   2. Not absolute
   3. Compelling ground that overrides freedoms of data subject
   4. Data required to exercise legal rights

## 5.2 - Document Activities

- Suppose a PIA is underway, it's required that the findings are documented in an acceptable manner.
- Data should be classified as sensitive or confidential where required.
  - This could be done via methods like tagging.
- This exercise is known as Data mapping and comprises of three steps:
  - Data discovery: Outline what data is being transferred to and where it ends up
  - Data Collection Lifecycle: Is there any unexpected and unnecessary usage of the data during its lifecycle? Can this be trimmed?
  - Data Mapping: Verify the key elements to determine appropriate safeguards e.g. what to do for highly confidential data.
    - Elements include:
      - Collection - category and nature?
      - Storage - how and in what format?
      - Transfer method between organisations - internal and external parties
      - Retention
      - Location of storage
      - Accountability - Who is responsible for the data
- Example: Date of birth of associate
  - Classification - confidential
  - Data flow: internal from US data entry to US system of record
  - Data use: internal only
  - Safeguards: limit access to system and encrypt data

## 5.3 - Technical Measures

- 4 components outlined for implementing technical controls to ensure a level of security appropriate to the risk.

1. Anonymize and Encrypt Personal Data
   1. Data in transit and at rest should be considered - utilse TLS and AES for the respective data states
2. Confidentiality, Integrity, and Availability (CIA)
   1. Resilience of processing systems and services
   2. Can review [CIS Controls](https://cisecurity.org/controls)
   3. Controls considered for the likes of inventory, vulnerability assessment, malware, data protection, monitoring, and training
3. Ability to Restore
   1. In the event of physical or technical incident, availability and access must be restored
   2. Processes must be tested and results logged regularly
4. Regular Testing and Evaluation
   1. Ensure the security of the processing measures

## 5.4 - Notification

- In the event of a breach, relevant parties must be notified
- If a breach is likely to result in a risk to the rights and freedoms of natural persons, you must notify, including the supervisory authority.
- Personal data breach:
  - A breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to, personal data transmitted, stored, or otherwise processed.
- Once a processor becomes aware of a breach, notification is expected within a particular timeframe, including if the processor is separate to the controller.
- Supervisory authorities must be made aware within 72 hours of the data processor noticing and verifying a breach
  - The only exception is when the breach is unlikely to result in a risk to subject's rights
  - If no notification is received within 72 hours, an explanation is required.
- When notifying, the following requirements or information must be outlined:
  - Nature of the breach: Number of people involved and what records
  - DPO contact information
  - Likely consequences
  - Proposed mitigation efforts
- The information can be provided in phases
- Regarding data subjects:
  - Notification must be sent without undue delay
  - Clear and plain language must be used, as well as outlining
    - The nature of the breach
    - DPO contact information
    - Likely consequences
    - Proposed mitigations
