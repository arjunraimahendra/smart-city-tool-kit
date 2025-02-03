ppp_framework_prompt = """ 
You are a research assistant tasked with creating a comprehensive, structured literature review on jobs and growth in cities located in the Middle East and North Africa (MENA) region. Your primary focus is on the city of **{city}** in **{country}**.

**Contextual Information Provided:**
- **Analytical Framework:** The analysis follows the "People, Production, Places" framework, which emphasizes:
  - People: Human capital, labor markets, and skills development
  - Production: Industrial structures, productivity, and value chains
  - Places: Urban infrastructure, spatial dynamics, and livability
- **Cross-cutting Themes:**
  - Gender Equality
  - Climate Change
  - Digital Transformation
  - Governance and Institutions
- **Local Context:** You have information about local institutions and stakeholders in **{city}**, **{country}** (**{stakeholders}**), who influence urban development and economic growth.

**Task Requirements:**
1. **Literature Review Structure:**  
   Construct a detailed, hierarchical literature review that:
   - Follows the provided structure focusing on People, Production, and Places
   - Incorporates cross-cutting themes throughout the analysis
   - Addresses both constraints and opportunities specific to **{city}**
   - Emphasizes evidence-based findings and policy implications

2. **Subsection-Specific Search Strategy:**  
   For each subsection, provide **{max_num_queries}** targeted search queries that:
   - Align with the specific focus area
   - Target both academic and policy literature
   - Seek empirical evidence and case studies
   - Include city-specific and comparative regional analyses

**Output Format:**
Present the literature review outline in the following structure and take into consideration the user provided structure recommendations {report_structure}:

1. **Introduction**
   1.1. **Urban Job Creation Context in MENA**
   1.2. **Review Scope and Objectives**
   1.3. **Methodology and Sources**

2. **Conceptual Framework**
   2.1. **People, Production, Places Framework**
   2.2. **Theory of Change**
   2.3. **Application to MENA Context**

3. **Urban Context in MENA Region**
   3.1. **Spatial Characteristics**
        - City Size and Distribution
        - Urban Growth Patterns
        - Regional Connectivity
        - City Hierarchy Analysis
   
   3.2. **Economic Structure**
        - Production vs Consumption Cities
        - Sectoral Composition
        - Economic Concentration
        - Regional Corridors
   
   3.3. **Labor Market Overview**
        - Employment Patterns
        - Formal-Informal Balance
        - Skills Distribution
        - Wage and Productivity Trends

4. **Places Analysis**
   4.1. **Urban Infrastructure**
   4.2. **Land Markets**
   4.3. **Housing Systems**
   4.4. **Basic Services**
   4.5. **Commercial Space**
   4.6. **Environmental Resilience**
   4.7. **Urban Governance**

5. **Production Analysis**
   5.1. **Industry Clusters**
   5.2. **Business Environment**
   5.3. **Innovation Systems**
   5.4. **Market Access**
   5.5. **Firm Dynamics**
   5.6. **Investment Patterns**
   5.7. **Infrastructure Impact**

6. **People Analysis**
   6.1. **Human Capital**
   6.2. **Labor Market Frictions**
   6.3. **Social Inclusion**
   6.4. **Opportunity Access**
   6.5. **Quality of Life**
   6.6. **Demographic Trends**

7. **Cross-cutting Themes**
   7.1. **Gender Equality Integration**
   7.2. **Climate Change Response**
   7.3. **Digital Transformation**
   7.4. **Governance Systems**

8. **Urban Constraints and Opportunities**
   8.1. **Cross-cutting Challenges**
   8.2. **City-specific Opportunities**

9. **Policy Implications**
   9.1. **Short-term Interventions**
   9.2. **Long-term Reforms**

10. **Synthesis**
    10.1. **Key Findings**
    10.2. **Research Gaps**
    10.3. **Monitoring Frameworks**

Give important to the literature review outline structure provided by the user: {report_structure}

---

**Example Output Section:**

**4. Places Analysis**
   
   **4.1. Urban Infrastructure**
   - Example Queries:
     - "Empirical assessment of infrastructure quality and economic growth in {city}, {country} 2015-2025"
     - "Impact evaluation of transport connectivity on job access in {city}, {country}"
     - "Comparative analysis of infrastructure investment returns across MENA cities vs. {city}, {country}"

   **4.2. Land Markets**
   - Example Queries:
     - "Land market efficiency and business growth in {city}, {country}"
     - "Effects of zoning regulations on commercial development in {city}, {country}"
     - "Land value capture mechanisms in MENA urban development vs. {city}, {country}"

   **4.3. Housing Systems**
   - Example Queries:
     - "Housing affordability impact on labor mobility in {city}, {country}"
     - "Worker housing programs effectiveness in {city}, {country} urban areas"
     - "Housing market reforms and economic growth in MENA cities vs. {city}, {country}"
"""



stakeholder_prompt = """ 
Please provide a comprehensive list of key stakeholders and institutions involved in urban development, employment, and economic growth policies for {city} in {country}. For each entity, include:

1. Institution/Organization Name
2. Role: A brief description of their primary responsibilities and scope of influence in urban development and job creation
3. Key Interlocutors: Names and titles of principal decision-makers or representatives (where applicable)

Please include stakeholders from the following categories:

- National-level ministries or departments responsible for:
  * Urban development and housing
  * Economic planning and development
  * Local administration
  * Labor and employment
  * Industry and trade

- Regional/State/Provincial governing bodies overseeing the city

- City-level authorities and planning agencies

- Industry associations and chambers of commerce

- Development authorities or special purpose vehicles

- Relevant regulatory bodies

- Key public-private partnership entities

- Major civil society organizations and community representatives

For each stakeholder, emphasize their specific role in:
- Urban planning and development
- Job creation and employment
- Economic growth initiatives
- Infrastructure development
- Local governance
- Industry and business development

Please format each entry following this structure:
[Institution Name]:
Role: [Detailed description of responsibilities]
Key Interlocutors: [Names and titles of key decision-makers]

Examples:

The stakeholders should be categorized based on their roles and responsibilities, similar to the following example:*

1. **Ministry/Department of Housing, Urban Development, and Infrastructure**  
   - **Role:** Oversees urban planning, housing projects, and infrastructure development in [City Name].  
   - **Key Interlocutor:** Minister/Secretary of [Housing/Urban Development Department].  

2. **Urban Development Authority/Agency**  
   - **Role:** Responsible for planning and developing new urban areas and managing existing ones in [City Name].  
   - **Key Interlocutor:** Director/Chairperson of [Urban Development Authority].  

3. **Ministry/Department of Planning and Economic Development**  
   - **Role:** Formulates long-term economic development plans and manages public investments.  
   - **Key Interlocutor:** Minister/Secretary of Planning and Economic Development.  

4. **Governorate/State Administration**  
   - **Role:** Administers [City Name] at the regional/state level, overseeing governance and development.  
   - **Key Interlocutor:** Governor of [City Name].  

5. **Local City Development Authorities**  
   - **Role:** Manage city-level planning, zoning regulations, and infrastructure development.  
   - **Key Interlocutors:** Heads of City Development Authorities for key districts in [City Name].  

6. **Ministry/Department of Local Government and Administration**  
   - **Role:** Coordinates municipal functions, local governance, and community development efforts.  
   - **Key Interlocutor:** Minister/Secretary of Local Government.  

7. **Ministry/Department of Labor and Workforce Development**  
   - **Role:** Oversees labor policies, employment programs, and skill development initiatives in [City Name].  
   - **Key Interlocutor:** Minister/Secretary of Labor and Workforce Development.  

8. **Ministry/Department of Trade and Industry**  
   - **Role:** Develops industrial policies, supports trade, and facilitates investment to promote economic growth.  
   - **Key Interlocutor:** Minister/Secretary of Trade and Industry.  

9. **Chamber of Commerce & Industry/Business Federation**  
   - **Role:** Represents private sector businesses, advocating for policies that support economic growth.  
   - **Key Interlocutor:** President/Chairman of [City Name] Chamber of Commerce & Industry.  

10. **Civil Society Organizations and Community Leaders**  
   - **Role:** Represent grassroots interests and provide insights on social and economic issues.  
   - **Key Interlocutors:** Leaders of prominent local NGOs and community associations in [City Name].  

Ensure that the response is specific to the city and country provided, referencing real institutions and government bodies where possible.

"""


### Variables
# city = "Sadat City"
# country = "Egypt"
max_num_queries = 5
policy_levers = [
    "Property tax abatements",
    "Sales tax exemptions",
    "Corporate income tax credits",
    "Utility rate reductions",
    "Land cost subsidies",
    "Relocation assistance grants",
    "Employee hiring credits",
    "Research and development tax credits",
    "Equipment purchase incentives",
    "Infrastructure cost-sharing",
    "Industry cluster development programs",
    "Supply chain attraction initiatives",
    "Business retention visitation programs",
    "Anchor institution partnerships",
    "Regional business alliances",
    "Industry-specific support centers",
    "Business improvement districts",
    "Joint purchasing programs",
    "Shared service facilities",
    "Cross-industry networking initiatives",
    "One-stop business centers",
    "Expedited permitting processes",
    "Business liaison officers",
    "Site selection assistance",
    "Utility connection fast-tracking",
    "Environmental compliance support",
    "International business support services",
    "Multilingual business services",
    "Business registration assistance",
    "Regulatory navigation support",
    "Industry-specific skill training",
    "Apprenticeship programs",
    "Digital skills bootcamps",
    "Language training programs",
    "Professional certification programs",
    "Career transition assistance",
    "Soft skills development",
    "Management training programs",
    "Technical education programs",
    "Online learning platforms",
    "University research partnerships",
    "Community college collaborations",
    "High school vocational programs",
    "Corporate training centers",
    "Industry-academia joint ventures",
    "Student internship programs",
    "Teacher externship programs",
    "Curriculum development partnerships",
    "Education equipment sharing",
    "Joint research facilities",
    "Job matching services",
    "Career counseling centers",
    "Labor market information systems",
    "Remote work support programs",
    "Commuter assistance programs",
    "Childcare support services",
    "Worker retention programs",
    "Skills assessment services",
    "Professional networking events",
    "Job fairs and recruitment events",
    "Municipal broadband networks",
    "Public Wi-Fi systems",
    "Smart city sensor networks",
    "Data centers",
    "5G infrastructure",
    "Digital inclusion programs",
    "Smart grid systems",
    "IoT platforms",
    "Cybersecurity systems",
    "Digital payment infrastructure",
    "Public transit systems",
    "Bike infrastructure",
    "Pedestrian facilities",
    "Electric vehicle charging",
    "Smart traffic management",
    "Parking management systems",
    "Transportation hubs",
    "Last-mile connectivity",
    "Freight logistics facilities",
    "Autonomous vehicle infrastructure",
    "Industrial parks",
    "Research campuses",
    "Mixed-use developments",
    "Convention centers",
    "Sports facilities",
    "Cultural venues",
    "Public markets",
    "Green spaces",
    "Water/wastewater systems",
    "Waste management facilities",
    "Research and development grants",
    "Innovation vouchers",
    "Technology demonstration sites",
    "Living labs",
    "Maker spaces",
    "Innovation districts",
    "Technology parks",
    "Creative hubs",
    "Design centers",
    "Testing facilities",
    "University technology transfer offices",
    "Patent assistance programs",
    "Commercialization support",
    "Research collaboration platforms",
    "Industry-academia exchanges",
    "Innovation competitions",
    "Hackathons",
    "Technology showcases",
    "Knowledge sharing networks",
    "Innovation mentorship programs",
    "Arts districts",
    "Public art programs",
    "Cultural festivals",
    "Performance venues",
    "Museum support",
    "Historical preservation",
    "Cultural education programs",
    "Artist residencies",
    "Creative space subsidies",
    "Cultural tourism initiatives",
    "Green building incentives",
    "Renewable energy programs",
    "Urban farming initiatives",
    "Waste reduction programs",
    "Air quality management",
    "Water conservation initiatives",
    "Green space development",
    "Climate resilience planning",
    "Environmental education",
    "Sustainable transportation",
    "Affordable housing programs",
    "Public safety initiatives",
    "Healthcare access programs",
    "Recreation facilities",
    "Community centers",
    "Public libraries",
    "Education facilities",
    "Senior services",
    "Youth programs",
    "Social service coordination",
    "Municipal bonds",
    "Tax increment financing",
    "Special assessment districts",
    "Development impact fees",
    "User fees and charges",
    "Special purpose taxes",
    "Revenue sharing agreements",
    "Public-private partnerships",
    "Infrastructure banks",
    "Green bonds",
    "Angel investor networks",
    "Venture capital attraction",
    "Private equity partnerships",
    "Crowdfunding platforms",
    "Investment pools",
    "Real estate investment trusts",
    "Community development financial institutions",
    "Microfinance programs",
    "Local investment funds",
    "Foreign direct investment programs",
    "Zoning flexibility",
    "Density bonuses",
    "Historic preservation incentives",
    "Environmental fast-tracking",
    "Self-certification programs",
    "Code compliance assistance",
    "Regulatory sandboxes",
    "Performance-based regulations",
    "Small business exemptions",
    "Sunset provisions",
    "Online permitting systems",
    "Integrated review processes",
    "Pre-application conferences",
    "Technical assistance programs",
    "Process mapping services",
    "Regulatory impact analysis",
    "Fee waiver programs",
    "Permit expediting",
    "Mobile inspection services",
    "Electronic plan review",
    "Export readiness programs",
    "Trade mission support",
    "International marketing assistance",
    "Export financing",
    "Trade compliance assistance",
    "Language services",
    "Cultural training",
    "Market research support",
    "Trade show assistance",
    "Export insurance programs",
    "Foreign investment offices",
    "International desk services",
    "Sister city programs",
    "Investment promotion events",
    "Familiarization tours",
    "Investment incentive packages",
    "International business centers",
    "Overseas representation",
    "Investment matchmaking",
    "Diplomatic relations support",
    "Manufacturing modernization",
    "Supply chain optimization",
    "Energy efficiency programs",
    "Process improvement support",
    "Equipment upgrade assistance",
    "Quality certification support",
    "Market diversification",
    "Product development assistance",
    "Workforce upskilling",
    "Technology adoption support",
    "Startup accelerators",
    "Industry-specific incubators",
    "Technology commercialization",
    "Proof of concept support",
    "Growth scaling programs",
    "Market validation support",
    "Prototype development",
    "Patent support",
    "Research collaboration",
    "Pilot project funding",
    "Business planning assistance",
    "Market research support",
    "Financial management training",
    "Marketing assistance",
    "Legal services",
    "Accounting support",
    "Technology adoption help",
    "Succession planning",
    "Procurement assistance",
    "Networking events",
    "Microlending programs",
    "Loan guarantee programs",
    "Equipment financing",
    "Working capital loans",
    "Emergency relief funds",
    "Grant programs",
    "Equity investment matching",
    "Crowdfunding support",
    "Revenue-based financing",
    "Bridge financing"
]

user_provided_institutions = """ 
Ministry of Housing, Utilities & Urban Communities (MoHUUC):
Role: Oversees urban planning, housing projects, and the development of new urban communities across Egypt.
Key Interlocutor: Minister Assem El Gazzar. 


New Urban Communities Authority (NUCA):
Role: Affiliated with MoHUUC, NUCA is responsible for planning and developing new urban areas, including 10th of Ramadan and Sadat City.
Key Interlocutors: Vice President Abdel-Muttalib Mamdouh and Assistant Vice President Engineer Gamal Talaat. 


Ministry of Planning and Economic Development (MPED):
Role: Formulates sustainable development plans and manages public investments to promote economic growth.
Key Interlocutor: Counsellor Mohamed Abdel-Wahab, CEO. 


Governorates of Cairo, Sharqia, and Monufia:
Role: Each governorate administers its respective region, with Cairo Governorate overseeing Cairo, Sharqia Governorate overseeing 10th of Ramadan, and Monufia Governorate overseeing Sadat City.
Key Interlocutors: The Governors of Cairo, Sharqia, and Monufia, respectively.


Local City Development Authorities:
Role: Manage city-level planning and development initiatives.
Key Interlocutors: Heads of the City Development Authorities for Cairo, 10th of Ramadan, and Sadat City.


Ministry of Local Development:
Role: Coordinates local administration efforts and implements development projects at the local level.
Key Interlocutor: The Minister of Local Development.


Ministry of Manpower:
Role: Responsible for labor market policies, employment services, and workforce development.
Key Interlocutor: The Minister of Manpower.


Ministry of Trade and Industry:
Role: Develops industrial policies and promotes trade to stimulate economic growth.
Key Interlocutor: The Minister of Trade and Industry.


Federation of Egyptian Industries (FEI):
Role: Represents the industrial sector, advocating for policies that support industrial growth and employment.
Key Interlocutor: The Chairman of FEI.


Civil Society Organizations and Community Leaders:
Role: Provide grassroots insights and represent citizen interests in urban development projects.
Key Interlocutors: Leaders of prominent local NGOs and community associations in each city.

"""