#!/usr/bin/env python3
"""Rebuild Quizzer.html with full topic coverage and install button."""
import json
import re
import random

random.seed(42)
KEYS = [0, 1, 3, 2, 1, 0, 2, 3, 3, 0, 1, 2, 1, 0, 2, 3, 3, 0, 2, 1, 0, 1, 3, 2, 2, 0, 1, 3, 0, 1, 3, 2, 2, 1, 3, 0, 3, 2, 0, 1, 0, 3, 2, 1, 1, 3, 0, 2, 1, 2, 0, 3, 0, 2, 3, 1, 2, 0, 3, 1, 1, 3, 2, 0, 1, 3, 0, 2, 3, 1, 2, 0, 2, 0, 1, 3, 2, 1, 3, 0, 1, 3, 2, 0, 3, 1, 2, 0, 2, 0, 1, 3, 3, 2, 1, 0, 1, 0, 3, 2, 0, 1, 2, 3, 3, 2, 0, 1, 3, 2, 1, 0, 0, 3, 1, 2, 2, 0, 3, 1, 1, 2]

# type, topic, question, correct, wrong[3], explain_c, explain_w[3]
RAW = [
("Definition","1.1 Macro View","What best describes a macro view in technopreneurship?",
 "Analysis of large-scale economic, industry, or market trends affecting society as a whole",
 ["Focus on individual customer purchase decisions only","Detailed study of one company's internal operations","Micro-level analysis of a single product feature"],
 "A macro view examines broad external forces—industry shifts, social developments, technical advancements, and economic trends—that shape entire markets.",
 ["Individual purchases are micro-level behavior.","Internal operations are micro analysis.","Product features are micro details, not macro patterns."]),

("Application","1.1 Economic Forces","A startup founder notices the global rise of gig workers and builds a financial app for freelancers. Which macro force did they observe?",
 "Economic forces",
 ["Industry trends only","Social developments only","Technical advancements only"],
 "The gig economy reflects shifting income models and labor markets—a core economic force at the macro level.",
 ["Industry trends are sector-specific; gig work spans industries as an economic pattern.","Social behavior plays a role, but the primary lens here is economic.","Technology enables gig work, but changing earning models are economic forces."]),

("Situational","1.2 Why Macro View","Without a macro perspective, entrepreneurs often end up:",
 "Constantly putting out fires instead of being proactive",
 ["Automatically attracting investors","Never needing customer segments","Skipping all problem validation"],
 "Avoiding macro view creates a myopic perspective—you react to daily crises instead of anticipating industry-wide shifts.",
 ["Investors want trend alignment; reactive founders struggle to demonstrate it.","Customer segments remain essential regardless of macro view.","Problem validation is still required; macro view complements it."]),

("Definition","1.4 Genius of the AND","According to Jim Collins in Good to Great, successful analysis requires:",
 "Both macro and micro analysis skills",
 ["Only macro analysis","Only micro analysis","Neither—intuition alone is sufficient"],
 "Collins' 'genius of the AND' means zooming OUT for trends and zooming IN for operations and customer behaviors.",
 ["Macro alone misses customer behavior and operations.","Micro alone misses industry trends and external threats.","Collins argues for structured dual analysis, not intuition alone."]),

("Application","1.4 Climate Macro","Which pair represents macro/industry-level responses to climate change?",
 "Wind/solar farms and development of bio-plastics",
 ["Avoiding single-use plastic at home","Using energy-efficient appliances personally","Biking instead of driving locally"],
 "Macro/industry responses include renewable energy infrastructure, nuclear power, EVs, and bio-plastics—between personal habits and global treaties.",
 ["Avoiding plastic is a personal/local micro action.","Energy-efficient appliances are micro/personal-level.","Biking is a micro personal transportation choice."]),

("Definition","1.5 SDGs","The UN Sustainable Development Goals (SDGs) consist of how many goals?",
 "17",
 ["15","12","21"],
 "The UN adopted 17 SDGs—from No Poverty to Partnerships—as a macro map of global problem areas for entrepreneurs.",
 ["The official UN framework has 17 goals, not 15.","12 understates the SDG agenda.","21 exceeds the adopted SDG count."]),

("Application","1.5 SDG Clean Water","An entrepreneur explores SDG 6 (Clean Water and Sanitation) for venture ideas. SDGs primarily serve as:",
 "A ready-made macro map of real-world problem areas",
 ["A substitute for customer personas","A tool to skip problem validation","A financial accounting framework"],
 "SDGs help entrepreneurs discover macro-level challenges aligned with passion and societal impact.",
 ["Personas profile customers; SDGs map global problems—they complement each other.","Validation remains essential after choosing a problem area.","SDGs are not financial frameworks."]),

("Situational","2.3 Well-Stated Problem","A founder pitches: 'We will offer stock-market training to college students.' What is wrong?",
 "It describes a solution, not a problem",
 ["It is too specific about the target market","It names the pain point clearly","It identifies a dying industry"],
 "Problem identification must start with pain or gap—not the product you plan to build.",
 ["Specificity isn't the issue; jumping to a solution is.","It doesn't describe pain—it states what the company will offer.","Stock-market education isn't framed as a dying industry here."]),

("Definition","2.1 Uri Levine","Uri Levine, co-founder of Waze, advises founders to:",
 "Fall in love with the problem, not the solution",
 ["Fall in love with the first product idea","Focus on competitors before customers","Skip problem validation to move fast"],
 "Levine stresses problem identification as the foundation for all later venture decisions.",
 ["Product attachment too early causes tunnel vision.","Competitors matter, but problem clarity comes first.","Skipping validation contradicts Levine's philosophy."]),

("Application","2.3 Well-Stated Problem","Which statement is a WELL-STATED problem?",
 "Despite high interest, many college students lack the knowledge and discipline to invest well in stock markets",
 ["We will offer stock-market training to college students","New-age investment apps are bringing younger investors into the market","College students need to start saving and investing"],
 "A well-stated problem names who is affected and the specific pain—not a solution, trend, or vague wish.",
 ["This is a solution, not a problem.","This describes a market trend, not a defined pain.","This is too vague—it lacks a specific barrier or pain point."]),

("Situational","2.5 Filter #5","Your team hasn't checked if the problem was already solved many times. Which filter did they skip?",
 "Filter #5: Has it not already been solved too many times (is there real demand)?",
 ["Filter #1: Is it a relevant problem (not dying)?","Filter #2: Is your team passionate about it?","Filter #4: Is it highly painful or desirable to solve?"],
 "Filter #5 checks market saturation—whether genuine demand still exists for another solution.",
 ["Filter #1 checks relevance, not saturation.","Filter #2 checks team passion.","Filter #4 checks pain/desirability, not oversupply."]),

("Definition","2.9 5 Whys","The 5 Whys root cause technique was developed by:",
 "Sakichi Toyoda, founder of Toyota",
 ["Steve Jobs, founder of Apple","Jim Collins, author of Good to Great","Uri Levine, co-founder of Waze"],
 "Sakichi Toyoda created the 5 Whys at Toyota to trace recurring symptoms to underlying root causes.",
 ["Jobs is associated with product design, not 5 Whys.","Collins wrote Good to Great; 5 Whys is a Toyota tool.","Levine focuses on problem-first thinking, not 5 Whys authorship."]),

("Application","2.9 5 Whys Example","In the classroom lateness 5 Whys example, the root cause identified is:",
 "Poor discipline and lack of a clear daily schedule",
 ["Waking up late only","Using social media at night","Having too much homework"],
 "Five iterations reveal poor schedule discipline—not the surface symptom of waking late.",
 ["Waking late is level-1 symptom, not root cause.","Social media is an intermediate cause.","Homework wasn't the identified root in this example."]),

("Situational","2.6 Fall in Love","A founder is attached to their app design but hasn't confirmed users face the problem. They should:",
 "Fall in love with the problem instead of the solution",
 ["Apply geographic segmentation first","Use SDGs and skip validation","Focus only on competitor copying"],
 "Attachment to a solution before validating the problem's reality and scale is a classic startup mistake.",
 ["Segmentation doesn't replace problem validation.","SDGs inspire problems but don't validate yours.","Copying competitors skips genuine problem understanding."]),

("Definition","2.8 Problem Analysis","Problem analysis asking 'Who is Impacted by it? How?' helps innovators:",
 "Understand affected people and how they experience the pain",
 ["Choose brand colors and logos","Skip customer empathy entirely","Write financial projections only"],
 "Knowing who suffers and how they experience the problem builds empathy and sharper problem statements.",
 ["Branding comes after problem clarity.","This question builds empathy—it doesn't replace it.","Financials are separate from impact analysis."]),

("Application","2.7 Impact over Ego","Which problem-analysis benefit means prioritizing meaningful impact over defending your first idea?",
 "Impact over Ego",
 ["Open-mindedness","Customer Empathy","Market Segmentation"],
 "Impact over Ego keeps founders flexible—they solve the real problem rather than protect their initial concept.",
 ["Open-mindedness means considering multiple solutions.","Customer Empathy means stepping into customers' shoes.","Segmentation divides markets—it isn't a problem-analysis benefit."]),

("Situational","2.2 Validate Problems","During validation your team asks: 'Who faces this and how urgent is it?' This is the:",
 "Validate Problems stage",
 ["Be Curious stage","Generate Ideas stage","Identify Problems stage"],
 "Validation confirms who is affected and how important/urgent the problem is before building solutions.",
 ["Being curious is the initial observation phase.","Idea generation follows validated problems.","Identification precedes validation."]),

("Definition","2.3 Well-Stated Problem","A well-stated problem should NOT be:",
 "A market trend or a proposed solution",
 ["Specific about who is affected","Focused on a real pain point","Concise and clear"],
 "Trends describe market movement; solutions describe products—neither is a problem statement.",
 ["Naming affected people is essential.","Describing pain is core to problem statements.","Conciseness aids communication."]),

("Application","2.4 Problem ID Steps","Problem identification steps include all EXCEPT:",
 "Launch the product immediately to test the market",
 ["Identify gaps and pain points in the industry","Determine who suffers from the pain","Create a concise problem statement"],
 "The process builds understanding and a clear statement before any product launch.",
 ["Gap identification is the first step.","Determining sufferers is explicit in the process.","Problem statement creation is the final listed step."]),

("Situational","2.7 Open-mindedness","An innovator considers multiple solutions instead of fixating on one. This reflects:",
 "Open-mindedness",
 ["Impact over Ego","Customer Empathy","Behavioural segmentation"],
 "Open-mindedness keeps innovators flexible about HOW to solve a validated problem.",
 ["Impact over Ego deprioritizes defending one's idea.","Customer Empathy focuses on the customer's experience.","Behavioural segmentation is a market tool, not a problem-analysis benefit."]),

("Definition","M2 Intro Customer Centricity","Module 2 states that being customer-centric is:",
 "A requirement, not an optional choice, for any venture to succeed",
 ["Optional and only needed for B2B","Needed only after product launch","Relevant only for large corporations"],
 "Customer-centricity is mandatory—understanding customer needs is foundational to product and venture success.",
 ["Both B2C and B2B require customer-centricity.","Customer understanding must precede and guide development.","Startups and family businesses need it equally."]),

("Application","1.2 Segmentation WHO","Demographic segmentation groups customers by measurable traits and answers the question:",
 "WHO they are",
 ["WHERE they are","WHY they buy","HOW they interact with the product"],
 "Demographic criteria—age, gender, income, occupation—identify WHO the customer is.",
 ["WHERE is geographic segmentation.","WHY is psychographic segmentation.","HOW is behavioural segmentation."]),

("Situational","1.2 Psychographic","A brand targets eco-conscious shoppers who value sustainability. Which criterion applies?",
 "Psychographic — WHY they buy",
 ["Demographic — WHO they are","Geographic — WHERE they are","Behavioural — HOW they buy only"],
 "Psychographic segmentation groups buyers by values, lifestyle, personality, and motivations.",
 ["Demographics use age/income, not inner values.","Geography uses location.","Behaviour focuses on actions; values are psychographic."]),

("Definition","1.2 Geographic","Geographic segmentation groups customers by:",
 "Physical location — WHERE they are",
 ["Age and income — WHO they are","Values and lifestyle — WHY they buy","Usage patterns — HOW they interact"],
 "Geographic segmentation uses region, climate, and urban/rural location.",
 ["Age and income are demographic.","Values are psychographic.","Usage patterns are behavioural."]),

("Application","1.4 B2B","A company selling accounting software to other companies operates as:",
 "B2B (Business-to-Business)",
 ["B2C (Business-to-Consumer)","B2G (Business-to-Government)","C2C (Consumer-to-Consumer)"],
 "B2B sells products/services to other businesses, not individual consumers.",
 ["B2C sells to end consumers.","B2G sells to government agencies.","C2C is consumer-to-consumer—not a primary segment type in the module."]),

("Situational","1.4 B2G","A construction firm bids on a city's road-repair contract. This is:",
 "B2G (Business-to-Government)",
 ["B2C","B2B commercial sales","D2C only"],
 "Selling to government agencies defines the B2G business model.",
 ["B2C targets individual consumers.","B2B is business-to-business, not government procurement.","D2C is a consumer channel, not government contracting."]),

("Definition","1.5 Buyer vs User","In the buyer vs. user model, who is the USER of Google Search?",
 "Web users who search for information",
 ["Advertisers who pay for ads","Google's engineering team","Website owners exclusively"],
 "Advertisers pay (buyers); web searchers use the service free (users).",
 ["Advertisers are buyers—they fund the platform.","Engineers build the product but aren't the user segment.","All searchers are users, not just site owners."]),

("Application","1.5 BYJU'S","For BYJU'S ed-tech, the buyer is typically the parent and the user is the student. This means:",
 "Marketing and product must address both payer and end-user needs",
 ["Only the student's opinion matters","Parents never influence purchases","B2B rules apply instead of B2C"],
 "When buyer ≠ user, convince the payer while serving the actual user's experience.",
 ["Both parties matter—payer decides, user determines engagement.","Parents are often payers and decision-makers.","BYJU'S is B2C, selling to families/consumers."]),

("Situational","1.5 Pedigree","For Pedigree dog food, the owner is the buyer and the dog is the user. The entrepreneur must understand:",
 "The owner's purchasing motivations AND the dog's consumption needs",
 ["Only veterinary regulations","Only competitor pricing","Only the dog's taste preferences"],
 "Both buyer willingness to pay and user acceptance must align for success.",
 ["Regulations matter but dual buyer-user understanding is the lesson.","Pricing alone misses the dual targeting principle.","Dog taste matters for the user, but the owner pays."]),

("Definition","1.2 Behavioural","Behavioural segmentation groups customers by:",
 "HOW they interact — usage patterns, loyalty, and purchase behavior",
 ["WHERE they live","WHO they are demographically","WHY they hold certain values"],
 "Behavioural segmentation focuses on actions: purchase frequency, brand loyalty, usage habits.",
 ["Location is geographic.","Age/gender are demographic.","Values are psychographic."]),

("Application","1.4 Sub-Segments","A shoe brand segments into Athletes, Hikers, Fashion-Conscious, and Orthopaedic Support Seekers. These are:",
 "Sub-segments within a larger B2C market",
 ["B2B customer types","Government agency segments","Macro economic forces"],
 "One B2C market (shoe buyers) contains distinct sub-segments with different needs.",
 ["These are consumer groups, not business clients.","Government segments are B2G.","Macro forces are economy-wide, not customer sub-groups."]),

("Situational","1.2 Geographic Application","A venture ships only within Metro Manila. This applies:",
 "Geographic segmentation",
 ["Psychographic segmentation only","Demographic segmentation only","Root cause analysis"],
 "Limiting service to a region is geographic segmentation—WHERE customers are.",
 ["Psychographic uses values/lifestyle.","Demographic uses age/income traits.","Root cause analysis is a problem-solving tool."]),

("Definition","1.1 Customer Segment","A customer segment is:",
 "A distinct group of potential customers with similar needs and behaviors",
 ["Any person who visits your website once","All people in a country","Only current paying customers"],
 "Like a slice of pie, a segment shares common characteristics within the broader market.",
 ["One-time visitors don't necessarily share needs.","A whole country is too broad without shared criteria.","Segments include potential customers, not just current ones."]),

("Application","1.3 Segmentation Benefits","Which is NOT a listed benefit of market segmentation?",
 "Eliminating the need for any marketing budget",
 ["Better understanding of customer needs","Personalization of product/service","Focused targeting"],
 "Segmentation improves fit and targeting—it doesn't remove marketing investment.",
 ["Understanding needs is a core benefit.","Personalization is explicitly listed.","Focused targeting allocates resources efficiently."]),

("Situational","1.7 Activity Step 1","Venture Journey Activity 2.1 Step 1 asks you to identify:",
 "Whether your primary segment is B2B, B2C, or B2G",
 ["Your company's logo design","The 5 Whys root cause","Your SDG number only"],
 "Step 1 establishes the fundamental customer type before detailing characteristics.",
 ["Logo is branding, not segment identification.","5 Whys is problem analysis.","SDGs may inspire problems but Step 1 is B2B/B2C/B2G."]),

("Definition","2.1 JTBD","Jobs to Be Done (JTBD) focuses on:",
 "The underlying task or goal the customer is trying to accomplish",
 ["The product's technical specs only","The company's org chart","Competitor pricing alone"],
 "JTBD shifts thinking from features to the job customers 'hire' a product to do.",
 ["Specs describe the product, not the customer's goal.","Org charts are internal structure.","Pricing is market analysis, not JTBD."]),

("Application","2.1 JTBD Emotional","A power drill buyer's functional job is 'make a hole.' An emotional job might be:",
 "Feel capable of fixing things myself",
 ["Maximize drill RPM specs","Analyze macro industry trends","Compare B2B vs B2C types"],
 "JTBD includes emotional jobs—how the purchase makes the customer feel.",
 ["RPM is a product spec, not an emotional job.","Macro trends are external analysis.","Segment types aren't personal emotional goals."]),

("Situational","2.1 JTBD Service","A furniture-mounting service can satisfy the same JTBD as a power drill. This shows:",
 "Customers hire products to get a job done—the solution form can vary",
 ["JTBD only applies to hardware","Emotional jobs don't matter","Functional jobs matter less than features"],
 "Different offerings can fulfill the same underlying customer job.",
 ["JTBD applies to services and software too.","Emotional/social jobs are equally important.","Functional jobs are foundational to JTBD."]),

("Definition","2.2 Customer Persona","A customer persona is:",
 "A detailed, semi-fictional representation of your ideal customer based on research and data",
 ["A fictional villain in marketing","An exact copy of one real person","A financial projection spreadsheet"],
 "Personas synthesize research into a vivid profile guiding product, marketing, and service decisions.",
 ["Personas are ideal archetypes, not antagonists.","Personas generalize patterns—they aren't 1:1 copies.","Financial projections are separate tools."]),

("Application","2.3 Persona Elements","Which set lists core elements included in a customer persona?",
 "Age, Location, Occupation, Interests, Tech-savviness, Lifestyle, JTBD, and Frustrations",
 ["Only company revenue targets and tax filings","Competitor patent numbers and stock prices","Internal employee satisfaction scores only"],
 "Personas combine demographics, lifestyle, jobs-to-be-done, and pain points into one research-based profile.",
 ["Revenue targets are business goals, not persona fields.","Patents and stock data aren't persona elements.","Employee scores are internal HR data."]),

("Situational","2.4 Rahul Pie JTBD","Rahul Pie (25, Social Media Manager, Pune) wants sneakers that:",
 "Are stylish and comfortable, building confidence and earning peer validation",
 ["Scale the company 4x in 12 months on low budget","Manage a marketing team under CEO pressure","Bid on government road-repair contracts"],
 "Rahul's JTBD blends functional needs (style, comfort) with social/emotional peer validation.",
 ["Scaling 4x is Vandana Singh's B2B challenge.","Team management is Vandana's organizational JTBD.","Government contracts are B2G, not Rahul's consumer need."]),

("Definition","2.4 B2B Persona","For B2B personas, a vital additional element compared to B2C is:",
 "Organizational role",
 ["Pet ownership status","Favorite shoe size","Social media username only"],
 "B2B personas map the customer's role—influencer, decision-maker, or end user—within their organization.",
 ["Pet ownership relates to Pedigree's buyer-user example, not B2B org mapping.","Shoe size is a B2C consumer detail.","Usernames alone don't capture organizational role."]),

("Application","2.4 Vandana Problem","Vandana Singh (Marketing Manager, AI marketing tool startup) faces the problem of:",
 "How to scale the company 4x in 12 months and become brand leader in India with a low marketing budget",
 ["Finding sneakers within budget in Pune","Training college students to invest in stocks","Bidding on city infrastructure contracts"],
 "Vandana's B2B persona centers on aggressive growth and brand leadership under budget constraints.",
 ["Sneaker budget frustration is Rahul Pie's B2C problem.","Stock training is the module's problem-statement example.","Infrastructure bidding is B2G."]),

("Situational","2.5 Different Personas","Building separate personas for Athletes and Fashion-Conscious shoe buyers follows the rule that:",
 "Different personas must be developed for different segments",
 ["One persona fits all segments","Personas replace segmentation entirely","B2G customers never need personas"],
 "Each segment has distinct needs requiring its own research-based persona.",
 ["One persona can't capture different JTBD across segments.","Personas complement segmentation—they don't replace it.","B2G can also use persona-style decision-maker profiles."]),

("Definition","1.4 Micro View","Micro analysis in the macro-micro framework examines:",
 "Finer details — individual business operations or customer behaviors",
 ["Large-scale economic trends only","Global treaties and super-macro policies","UN SDG numbering only"],
 "Micro zooms in on specific operations, customer actions, and business-level details.",
 ["Large-scale trends are macro.","Global treaties are super-macro.","SDG numbering is reference knowledge, not micro analysis."]),

("Application","1.4 Zoom OUT/IN","'Zoom OUT to identify your area of interest; Zoom IN to uncover specific problems' describes:",
 "Using both macro and micro analysis together",
 ["Using only demographic segmentation","Skipping problem validation","Focusing solely on SDGs"],
 "Zoom-out finds industries/domains; zoom-in reveals growth potential, startups, and specific challenges.",
 ["Demographics are one tool, not the zoom framework.","Validation remains essential.","SDGs are one macro map, not a substitute for zoom analysis."]),

("Situational","1.3 Family Business","A family business owner reads global trend reports to spot external risks. This applies the:",
 "Family Business career path — spot risks and find expansion/diversification opportunities",
 ["Corporate Job path — avoid all networking","Launch a Venture path — skip investors","None — family businesses don't need macro view"],
 "Macro view helps family businesses innovate, spot threats early, and diversify using global trends.",
 ["Corporate path includes networking with industry leaders.","Investor relations matters for new ventures.","Family businesses benefit significantly from macro perspective."]),

("Definition","1.1 Technical Advancements","Technical advancements as a macro factor include:",
 "Ethics for AI and questions that new technologies raise",
 ["Only traditional farming methods","Personal budgeting habits","Individual shoe size preferences"],
 "Technical macro factors cover emerging tech and the societal questions they create.",
 ["Traditional farming isn't framed as a technical advancement factor.","Personal budgeting is micro/individual.","Shoe size is a micro consumer detail."]),

("Application","1.1 Social Developments","Social developments as a macro factor are best exemplified by:",
 "Public health failures during COVID-19",
 ["A single person's morning routine","One store's inventory count","An individual's stock portfolio"],
 "Social developments are society-wide behavioral and living changes affecting many people.",
 ["Morning routines are personal/micro.","Store inventory is business micro-operation.","Individual portfolios are personal finance."]),

("Situational","1.2 Trivial Problems","A founder solving a trivial problem that barely affects anyone will likely create:",
 "A solution with minimal impact that fails to serve society or the market",
 ["Guaranteed unicorn status","Automatic SDG compliance","No need for customer segments"],
 "Without meaningful problems, solutions lack impact regardless of execution quality.",
 ["Trivial problems rarely produce high-growth ventures.","SDG alignment requires intentional selection.","Segments remain essential."]),

("Definition","1.1 Industry Trends","The lack of EV charging stations is an example of:",
 "Industry trends and challenges — shifts, gaps, or recurring problems within an industry",
 ["One customer's complaint","A personal hobby preference","A single employee review"],
 "Insufficient EV infrastructure is a sector-wide gap—a macro industry trend entrepreneurs can address.",
 ["Individual complaints are micro signals.","Hobbies are personal, not industry-wide.","Performance reviews are internal HR matters."]),

("Application","2.3 Vague Problem","'College students need to start saving and investing' is weak because it is:",
 "Vague and not specific enough about the real pain",
 ["A well-stated problem with clear pain","A proposed product solution","A root cause analysis result"],
 "It lacks specificity about who suffers, what barrier exists, and what the real pain is.",
 ["It doesn't name a specific pain or barrier.","It states a general need, not a product.","Root cause analysis traces why problems persist."]),

("Situational","2.5 Filter #3","Filter #3 asks: 'Is it one that matters to many people or companies?' This checks:",
 "The scale and significance of the problem's audience",
 ["Whether your team has a logo","Whether you used the 5 Whys","Whether the product is colorful"],
 "Problems worth solving should affect a meaningful number of people or organizations.",
 ["Logo design is branding.","5 Whys is root cause analysis.","Aesthetics don't determine problem significance."]),

("Definition","2.7 Customer Empathy","Customer empathy as a problem-analysis benefit means:",
 "Stepping into the shoes of your customers",
 ["Copying competitors exactly","Ignoring user feedback","Prioritizing founder ego over users"],
 "Empathy guides innovators to deeply understand customer experiences, pains, and motivations.",
 ["Copying isn't empathy.","Ignoring feedback contradicts customer-centricity.","Prioritizing ego opposes Impact over Ego."]),

("Application","2.8 Root Causes","Problem analysis asking 'What are the Root Causes?' supports:",
 "Solving problems at their source rather than treating symptoms",
 ["Choosing a company name","Setting office furniture layout","Selecting brand colors only"],
 "Root cause identification prevents recurring problems that surface fixes can't resolve.",
 ["Naming is branding.","Office layout is operational.","Brand colors are design, not causal analysis."]),

("Situational","2.5 Filter #5 Saturation","Fifty identical apps already solve your chosen problem. Filter #5 suggests:",
 "There may not be real demand—consider a different problem",
 ["Launch immediately anyway","Skip all customer validation","Ignore segmentation entirely"],
 "Oversaturated spaces often lack demand for yet another identical solution.",
 ["Saturation reduces differentiation opportunity.","Validation becomes more critical in crowded markets.","Segmentation may help find niches but doesn't override demand concerns."]),

("Definition","2.5 Filter #1","The 5-point filter's first question asks:",
 "Is it a relevant problem (not one that's already 'dying')?",
 ["Is it the cheapest to solve?","Does it require zero research?","Is it only interesting to the founder?"],
 "Relevance ensures the problem still exists and isn't fading from importance.",
 ["Cost isn't a filter criterion.","Research is essential.","Founder-only interest fails filters #3 and #4."]),

("Application","2.2 Generate Ideas","After validating a problem, the next step in the idea-finding process is to:",
 "Generate ideas that match your passion and offer delightful solutions",
 ["Skip directly to IPO planning","Abandon the validated problem","Incorporate the company immediately"],
 "The flow is: Curious → Identify → Validate → Generate Ideas → then validate Solution and Business Model.",
 ["IPO is a late-stage outcome.","Validated problems should be pursued.","Incorporation follows solution and business model validation."]),

("Situational","1.5 Samsung B2B","A Samsung CFO buys 1,000 A/C gas-filling machines for service engineers. This shows:",
 "In B2B, the buyer (CFO) and user (engineer) can be different organizational roles",
 ["B2B never separates buyers and users","Only B2C has buyer-user distinction","Government is always the B2B buyer"],
 "B2B purchases often involve financial approvers (buyers) and operational staff (users).",
 ["B2B frequently separates economic buyer from end user.","Buyer-user distinction applies to both B2C and B2B.","Government buyers indicate B2G."]),

("Definition","1.1 Segment Noun","Segment (noun) in market segmentation means:",
 "A part or section distinct or separate from the whole — like a slice of pie",
 ["The entire global population as one group","A company's internal department","A root cause analysis method"],
 "A segment is a distinct portion of the broader market sharing common traits.",
 ["Whole populations without criteria aren't segments.","Departments are org structure.","Root cause analysis is problem-solving."]),

("Application","1.3 Customized Communication","Customized communication is a segmentation benefit because:",
 "Different segments respond to different messaging",
 ["All customers prefer identical ads","Segmentation eliminates messaging","One message works globally"],
 "Segment-specific messaging improves relevance, engagement, and conversion.",
 ["Customers have diverse motivations.","Segmentation enhances messaging—it doesn't remove it.","One-size-fits-all messaging underperforms."]),

("Situational","1.2 Combined Segmentation","An eco-conscious shopper who always buys the same sustainable brand demonstrates:",
 "Psychographic values AND behavioural brand loyalty",
 ["Geographic and demographic criteria only","B2G and B2B market types","Macro and micro analysis only"],
 "Values-driven buying is psychographic; repeat same-brand purchasing is behavioural.",
 ["Location/age alone don't capture values and loyalty.","B2G/B2B are market types, not this behavior pattern.","Macro/micro are analysis levels."]),

("Definition","1.4 B2C","B2C (Business-to-Consumer) means:",
 "A company sells products/services directly to individual consumers",
 ["Businesses sell only to other businesses","Companies sell only to government","Consumers sell to businesses exclusively"],
 "B2C targets end consumers—shoppers, students, families—directly.",
 ["Business-to-business is B2B.","Business-to-government is B2G.","Consumer-to-business isn't the B2C definition."]),

("Application","1.3 Product Fit","Better product fit is a segmentation benefit because:",
 "Understanding segment needs lets you tailor the product to match",
 ["All segments want identical features","Segmentation guarantees zero product changes","Product fit is unrelated to segments"],
 "Segment insights drive feature prioritization and design for specific groups.",
 ["Different segments have different needs.","Products typically require per-segment tailoring.","Product fit is directly tied to segment understanding."]),

("Situational","1.7 Activity Step 2","Venture Activity 2.1 Step 2 — Segment Characteristics — requires:",
 "Identifying broad traits common to people in the primary segment",
 ["Designing your company logo","Running the 5 Whys on your product","Listing all 17 SDGs"],
 "Step 2 captures shared demographic, geographic, psychographic, or behavioural traits.",
 ["Logo is branding.","5 Whys is root cause analysis.","SDGs may inspire problems but aren't Step 2."]),

("Definition","2.1 Functional Jobs","In JTBD, functional jobs refer to:",
 "The practical task the customer needs accomplished",
 ["How the product makes them feel only","How others perceive them only","The company's profit margin"],
 "Functional jobs are tangible outcomes—making a hole, completing a task, reaching a destination.",
 ["Feelings are emotional/social jobs.","Social perception is emotional/social.","Profit margin is a business metric."]),

("Application","2.1 Emotional/Social Jobs","JTBD requires equal importance for functional jobs and:",
 "Emotional/social jobs",
 ["Only competitor analysis","Only technical specifications","Only financial auditing"],
 "Customers hire products for practical tasks AND for how those products make them feel or look to others.",
 ["Competitor analysis supports strategy but isn't a job type.","Specs alone miss emotional/social dimensions.","Financial auditing is internal."]),

("Situational","2.4 Vandana Frustrations","Vandana Singh's scaling challenge on a low budget belongs in her persona under:",
 "Problems / Frustrations",
 ["SDG numbering charts","Macro industry trend tables only","The 5 Whys symptom tree only"],
 "Personas explicitly document frustrations and problems the ideal customer faces.",
 ["SDG charts map global goals.","Macro trends are external context.","5 Whys analyzes causes; personas document frustrations."]),

("Definition","2.2 Persona Purpose","Personas help businesses with all EXCEPT:",
 "Eliminating the need to ever talk to real customers",
 ["Marketing strategy guidance","Product development decisions","Customer service strategies"],
 "Personas are research-based guides—they never replace ongoing real customer interaction.",
 ["Personas guide marketing messaging.","Personas inform feature priorities.","Personas tailor customer service."]),

("Application","2.3 Tech-savviness","Tech-savviness as a persona element helps decide:",
 "Which digital channels and UX complexity to use",
 ["Which SDG number to memorize","How many 5 Whys iterations to run","Whether macro view is optional"],
 "Tech-savviness shapes app design, platform choice, and support models.",
 ["SDG selection relates to problem areas.","5 Whys count isn't persona-driven.","Macro view is never optional for strategy."]),

("Situational","1.2 Brand Loyalty","A frequent buyer who always chooses the same brand out of loyalty uses:",
 "Behavioural segmentation",
 ["Demographic criteria only","Geographic criteria only","B2G criteria"],
 "Purchase behavior and brand loyalty are core behavioural variables.",
 ["Demographics use age/income.","Geography uses location.","B2G is a market type, not a criterion."]),

("Definition","Cheat Sheet 5 Whys","The Quick-Recap cheat sheet defines the 5 Whys as:",
 "Ask 'why' repeatedly (~5 times) to trace a symptom back to its root cause",
 ["Ask 'what' repeatedly to list product features","Ask 'who' once to identify competitors","Ask 'how much' to set pricing"],
 "5 Whys digs beneath surface symptoms to find the underlying root cause.",
 ["Feature listing isn't 5 Whys.","Competitor ID isn't the 5 Whys method.","Pricing questions aren't root cause analysis."]),

("Application","1.3 Launch Venture","Using macro view to launch a venture helps founders:",
 "Spot unmet needs, make strategic decisions, and attract investors by showing trend alignment",
 ["Ignore industry trends deliberately","Avoid all investor communication","Focus only on office interior design"],
 "Macro analysis identifies gaps, informs strategy, and demonstrates market fit to investors.",
 ["Ignoring trends contradicts macro perspective.","Investor communication is enhanced by macro insight.","Office design is operational detail."]),

("Situational","1.3 Corporate Job","Corporate professionals use macro view to network with industry leaders for:",
 "Insight and job connections in growing industries",
 ["Avoiding all skill development","Ignoring growth outlook data","Focusing only on declining sectors"],
 "Macro perspective plus networking helps identify growing fields and build relevant career connections.",
 ["Macro view supports skill preparation.","Growth outlook is a key macro reflection topic.","Declining sectors offer fewer opportunities."]),

("Definition","1.6 Passion Area","Passion area in Lesson 1 reflections refers to:",
 "Areas you are passionate about and gaps you could work on",
 ["Your company's tax filing schedule","Competitor employee headcount","Office supply inventory"],
 "Passion areas connect personal motivation to observable industry gaps worth pursuing.",
 ["Tax schedules are administrative.","Headcount is market intel, not passion mapping.","Inventory is operational."]),

("Application","1.6 Startups & Innovations","The Startups & Innovations reflection topic helps you understand:",
 "The needs startups are solving and innovations being made in your industry",
 ["Internal HR vacation policies only","Social media follower counts","Historical bankruptcy records exclusively"],
 "Tracking startup activity reveals where innovation happens and which problems are being tackled.",
 ["HR policies are internal operations.","Follower counts are vanity metrics.","Bankruptcy records aren't the focus of this reflection."]),

("Situational","2.9 Symptom vs Root","In the lateness 5 Whys example, being late for class is:",
 "A symptom (the tree's leaves), not the root cause",
 ["The root cause itself","A macro industry trend","Unrelated to the problem chain"],
 "Surface complaints are symptoms; root causes lie deeper—like poor schedule discipline.",
 ["Root cause was poor discipline/lack of schedule.","Personal lateness is micro-level, not industry macro.","Lateness starts the problem chain as the visible symptom."]),

("Definition","1.6 Growth Outlook","Growth outlook in macro reflections refers to:",
 "How an industry is expected to perform in the future",
 ["A company's past quarterly revenue only","One customer's satisfaction score","An employee's daily schedule"],
 "Growth outlook projects future industry trajectory—expansion, contraction, or transformation.",
 ["Past revenue is company history, not industry outlook.","Individual satisfaction is micro feedback.","Personal schedules aren't industry forecasts."]),

("Application","1.5 SDG Gender/Inequality","Gender Equality and Reduced Inequalities correspond to SDGs:",
 "SDG 5 and SDG 10 respectively",
 ["SDG 1 and SDG 2","SDG 14 and SDG 15","SDG 8 and SDG 9"],
 "SDG 5 is Gender Equality; SDG 10 is Reduced Inequalities—both among the 17 UN goals.",
 ["SDG 1 is No Poverty; SDG 2 is Zero Hunger.","SDG 14 is Life Below Water; SDG 15 is Life on Land.","SDG 8 is Decent Work; SDG 9 is Industry & Innovation."]),

("Situational","2.4 Problem ID Steps","Your team wrote a problem statement before listing pain points. The skipped step was:",
 "Make a list of problems/pain points/unresolved needs",
 ["Choose the problem your team wants to address","Create a concise problem statement","Identify gaps in the industry"],
 "Listing pain points precedes choosing one problem and writing the final statement.",
 ["Choosing comes after listing options.","Statement creation is the last step.","Gap identification is an earlier foundational step."]),

("Definition","2.1 Stay Curious","Being curious in the idea-finding process means:",
 "Observe the world and discover your passion",
 ["Copy the first startup you see","Skip observation and guess","Avoid asking any questions"],
 "Curiosity drives observation of problems—the starting point for opportunity discovery.",
 ["Copying skips validation.","Observation is essential—guessing skips research.","Asking 'Why not?' and challenging assumptions is encouraged."]),

("Application","1.5 SDG Health/Education","Good Health and Well-being and Quality Education are:",
 "SDG 3 and SDG 4 respectively",
 ["SDG 8 and SDG 9","SDG 16 and SDG 17","SDG 11 and SDG 12"],
 "SDG 3 promotes good health; SDG 4 promotes quality education—key macro problem areas.",
 ["SDG 8 is Decent Work; SDG 9 is Industry & Innovation.","SDG 16 is Peace & Justice; SDG 17 is Partnerships.","SDG 11 is Sustainable Cities; SDG 12 is Responsible Consumption."]),

("Situational","1.4 B2C Example","A shoe brand selling sneakers directly to shoppers operates as:",
 "B2C",
 ["B2B","B2G","Non-commercial"],
 "Direct sales to individual consumers define B2C.",
 ["B2B sells to other businesses.","B2G sells to government.","This is a commercial consumer sale."]),

("Definition","1.5 Google Buyer","The BUYER in Google's search advertising model is:",
 "Advertisers who pay for ad placements",
 ["Web users who search for free","Google's software developers","Internet service providers"],
 "Advertisers pay (buyers); searchers use the product free (users).",
 ["Web users are users, not payers.","Developers build the platform.","ISPs provide connectivity—they aren't ad buyers."]),

("Application","1.7 Activity Step 3","Venture Activity 2.1 Step 3 — Secondary Segments — asks you to identify:",
 "Up to 3 secondary customer segments beyond the primary",
 ["Only government agencies","Zero segments because segmentation is optional","Only one segment total"],
 "After the primary segment, up to three secondary segments broaden market understanding.",
 ["Secondaries can be B2B, B2C, or B2G—not only government.","Segmentation is required, not optional.","One segment ignores secondary opportunities."]),

("Situational","2.4 B2B Org Role","'Organizational role' as a persona element is vital when targeting:",
 "B2B customers and influencers",
 ["Wild animals as end users only","Anonymous web traffic only","Internal accounting ledgers"],
 "B2B personas map roles—CFO buyer, engineer user, marketing manager influencer.",
 ["Animals can be users (Pedigree) but org role is a B2B human factor.","Web traffic is analytics, not persona mapping.","Ledgers are financial records."]),

("Definition","2.3 Lifestyle","Lifestyle as a persona element captures:",
 "How the customer lives, spends time, and what they value day-to-day",
 ["The company's manufacturing process","Competitor stock price history","Government tax code sections"],
 "Lifestyle covers activities, interests, social habits, and daily patterns.",
 ["Manufacturing is internal operations.","Stock prices are market data.","Tax codes are legal/regulatory."]),

("Application","2.4 Rahul Channels","Rahul Pie being active on Instagram and fashion forums informs:",
 "Marketing channel selection and community engagement strategy",
 ["B2G procurement rules","5 Whys iteration count","Global treaty drafting"],
 "Knowing where Rahul spends time online guides social and community-based marketing.",
 ["B2G is government contracting.","5 Whys is root cause methodology.","Treaties are super-macro policy."]),

("Situational","2.5 Filter #2","Filter #2 'Is it one your team feels passionate about?' ensures:",
 "Team motivation to persist through the venture journey",
 ["The problem requires zero effort","Passion replaces customer validation","Only financial metrics matter"],
 "Passion sustains founders through challenges—it's one of five problem-worthiness filters.",
 ["Worthy problems still require significant effort.","Passion complements but never replaces validation.","Financial metrics matter but passion drives commitment."]),

("Definition","2.1 Idea vs Problem","The Idea vs. Problem distinction teaches startups to begin with:",
 "A real-world problem, not just an idea or product concept",
 ["A logo design concept","An office lease agreement","A social media hashtag"],
 "The right starting point is a validated problem—not branding or tactics.",
 ["Logo comes after problem-solution fit.","Office lease is operational.","Hashtags are marketing tactics."]),

("Application","1.4 Climate Micro","Personal/local micro responses to climate change include:",
 "Avoiding single-use plastic, using energy-efficient appliances, and biking instead of driving",
 ["The Paris Agreement and global treaties","Wind and solar farms at industry scale","Global research and advocacy programs"],
 "Micro actions are individual/local habits—plastic reduction, efficient appliances, biking.",
 ["Paris Agreement is super-macro/global.","Wind/solar farms are macro/industry scale.","Global advocacy is super-macro."]),

("Situational","2.6 Solution Attachment","Founders overly attached to a specific solution should shift toward:",
 "Loving the problem and staying flexible on how to solve it",
 ["Permanently keeping the first prototype unchanged","Avoiding all customer contact","Skipping the 5-point filter"],
 "Problem-first thinking keeps solution options open until the problem is deeply validated.",
 ["Permanent prototype attachment is what the lesson warns against.","Customer contact is essential.","All five filters should be applied."]),

("Definition","1.3 Focused Targeting","Focused targeting as a segmentation benefit means:",
 "Concentrating resources on the most relevant customer groups",
 ["Marketing to everyone with no priorities","Avoiding all communication","Serving every segment identically"],
 "Focused targeting allocates limited startup resources to highest-potential segments.",
 ["Marketing to everyone dilutes resources.","Communication is essential—targeting refines it.","Startups must choose focus, especially early on."]),

("Application","2.4 Vandana Values","Vandana Singh values creativity, innovation, and sustainability. These are:",
 "Psychographic/lifestyle traits in her persona",
 ["Geographic location data only","B2G procurement criteria","5 Whys answers"],
 "Values and aspirations are psychographic elements shaping her JTBD and decisions.",
 ["Her location (Gurugram) is geographic.","Procurement applies to government sales.","5 Whys traces root causes, not persona values."]),

("Situational","2.5 Filter #4","'Is it highly painful or highly desirable to solve?' corresponds to filter:",
 "#4 — the pain/desirability test",
 ["#1 — relevance test","#2 — passion test","#5 — saturation test"],
 "Filter #4 assesses whether the problem causes enough pain or desire to motivate solution-seeking.",
 ["#1 checks if the problem is still relevant.","#2 checks team passion.","#5 checks market oversaturation."]),

("Definition","1.4 Super Macro","The Paris Agreement and global financial support to developing nations represent:",
 "Super-macro / global-level climate action",
 ["Micro personal habit changes","Individual store inventory management","Single customer persona profiling"],
 "International treaties and global programs operate at the super-macro level—above industry macro.",
 ["Personal habits are micro.","Inventory is micro business operation.","Personas profile individual customers."]),

("Application","2.2 Process Flow","After generating ideas, the process leads to validating the:",
 "Solution, Business Model, and related venture elements",
 ["Company logo color only","Office parking layout","Social media username"],
 "The full flow: Curious → Identify → Validate Problem → Generate Ideas → Validate Solution & Business Model.",
 ["Logo color is branding detail.","Parking is operational trivia.","Usernames are marketing details."]),

("Situational","2.1 Observe Problems","Startup ideas come from observing problems through:",
 "Staying curious, observing, and asking 'Why not?'",
 ["Copying competitors without thinking","Skipping all market research","Avoiding critical questions"],
 "Observation, curiosity, and challenging assumptions ('Why not?') reveal real opportunities.",
 ["Blind copying skips problem understanding.","Research and observation are essential.","Critical questioning is explicitly encouraged."]),

("Definition","1.5 SDG Work/Innovation","Decent Work and Economic Growth and Industry, Innovation and Infrastructure are:",
 "SDG 8 and SDG 9 respectively",
 ["SDG 1 and SDG 2","SDG 16 and SDG 17 only","SDG 3 and SDG 4 only"],
 "SDG 8 promotes decent work; SDG 9 focuses on industry, innovation, and infrastructure.",
 ["SDG 1 is No Poverty; SDG 2 is Zero Hunger.","SDG 16 is Peace & Justice; SDG 17 is Partnerships.","SDG 3 is Good Health; SDG 4 is Quality Education."]),

("Application","1.3 Family Business Innovation","Family businesses use macro view to bring:",
 "Fresh, innovative ideas from global trends",
 ["Zero external awareness of risks","Complete avoidance of diversification","Only traditional methods forever"],
 "Macro perspective injects innovation and helps family businesses spot risks and diversify.",
 ["Macro view specifically helps spot external risks.","Diversification is a stated family business benefit.","Global trends inspire fresh ideas, not stagnation."]),

("Situational","2.8 Personal Connection","Problem analysis asking about your personal connection to the problem helps:",
 "Build genuine motivation and authentic understanding of the pain",
 ["Skip customer empathy entirely","Avoid all validation steps","Replace the need for segmentation"],
 "Personal connection fuels passion and deeper empathy—but still requires customer validation.",
 ["Personal connection complements empathy.","Validation remains necessary.","Segmentation is still required."]),

("Definition","1.5 SDG Poverty/Hunger","No Poverty and Zero Hunger are:",
 "SDG 1 and SDG 2 respectively",
 ["SDG 10 and SDG 11","SDG 14 and SDG 15","SDG 8 and SDG 9"],
 "SDG 1 is No Poverty; SDG 2 is Zero Hunger—the first two UN Sustainable Development Goals.",
 ["SDG 10 is Reduced Inequalities; SDG 11 is Sustainable Cities.","SDG 14 is Life Below Water; SDG 15 is Life on Land.","SDG 8 is Decent Work; SDG 9 is Industry & Innovation."]),

("Application","1.5 SDG Cities/Consumption","Sustainable Cities and Communities and Responsible Consumption and Production are:",
 "SDG 11 and SDG 12 respectively",
 ["SDG 3 and SDG 4","SDG 5 and SDG 6","SDG 1 and SDG 2"],
 "SDG 11 addresses sustainable cities; SDG 12 addresses responsible consumption—macro urban and consumption challenges.",
 ["SDG 3 is Good Health; SDG 4 is Quality Education.","SDG 5 is Gender Equality; SDG 6 is Clean Water.","SDG 1 is No Poverty; SDG 2 is Zero Hunger."]),

("Situational","1.5 CFO Buyer","A CFO approving budget for machines used by service engineers is the:",
 "Buyer — the one who pays or approves the purchase",
 ["User who operates the machines","Secondary segment label only","Fictional persona with no real role"],
 "The CFO pays/approves (buyer); engineers operate the machines (users).",
 ["Engineers are users.","CFO represents buyer role, not a segment label.","CFO is a real B2B organizational role."]),

("Definition","1.5 SDG Environment","Life Below Water and Life on Land are:",
 "SDG 14 and SDG 15 respectively",
 ["SDG 8 and SDG 9","SDG 3 and SDG 4","SDG 1 and SDG 2"],
 "SDG 14 protects marine ecosystems; SDG 15 protects terrestrial ecosystems.",
 ["SDG 8 is Decent Work; SDG 9 is Industry & Innovation.","SDG 3 is Good Health; SDG 4 is Quality Education.","SDG 1 is No Poverty; SDG 2 is Zero Hunger."]),

("Application","1.5 SDG Governance","Peace, Justice and Strong Institutions and Partnerships for the Goals are:",
 "SDG 16 and SDG 17 respectively",
 ["SDG 5 and SDG 6","SDG 11 and SDG 12","SDG 13 and SDG 14"],
 "SDG 16 promotes peace and strong institutions; SDG 17 promotes global partnerships—the final SDGs.",
 ["SDG 5 is Gender Equality; SDG 6 is Clean Water.","SDG 11 is Sustainable Cities; SDG 12 is Responsible Consumption.","SDG 13 is Climate Action; SDG 14 is Life Below Water."]),

("Situational","2.4 Rahul Frustration","Rahul Pie's core frustration is struggling to find sneakers that:",
 "Meet fashion and comfort needs within budget, leading to unsatisfactory purchases",
 ["Scale a company 4x in 12 months","Manage CFO-approved equipment orders","Win government infrastructure bids"],
 "Rahul can't find sneakers balancing style, comfort, and affordability—a key persona frustration.",
 ["Scaling 4x is Vandana's B2B challenge.","CFO equipment orders are Samsung's B2B example.","Infrastructure bids are B2G."]),

("Definition","2.4 Vandana JTBD","Vandana Singh's B2B JTBD includes wanting:",
 "Campaigns that resonate, brand loyalty, less team stress, and respect from the CEO/Board",
 ["Stylish sneakers for peer validation","Dog food the owner and pet both accept","Free web search results"],
 "Vandana's organizational JTBD covers marketing impact, loyalty, team management, and executive respect.",
 ["Sneaker validation is Rahul's B2C JTBD.","Dog food is the Pedigree buyer-user example.","Free search describes Google's user experience."]),

("Application","1.4 Climate Super Macro","Global research and advocacy on climate change represents:",
 "Super-macro action — alongside treaties like the Paris Agreement",
 ["Micro personal recycling only","Single-store inventory management","One customer's persona element"],
 "Global research, advocacy, and financial support operate at the super-macro level above industry.",
 ["Personal recycling is micro.","Inventory is business micro-operation.","Personas profile individuals, not global programs."]),

("Situational","1.6 Reflection Macro Industry","The 'Macro Industry' reflection topic helps you understand:",
 "Why a macro view matters for a larger perspective of industries",
 ["How to design a company logo","Which font to use in pitch decks","Office furniture arrangement"],
 "Macro Industry reflection builds appreciation for zooming out to see industry-wide patterns and opportunities.",
 ["Logo design is branding.","Fonts are presentation details.","Furniture is operational."]),

("Definition","1.6 Reflection Market Segmentation","The 'Market Segmentation' reflection topic covers:",
 "Dividing a broad market into sub-groups based on shared characteristics",
 ["Running the 5 Whys on lateness","Writing a business incorporation document","Choosing SDG colors"],
 "Segmentation divides markets into focused sub-groups for clarity and targeted strategy.",
 ["5 Whys is root cause analysis.","Incorporation is legal setup.","SDG colors aren't a reflection topic."]),

("Application","1.6 Reflection Buyer/User","The 'Differentiating Buyers & Users' reflection emphasizes:",
 "Why telling buyer and user apart matters for targeting and who actually faces the problem",
 ["Why logos must be blue","Why offices need parking","Why SDGs have 17 items"],
 "Buyer-user distinction shapes targeting, messaging, and understanding who experiences the pain.",
 ["Logo color is branding preference.","Parking is operational.","SDG count is factual, not the reflection focus."]),

("Situational","2.3 Trend vs Problem","'New-age investment apps are bringing younger investors into the market' is:",
 "A trend observation, not a well-stated problem",
 ["A well-stated problem with named pain","A root cause analysis finding","A complete customer persona"],
 "Trends describe market movement—they don't specify who hurts and how.",
 ["Well-stated problems name affected people and specific pain.","Root causes explain why problems persist.","Personas are customer profiles."]),

("Definition","Cheat Sheet Macro View","The Quick-Recap defines Macro View as:",
 "Large-scale trends and factors affecting whole industries or economies",
 ["Individual customer shoe preferences","One employee's daily schedule","A single store's inventory count"],
 "Macro view = broad external forces shaping entire industries or economies.",
 ["Shoe preferences are micro consumer details.","Schedules are personal micro matters.","Inventory is micro business operation."]),

("Application","Cheat Sheet JTBD","The Quick-Recap defines JTBD as:",
 "The underlying functional plus emotional/social job a customer hires a product to do",
 ["A company's internal profit margin target","A competitor's patent filing","An SDG numbering system"],
 "JTBD captures both practical tasks and emotional/social outcomes customers seek.",
 ["Profit margin is a business metric.","Patents are legal/competitive data.","SDG numbering is reference knowledge."]),

("Situational","2.5 All Filters","A validated problem affects many people, your team is passionate, but 50 identical apps exist. Best action:",
 "Reconsider—Filter #5 signals insufficient real demand despite other strengths",
 ["Launch without any differentiation","Ignore all five filters","Skip all customer interviews"],
 "Saturation with identical solutions suggests weak demand—passion and scale alone aren't enough.",
 ["Differentiation may help but saturation warrants caution.","All five filters matter collectively.","Interviews become more important in saturated markets."]),

("Definition","Cheat Sheet Buyer vs User","The Quick-Recap states Buyer vs. User means:",
 "The one who pays is not always the one who uses the product",
 ["Buyer and user are always the same person","Only government can be the buyer","Users always pay for the product"],
 "Pedigree, BYJU'S, Samsung, and Google Search all illustrate payer ≠ user.",
 ["Many examples show buyer and user differ.","Government buyers indicate B2G specifically.","Google Search users don't pay—advertisers do."]),

("Application","1.5 SDG Climate/Energy","Climate Action and Affordable and Clean Energy are:",
 "SDG 13 and SDG 7 respectively",
 ["SDG 1 and SDG 2","SDG 5 and SDG 6","SDG 16 and SDG 17"],
 "SDG 13 addresses climate action; SDG 7 addresses clean energy—both macro sustainability areas.",
 ["SDG 1 is No Poverty; SDG 2 is Zero Hunger.","SDG 5 is Gender Equality; SDG 6 is Clean Water.","SDG 16 is Peace & Justice; SDG 17 is Partnerships."]),

("Situational","2.6 Reflection Persona B2B","The 'Persona for B2B' reflection topic highlights that B2B personas:",
 "Add Organizational Role and write JTBD from the organization's perspective",
 ["Never include frustrations or problems","Are identical to B2C personas in every field","Replace the need for any segmentation"],
 "B2B personas require org role mapping and organization-level jobs-to-be-done.",
 ["Frustrations are included in all personas.","B2B adds org role—B2C doesn't require it.","Personas complement segmentation."]),

("Definition","2.5 Create Persona","The 'Create Customer Persona' reflection teaches you to:",
 "Build a persona for your chosen segment based on the problem your team chose to solve",
 ["Skip segment identification entirely","Copy a competitor's persona exactly","Avoid any research or data"],
 "Personas are built for your specific segment and problem context using research.",
 ["Segment identification precedes persona creation.","Personas should be research-based, not copied blindly.","Research and data are foundational to personas."]),

("Application","2.2 Validate Then Build","A founder who validates WHO faces the problem and its urgency BEFORE building avoids:",
 "Creating products nobody urgently needs",
 ["Needing customer segments ever","Using macro analysis ever","Building any personas"],
 "Problem validation ensures real demand before investing in solution development.",
 ["Segments target validated customers.","Macro view informs which problems to explore.","Personas translate segments into actionable profiles."]),

("Situational","1.3 Launch Venture Investors","Launching a venture with macro view helps attract investors by:",
 "Showing how the business fits larger industry and societal trends",
 ["Hiding all trend data from investors","Avoiding any strategic decisions","Presenting only micro-level data"],
 "Investors want evidence that your venture aligns with meaningful macro trends and market gaps.",
 ["Hiding trends reduces investor confidence.","Strategic decisions should be trend-informed.","Macro alignment complements micro execution details."]),
]

assert len(RAW) >= 100, f"Need at least 100 questions, got {len(RAW)}"
assert len(KEYS) >= len(RAW), "KEYS must cover all questions"
KEYS = KEYS[:len(RAW)]

questions = []
for i, (qtype, topic, qtext, correct, wrongs, exp_c, exp_ws) in enumerate(RAW):
    target = KEYS[i]
    options = [{"text": correct, "explain": exp_c, "correct": True}]
    for j, w in enumerate(wrongs):
        options.append({"text": w, "explain": exp_ws[j], "correct": False})
    random.shuffle(options)
    ci = next(k for k, o in enumerate(options) if o["correct"])
    if ci != target:
        options[ci], options[target] = options[target], options[ci]
    questions.append({
        "id": i + 1,
        "type": qtype,
        "topic": topic,
        "question": qtext,
        "choices": [o["text"] for o in options],
        "correct": target,
        "explanations": {str(k): o["explain"] for k, o in enumerate(options)},
    })

topics = [t for _, t, *_ in RAW]
TOTAL = len(questions)
print("Questions:", TOTAL)
print("Unique topics:", len(set(topics)))

REQUIRED_TOPICS = [
 "1.1 Macro View","1.1 Economic Forces","1.1 Industry Trends","1.1 Social Developments","1.1 Technical Advancements",
 "1.2 Why Macro View","1.2 Trivial Problems","1.3 Launch Venture","1.3 Corporate Job","1.3 Family Business",
 "1.3 Family Business Innovation","1.3 Launch Venture Investors",
 "1.4 Genius of the AND","1.4 Micro View","1.4 Zoom OUT/IN","1.4 Climate Macro","1.4 Climate Micro","1.4 Climate Super Macro","1.4 Super Macro",
 "1.5 SDGs","1.5 SDG Clean Water","1.5 SDG Gender/Inequality","1.5 SDG Health/Education","1.5 SDG Work/Innovation",
 "1.5 SDG Poverty/Hunger","1.5 SDG Cities/Consumption","1.5 SDG Environment","1.5 SDG Governance","1.5 SDG Climate/Energy",
 "1.6 Passion Area","1.6 Growth Outlook","1.6 Startups & Innovations","1.6 Reflection Macro Industry",
 "1.6 Reflection Market Segmentation","1.6 Reflection Buyer/User",
 "2.1 Uri Levine","2.1 Stay Curious","2.1 Observe Problems","2.1 Idea vs Problem","2.2 Validate Problems","2.2 Generate Ideas","2.2 Process Flow","2.2 Validate Then Build",
 "2.3 Well-Stated Problem","2.3 Vague Problem","2.3 Trend vs Problem","2.4 Problem ID Steps",
 "2.5 Filter #1","2.5 Filter #2","2.5 Filter #3","2.5 Filter #4","2.5 Filter #5","2.5 All Filters",
 "2.6 Fall in Love","2.6 Solution Attachment","2.7 Open-mindedness","2.7 Customer Empathy","2.7 Impact over Ego",
 "2.8 Root Causes","2.8 Personal Connection","2.9 5 Whys","2.9 5 Whys Example","2.9 Symptom vs Root",
 "M2 Intro Customer Centricity","1.1 Customer Segment","1.1 Segment Noun","1.2 Segmentation WHO","1.2 Psychographic","1.2 Geographic","1.2 Behavioural","1.2 Geographic Application","1.2 Combined Segmentation","1.2 Brand Loyalty",
 "1.3 Segmentation Benefits","1.3 Customized Communication","1.3 Product Fit","1.3 Focused Targeting",
 "1.4 B2B","1.4 B2C","1.4 B2G","1.4 B2C Example","1.4 Sub-Segments",
 "1.5 Buyer vs User","1.5 BYJU'S","1.5 Pedigree","1.5 Google Buyer","1.5 Samsung B2B","1.5 CFO Buyer",
 "1.7 Activity Step 1","1.7 Activity Step 2","1.7 Activity Step 3",
 "2.1 JTBD","2.1 Functional Jobs","2.1 Emotional/Social Jobs","2.1 JTBD Emotional","2.1 JTBD Service",
 "2.2 Customer Persona","2.2 Persona Purpose","2.3 Persona Elements","2.3 Lifestyle","2.3 Tech-savviness",
 "2.4 Rahul Pie JTBD","2.4 Rahul Frustration","2.4 Rahul Channels","2.4 Vandana Problem","2.4 Vandana JTBD","2.4 Vandana Frustrations","2.4 Vandana Values",
 "2.4 B2B Persona","2.4 B2B Org Role","2.5 Different Personas","2.5 Create Persona","2.6 Reflection Persona B2B",
 "Cheat Sheet Macro View","Cheat Sheet 5 Whys","Cheat Sheet JTBD","Cheat Sheet Buyer vs User",
]
missing = [r for r in REQUIRED_TOPICS if r not in set(topics)]
if missing:
    print("MISSING TOPICS:", missing)
else:
    print("All required topics covered!")

q_json = json.dumps(questions, ensure_ascii=False)

HTML = open("Quizzer.html", encoding="utf-8").read()
HTML = re.sub(r'const TOTAL=\d+;\n', '', HTML)
HTML = re.sub(r'const QUESTIONS = \[.*?\];', f'const TOTAL={TOTAL};\nconst QUESTIONS = {q_json};', HTML, count=1, flags=re.DOTALL)

# Update count references in HTML and JS
HTML = re.sub(r"1/100", f"1/{TOTAL}", HTML)
HTML = re.sub(r"(?<!\d)/100(?!\d)", f"/{TOTAL}", HTML)
HTML = re.sub(r"100 Questions", f"{TOTAL} Questions", HTML)
HTML = re.sub(r"100 interactive", f"{TOTAL} interactive", HTML)
HTML = re.sub(r"100-item", f"{TOTAL}-item", HTML)
HTML = re.sub(r"cur===99", f"cur==={TOTAL-1}", HTML)
HTML = re.sub(r"cur<99", f"cur<{TOTAL-1}", HTML)
HTML = re.sub(r"\(cur\+1\)/100\*100", f"(cur+1)/TOTAL*100", HTML)
HTML = re.sub(r"\+'/100'", f"+'/'+TOTAL", HTML)
HTML = re.sub(r"score\}/100", f"score}}/{TOTAL}", HTML)
HTML = re.sub(r"'/ 100'", f"'/ {TOTAL}'", HTML)
HTML = re.sub(r"100/100", f"{TOTAL}/{TOTAL}", HTML)
HTML = re.sub(r"pct=score", "pct=Math.round(score/TOTAL*100)", HTML)
HTML = re.sub(r"document\.getElementById\('counter'\)\.textContent=\(cur\+1\)\+'/100'",
              "document.getElementById('counter').textContent=(cur+1)+'/'+TOTAL", HTML)
HTML = re.sub(r"document\.getElementById\('progress-fill'\)\.style\.width=\(\(cur\+1\)/100\*100\)",
              "document.getElementById('progress-fill').style.width=((cur+1)/TOTAL*100)", HTML)
HTML = re.sub(r"document\.getElementById\('btn-next'\)\.textContent=cur===99",
              f"document.getElementById('btn-next').textContent=cur==={TOTAL-1}", HTML)
HTML = re.sub(r"detail\+' Score: '\+score\+'/100 \('\+pct\+'%\)'",
              "detail+' Score: '+score+'/'+TOTAL+' ('+pct+'%)'", HTML)
HTML = re.sub(r"document\.getElementById\('score-ring'\)\.style\.setProperty\('--pct',score\)",
              "document.getElementById('score-ring').style.setProperty('--pct',Math.round(score/TOTAL*100))", HTML)

# --- Add install button CSS if not present ---
INSTALL_CSS = """
.install-fab{position:fixed;bottom:calc(10px + var(--safe-b));right:10px;z-index:900;
  display:flex;align-items:center;gap:6px;padding:10px 14px;background:var(--accent);color:#fff;
  border:none;border-radius:999px;font-size:clamp(11px,2.8vw,13px);font-weight:700;cursor:pointer;
  box-shadow:0 4px 20px rgba(99,102,241,.5);transition:transform .15s}
.install-fab:active{transform:scale(.95)}
.install-fab.hidden{display:none}
.install-fab svg{width:16px;height:16px;fill:currentColor;flex-shrink:0}
.install-overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;display:none;
  align-items:center;justify-content:center;padding:16px}
.install-overlay.show{display:flex}
.install-modal{background:var(--surface);border:1px solid var(--border);border-radius:16px;
  padding:clamp(16px,4vw,24px);max-width:340px;width:100%;max-height:85dvh;overflow-y:auto}
.install-modal h3{font-size:clamp(16px,4vw,20px);margin-bottom:8px;display:flex;align-items:center;gap:8px}
.install-modal p,.install-modal li{font-size:clamp(12px,3vw,14px);color:var(--muted);line-height:1.45}
.install-modal ol{padding-left:18px;margin:8px 0}
.install-modal li{margin-bottom:6px;color:var(--text)}
.install-modal .modal-close{margin-top:14px;width:100%}
.install-start-btn{max-width:280px;width:100%;display:flex;align-items:center;justify-content:center;gap:8px}
"""

if '.install-fab' not in HTML:
    HTML = HTML.replace('</style>', INSTALL_CSS + '\n</style>')

# Add install FAB and modal before </body> if not present
INSTALL_HTML = """
<button class="install-fab" id="install-fab" onclick="handleInstallClick()" title="Install Quizzer">
  <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
  Install App
</button>
<div class="install-overlay" id="install-overlay" onclick="if(event.target===this)closeInstallModal()">
  <div class="install-modal">
    <h3><span style="background:var(--accent);color:#fff;width:28px;height:28px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-weight:800">Q</span> Install Quizzer</h3>
    <p id="install-modal-body">Loading instructions...</p>
    <button class="btn btn-primary modal-close" onclick="closeInstallModal()">Got it</button>
  </div>
</div>
"""

if 'id="install-fab"' not in HTML:
    HTML = HTML.replace('</div>\n<script>', '</div>\n' + INSTALL_HTML + '\n<script>')

# Update start screen - add install button in start content
if 'install-start-btn' not in HTML:
    HTML = HTML.replace(
        '<button class="btn btn-primary" style="max-width:280px;width:100%" onclick="startQuiz()">Start Quiz</button>',
        '<button class="btn btn-secondary install-start-btn" onclick="handleInstallClick()"><svg viewBox="0 0 24 24" style="width:18px;height:18px;fill:currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg> Install App</button>\n      <button class="btn btn-primary" style="max-width:280px;width:100%" onclick="startQuiz()">Start Quiz</button>'
    )

# Replace PWA install JS
OLD_PWA = """var deferredPrompt;
window.addEventListener('beforeinstallprompt',function(e){
  e.preventDefault();deferredPrompt=e;
  document.getElementById('install-hint').textContent='Tap Install App below or use Add to Home Screen.';
  var btn=document.createElement('button');
  btn.className='btn btn-secondary';btn.style.maxWidth='280px';btn.style.width='100%';
  btn.textContent='Install App';
  btn.onclick=function(){
    if(deferredPrompt){deferredPrompt.prompt();deferredPrompt.userChoice.then(function(){deferredPrompt=null;btn.remove();});}
  };
  var startBtn=document.querySelector('.start-content .btn-primary');
  startBtn.parentNode.insertBefore(btn,startBtn);
});"""

NEW_PWA = """var deferredPrompt=null;
var isStandalone=window.matchMedia('(display-mode: standalone)').matches||window.navigator.standalone===true;

function isIOS(){return /iPad|iPhone|iPod/.test(navigator.userAgent)&&!window.MSStream;}
function isAndroid(){return /Android/.test(navigator.userAgent);}

function closeInstallModal(){document.getElementById('install-overlay').classList.remove('show');}

function getInstallInstructions(){
  if(isIOS()){
    return '<p><strong>iPhone / iPad (Safari):</strong></p><ol><li>Open this page in <strong>Safari</strong></li><li>Tap the <strong>Share</strong> button (square with arrow) at the bottom</li><li>Scroll down and tap <strong>Add to Home Screen</strong></li><li>Tap <strong>Add</strong> — Quizzer will appear on your home screen!</li></ol>';
  }
  if(isAndroid()){
    return '<p><strong>Android (Chrome):</strong></p><ol><li>Tap <strong>Install App</strong> on this screen if the prompt appears</li><li>Or tap the <strong>menu ⋮</strong> (top right)</li><li>Select <strong>Install app</strong> or <strong>Add to Home screen</strong></li><li>Confirm to install Quizzer</li></ol>';
  }
  return '<p><strong>Desktop:</strong></p><ol><li>Look for the install icon in the address bar</li><li>Or open browser menu → <strong>Install Quizzer</strong></li><li>On some browsers, use <strong>Add to Home Screen</strong> from the menu</li></ol>';
}

function handleInstallClick(){
  if(isStandalone){alert('Quizzer is already installed!');return;}
  if(deferredPrompt){
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function(choice){
      if(choice.outcome==='accepted'){hideInstallButtons();}
      deferredPrompt=null;
    });
    return;
  }
  document.getElementById('install-modal-body').innerHTML=getInstallInstructions();
  document.getElementById('install-overlay').classList.add('show');
}

function hideInstallButtons(){
  var fab=document.getElementById('install-fab');
  if(fab)fab.classList.add('hidden');
  var hint=document.getElementById('install-hint');
  if(hint)hint.textContent='Quizzer is installed. Happy studying!';
}

if(isStandalone){hideInstallButtons();}

window.addEventListener('beforeinstallprompt',function(e){
  e.preventDefault();
  deferredPrompt=e;
  var hint=document.getElementById('install-hint');
  if(hint)hint.textContent='Tap Install App to add Quizzer to your home screen instantly.';
});

window.addEventListener('appinstalled',function(){hideInstallButtons();closeInstallModal();});"""

if OLD_PWA in HTML:
    HTML = HTML.replace(OLD_PWA, NEW_PWA)
elif 'handleInstallClick' not in HTML:
    HTML = HTML.replace('</script>\n</body>', NEW_PWA + '\n</script>\n</body>')

# Show topic in type badge area - optional: append topic to badge via JS - skip to keep UI clean

# Update install hint default
HTML = HTML.replace(
    'Tip: Add to Home Screen to install Quizzer as an app on your phone.',
    'Tap Install App below to add Quizzer to your home screen.'
)

# bump SW cache
HTML = HTML.replace("const CACHE='quizzer-v1'", "const CACHE='quizzer-v2'")

with open("Quizzer.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print("Quizzer.html rebuilt successfully")
