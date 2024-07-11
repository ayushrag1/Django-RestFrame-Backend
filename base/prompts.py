CONTRACT_TEMPLATE = """
CONTRACT AGREEMENT

This Contract Agreement (the "Agreement") is made and entered into as of [Date], by and between:

Party 1:
Name: __________________________
Address: ________________________
Phone: __________________________
Email: __________________________

Party 2:
Name: __________________________
Address: ________________________
Phone: __________________________
Email: __________________________

Scope of Work:
Party 1 agrees to provide the following services/products to Party 2:

Terms and Conditions:

Term: This Agreement shall commence on [Start Date] and shall continue until [End Date] or until the completion of the \
    services/products as described above.

Payment:
a. The total fee for the services/products is $__________.
b. Payment shall be made as follows:

[Amount] upon signing of this Agreement.
[Amount] upon completion/delivery of services/products.
c. Payment shall be made via [Payment Method] to [Payment Details].

Confidentiality: Both parties agree to keep all terms of this Agreement and any information exchanged during the term \
    of this Agreement confidential.

Termination: Either party may terminate this Agreement with [Number] days' written notice to the other party. In the \
    event of termination, Party 1 shall be compensated for all services/products rendered up to the date of termination.

Indemnification: Each party agrees to indemnify and hold harmless the other party from any claims, damages, or \
    liabilities arising out of or related to this Agreement.

Governing Law: This Agreement shall be governed by and construed in accordance with the laws of the State of [State].

Entire Agreement: This Agreement constitutes the entire agreement between the parties and supersedes all prior \
    negotiations, representations, or agreements, whether written or oral.

Amendments: Any amendments or modifications to this Agreement must be made in writing and signed by both parties.

Signatures:

Party 1 (Signature)
Date: ___________________

Party 2 (Signature)
Date: ___________________"""


CONTRACT_TEXT = """
This Software Development Agreement ("Agreement") is made and entered into as of the 15th day of May, 2024, by and \
    between Acme Solutions Inc., having its principal place of business at 123 Main Street, Anytown, USA ("Client"), \
        and DevTech Solutions LLC, having its principal place of business at 456 Elm Street, Anycity, USA ("Developer").

Scope of Work
1.1 Developer agrees to design, develop, and deliver a custom software solution ("Software") according to the \
    specifications provided by Client.

1.2 The Software shall include features such as user authentication, data management, and reporting functionalities.

1.3 Developer shall provide regular progress updates and seek Client's approval at key milestones during the \
    development process.

Payment Terms
2.1 Client agrees to pay Developer a total fee of $50,000 for the development of the Software.

2.2 Payment shall be made in three installments as follows: 50% upon signing of this Agreement, 25% upon delivery of \
    the initial prototype, and the remaining 25% upon final delivery and acceptance of the Software.

2.3 In the event of any delay in payment exceeding 30 days, Developer reserves the right to suspend work until payment \
    is received.

Pricing Model
3.1 The total fee for the development of the Software shall be $50,000, which is based on an estimated 500 hours of \
    work at a rate of $100 per hour.

3.2 Additional work requested by Client that is outside the scope of the initial specifications will be billed at an \
    hourly rate of $120 per hour.

3.3 Any changes to the scope of work that affect the overall cost will be documented and agreed upon in a written \
    change order before additional work begins.

3.4 In case of early termination of the Agreement by the Client, the Client agrees to pay for the hours worked up to \
    the date of termination at the rate of $100 per hour.

Intellectual Property
4.1 All intellectual property rights, including copyrights and patents, related to the Software developed under this \
    Agreement shall belong to Client upon full payment.

4.2 Developer retains the right to reuse any pre-existing code or components not specific to the Software developed \
    under this Agreement.

Confidentiality
5.1 Both parties agree to maintain the confidentiality of any proprietary or sensitive information disclosed during \
    the course of this Agreement.

5.2 Confidential information includes, but is not limited to, software code, business processes, and financial data.

Warranties and Disclaimers
6.1 Developer warrants that the Software will be free from defects and will perform in accordance with the \
    specifications provided.

6.2 Client acknowledges that the Software is provided "as is" and that Developer makes no warranties, express or \
    implied, regarding its fitness for a particular purpose.

Limitation of Liability
7.1 Neither party shall be liable to the other for any indirect, incidental, or consequential damages arising out of \
    or in connection with this Agreement.

7.2 In no event shall either party's total liability exceed the total amount paid by Client under this Agreement.

Term and Termination
8.1 This Agreement shall commence on the 15th day of May, 2024, and shall continue until the completion of the \
    Software development or until terminated by either party upon 30 days' written notice.

8.2 Upon termination, Client shall pay Developer for all work completed up to the date of termination.

Governing Law and Dispute Resolution
9.1 This Agreement shall be governed by and construed in accordance with the laws of the State of California.

9.2 Any dispute arising out of or in connection with this Agreement shall be resolved through arbitration in \
    accordance with the rules of the American Arbitration Association.

Miscellaneous
10.1 This Agreement constitutes the entire understanding between the parties and supersedes all prior agreements and \
    understandings, whether written or oral.

10.2 Amendments to this Agreement must be made in writing and signed by both parties.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.

Client Name: John Doe

By: [Signature]

Name: John Doe

Title: CEO

Date: May 15, 2024

Developer Name: Jane Smith

By: [Signature]

Name: Jane Smith

Title: President

Date: May 15, 2024"""


REVENUE_LEAKAGE_POINTS = """
Manual Invoicing Errors:

Delays in invoice generation leading to omission of billable services or underestimation of billable time.
Spreadsheet Inaccuracies:

Errors in manually entered data, such as time tracking or service details, leading to underbilling or incorrect \
    invoicing.
Inaccurate Customer Information:

Incorrect or outdated data about customer volumes, leading to missed billing opportunities or incorrect invoicing.
Pricing Errors:

Continuing promotional pricing beyond its intended period or incorrectly applying volume discounts, resulting in \
    revenue loss.
Lax Discount Policies:

Salespeople offering unnecessary discounts, leading to revenue leakage through reduced margins.
Unclear Policy Communication:

Lack of immediate access to policy information for sales staff, resulting in undercharging or incorrect invoicing.
Underbilling for Services:

Failure to bill for all billable services rendered, especially prevalent in service-oriented businesses, leading to \
    revenue loss.
Unenforced Penalty Fees:

Failure to enforce penalty fees for contract violations or infractions, resulting in missed revenue opportunities.
Poor Data Integration:

Incompatibility between systems leading to data silos and incomplete or inaccurate financial records, causing revenue \
    discrepancies.
Manual Data Entry Errors:

Mistakes during manual data entry processes, such as miskeying numbers or overlooking billing details, leading to \
      underbilling or missed revenue."""


CONTRACT_INFO_EXTRACTION = """
As an intelligent assistant, your task is to extract detailed information related to the specified PARAMETERS from \
    the provided CONTRACT TEXT. Ensure that your extraction is as comprehensive as possible for each parameter.

CONTRACT TEXT:
{contract_chuncked_text}

PARAMETERS:

1. Payment Amount
2. Payment Schedule
3. Incentives and Penalties
4. Price Adjustment Clauses
5. Scope of Work
6. Deliverables
7. Quality Standards
8. Contract Duration
9. Termination Clauses
10. Renewal Terms
11. Roles and Responsibilities
12. Compliance Requirements
13. Reporting and Monitoring
14. Liability Clauses
15. Insurance Requirements
16. Force Majeure
17. Governing Law
18. Arbitration and Mediation
19. Litigation
20. Confidentiality Clauses
21. Intellectual Property Rights
22. Amendment Procedures
23. Flexibility
24. Key Performance Indicators
25. Service Level Agreements
26. Subcontracting
27. Third-Party Approvals

Important Instructions:

- Only include details from the CONTRACT TEXT that are directly related to the PARAMETERS listed above.
- Do not include any information unrelated to the PARAMETERS.
- If a parameter's details are not present in the CONTRACT TEXT, do not include that parameter in generated response \
    for that parameter.
"""
