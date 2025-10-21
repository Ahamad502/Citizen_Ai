from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple in-memory session storage (in production, use proper session management)
users = {"admin": "admin"}

# Sample responses for common questions
sample_responses = {
    "hi": "Hello! I'm your CitizenAI assistant. How can I help you today?",
    "hello": "Hi there! I'm your CitizenAI assistant. What can I do for you?",
    "how are you": "I'm just a computer program, but I'm functioning well! How can I assist you today?",
    "what can you do": """I'm an AI assistant for CitizenAI, a civic engagement platform. I can help you with:

## Key Areas of Assistance

### 1. Civic Engagement
- Information on attending city council meetings
- Volunteering opportunities
- Board and commission participation

### 2. Voting & Elections
- Voter registration information
- Upcoming election dates
- Candidate information

### 3. Reporting Issues
- How to report neighborhood problems
- Contacting local representatives
- Requesting city services

### 4. Community Resources
- Local organizations and nonprofits
- Educational programs
- Youth engagement opportunities

What specific topic would you like to explore?""",
    "who are you": "I'm the CitizenAI assistant, here to help you with civic engagement and community-related questions.",
    "local government": """# Getting Involved in Local Government

Hello! I'm glad you're interested in civic engagement. Here's a concise overview of how you can get involved in local government:

## Key Ways to Participate

### 1. Attend Public Meetings
- **City Council Meetings**: Open to the public, great for learning about local issues
- **Planning Commission Meetings**: Deal with development and zoning matters
- **School Board Meetings**: Important for education policy in your district

### 2. Serve on Boards/Commissions
Many cities have appointed positions for citizens on boards dealing with:
- Parks and Recreation
- Public Safety
- Planning and Zoning
- Library Services

### 3. Volunteer in Your Community
- Local non-profits and community organizations
- Neighborhood associations
- Civic groups like Rotary or Lions Club

### 4. Vote in Local Elections
- Register to vote if you haven't already
- Participate in municipal and school board elections
- Local elections often have lower turnout but significant impact

### 5. Stay Informed
- Follow local government on social media
- Subscribe to city newsletters
- Read local newspapers for community updates

### 6. Contact Your Representatives
- Reach out to your city council member or mayor
- Attend "office hours" or town halls
- Provide input on local issues that matter to you

Would you like more specific information about any of these engagement opportunities?""",
    "voting": """# Voting & Elections Information

## Voter Registration
- **Eligibility**: U.S. citizens aged 18+ who are residents of their state
- **How to Register**: Online at your state's Secretary of State website, by mail, or in person
- **Deadline**: Usually 15-30 days before an election (varies by state)

## Finding Election Information
- Check your state's Secretary of State website for:
  - Upcoming election dates
  - Polling locations
  - Sample ballots
  - Candidate information

## Absentee/Mail-in Voting
- Available in most states for those who can't vote in person
- Request an absentee ballot well before the election
- Follow your state's specific requirements for submission

## Poll Worker Opportunities
- Paid positions to assist with election administration
- Training provided
- Help ensure fair and accessible elections

Would you like help finding your state's specific voting information?""",
    "report problem": """# Reporting Issues in Your Neighborhood

## Common Issues to Report
- Potholes and road damage
- Streetlight outages
- Graffiti or litter
- Water or sewer problems
- Park maintenance needs
- Noise complaints
- Animal control issues

## How to Report
### Online Methods
- Your city's official website (look for "Report a Problem" or "Service Request")
- Dedicated mobile apps (e.g., SeeClickFix, CitySourced)
- Social media channels of local government

### Phone Methods
- Non-emergency police line
- City hall main number
- Department-specific hotlines (Public Works, Utilities, etc.)

### In-Person Methods
- City hall service counters
- Community police substations
- Public meetings where you can speak directly to officials

## What to Include in Your Report
- Specific location (address or cross streets)
- Clear description of the problem
- Your contact information for follow-up
- Photos if possible

Would you like help finding the reporting system for your specific city?""",
    "community organizations": """# Finding Community Organizations

## Types of Organizations
### Service Organizations
- Food banks and pantries
- Homeless shelters
- Youth centers
- Senior centers

### Advocacy Groups
- Environmental organizations
- Neighborhood associations
- Civil rights groups
- Professional associations

### Cultural & Recreational
- Libraries
- Museums
- Sports leagues
- Arts councils

## How to Find Them
1. **Online Searches**
   - Search "[Your City] + volunteer opportunities"
   - Check volunteermatch.org or justserve.org
   - Look at your city's website community resources section

2. **Local Government Resources**
   - City hall community bulletin boards
   - Parks and Recreation Department
   - Public Library community boards

3. **Word of Mouth**
   - Ask neighbors, coworkers, or friends
   - Check community Facebook groups
   - Attend local events and meetings

## Getting Started
- Visit organization websites to learn about their mission
- Attend volunteer orientation sessions
- Start with one-time events before committing to ongoing roles

Would you like suggestions for specific types of organizations based on your interests?""",
    "petition": """# Starting a Petition for Local Change

Petitions are a powerful way to bring attention to issues and influence local decision-making. Here's how to start one effectively:

## 1. Define Your Issue Clearly
- Be specific about the problem you want to address
- Research existing policies or procedures related to your issue
- Identify the appropriate authority who can make the change

## 2. Gather Support
- Start with people you know (friends, family, neighbors)
- Use social media to reach a broader audience
- Attend community meetings to find like-minded individuals
- Collect contact information for follow-up

## 3. Choose the Right Platform
- **Online platforms**: Change.org, Petition2Congress, or local government websites
- **Paper petitions**: For local issues, sometimes physical signatures carry more weight
- **Hybrid approach**: Both online and offline collection

## 4. Write a Compelling Petition
- Include a clear, actionable request
- Provide background information and evidence
- Include a strong call to action
- Keep it concise but comprehensive

## 5. Submit to the Appropriate Authority
- City Council
- County Commissioners
- School Board
- Specific department heads

## 6. Follow Up
- Present the petition at public meetings
- Engage with media to raise awareness
- Continue building momentum for your cause

Would you like help with any specific aspect of creating your petition?""",
    "running for office": """# Requirements for Running for Local Office

Running for local office is an excellent way to directly impact your community. Here are the typical requirements and steps:

## Basic Eligibility Requirements
- **Age**: Usually 18 or older (varies by position)
- **Residency**: Must live in the jurisdiction where you're running
- **Voter registration**: Must be a registered voter
- **No felony convictions** (in most cases)

## Specific Requirements by Office Type

### City Positions (Mayor, Councilmember)
- Filing fee or petition with required signatures
- Statement of economic interests
- Campaign finance reporting requirements

### School Board
- Educational qualifications may apply in some districts
- Residency within school district boundaries
- Background check in some jurisdictions

### County Positions
- More stringent filing requirements
- Higher signature thresholds for ballot access
- Financial disclosure requirements

## Key Steps to Get Started

### 1. Research the Position
- Understand the duties and responsibilities
- Review term lengths and compensation
- Study the jurisdiction's charter or ordinances

### 2. File Required Paperwork
- Candidate intention forms
- Petition signatures (if required)
- Financial disclosure statements

### 3. Comply with Campaign Finance Laws
- Register your campaign committee
- Understand contribution limits
- Learn reporting deadlines

### 4. Campaign Effectively
- Develop a platform addressing local issues
- Engage with community members
- Attend public forums and debates
- Use social media and traditional outreach

Would you like detailed information about running for a specific type of local office?""",
    "business license": """# Applying for a Business License

## Why You Need a Business License
- Legal requirement in most jurisdictions
- Helps fund local services and infrastructure
- Protects consumers through regulation
- Generates revenue for the city

## Types of Licenses
- **General Business License**: Required for most businesses
- **Professional Licenses**: For specific professions (contractors, real estate agents, etc.)
- **Occupational Licenses**: For certain trades
- **Specialty Licenses**: For activities like food service, alcohol sales, etc.

## How to Apply
### 1. Determine What You Need
- Check your city/county website for requirements
- Contact the Business License Office for guidance
- Identify any additional permits (health, fire, zoning)

### 2. Gather Required Information
- Business name and address
- Owner information (SSN, address)
- Business structure (LLC, Corporation, etc.)
- Type of business activity
- Estimated number of employees

### 3. Submit Application
- Online through city/county portal
- In person at the Business License Office
- By mail (if available)

### 4. Pay Fees
- Vary based on business type and size
- May be annual or one-time fees
- Additional fees for specialty licenses

## Timeline and Renewals
- Processing typically takes 1-4 weeks
- Most licenses require annual renewal
- Keep documentation of your license current

Would you like help finding the requirements for your specific business type?""",
    "zoning laws": """# Understanding Local Zoning Laws

## What Are Zoning Laws?
Zoning laws divide a city or county into districts that specify:
- What types of buildings are allowed
- How land can be used (residential, commercial, industrial)
- Building height and size restrictions
- Parking requirements
- Setback distances from property lines

## Common Zoning Categories
### Residential Zones
- Single-family homes (R-1)
- Multi-family dwellings (R-2, R-3)
- Mixed residential/commercial (R-C)

### Commercial Zones
- Retail and service businesses (C-1)
- Offices and professional services (C-2)
- Major shopping centers (C-3)

### Industrial Zones
- Light manufacturing (I-1)
- Heavy industry (I-2)
- Warehousing and distribution (I-3)

### Special Purpose Zones
- Schools and churches
- Parks and recreation
- Public facilities

## How to Find Your Zoning
1. Visit your city/county planning department website
2. Use their online zoning map tool
3. Enter your address to see your zone designation
4. Review the zoning code for permitted uses

## Changing Zoning
- Requires a rezoning application
- Public hearing process
- Planning commission review
- City council approval

Would you like help understanding the zoning for a specific property or use?""",
    "street repair": """# Requesting Street Repairs

## Types of Street Issues
- **Potholes**: Depressions in pavement that collect water
- **Cracks**: Surface fractures that can worsen over time
- **Heaving**: Pavement pushed up by freeze/thaw cycles
- **Flooding**: Poor drainage causing water accumulation
- **Missing Signs**: Traffic or street name signs that are damaged/missing

## How to Report Street Issues
### Online Reporting
- Visit your city's official website
- Look for "Report a Problem" or "Service Request" portal
- Many cities have mobile apps for easy reporting

### Phone Reporting
- Call your city's 311 non-emergency number
- Contact Public Works Department directly
- Some areas have dedicated road repair hotlines

### In-Person Reporting
- Visit City Hall service counters
- Attend city council meetings to report issues
- Speak with Public Works staff at community events

## What Information to Provide
- Exact location (address or nearest intersection)
- Description of the problem and its severity
- Photos if possible
- Your contact information for follow-up

## Timeline for Repairs
- Emergency repairs (large potholes): 24-48 hours
- Routine maintenance: 2-4 weeks
- Major reconstruction: Scheduled projects with longer timelines

Would you like help finding your city's specific reporting system?""",
    "public transportation": """# Public Transportation Information

## Types of Public Transit
### Fixed Route Services
- **Buses**: Most common form, serving major corridors
- **Light Rail/Trams**: Electric rail systems in urban areas
- **Subway/Metro**: Underground rail systems in large cities
- **Commuter Rail**: Connecting suburbs to city centers

### Flexible Services
- **Paratransit**: Door-to-door service for those unable to use fixed routes
- **Dial-a-Ride**: Call-ahead transportation in rural areas
- **Shuttle Services**: Connecting to major transit hubs

## How to Use Public Transit
### 1. Plan Your Trip
- Use transit apps (Transit, Moovit, Google Maps)
- Check route maps on transit authority websites
- Note schedules and frequency of service

### 2. Pay Fares
- **Single Ride**: Pay per trip (cash, card, mobile app)
- **Day Pass**: Unlimited rides for one day
- **Weekly/Monthly Pass**: Cost savings for regular users
- **Annual Pass**: Best value for daily commuters

### 3. Access Real-Time Information
- Mobile apps for arrival times
- Digital displays at stops/stations
- Service alerts for delays or detours

## Accessibility Features
- Wheelchair ramps and lifts
- Audio/visual stop announcements
- Priority seating
- Tactile guidance strips

## Special Programs
- Reduced fares for seniors, students, disabled riders
- Free transit for certain groups (veterans, children)
- Bike-share integration at transit stations

Would you like specific information about transit options in your area?""",
    "students": """# Student Engagement in Local Government

## Opportunities for Students
### High School Students
- **Student Government**: Learn leadership and governance
- **Volunteer Programs**: Community service hours
- **Internships**: Work with local officials or departments
- **Youth Advisory Councils**: Many cities have councils for teens

### College Students
- **Campus Government**: Student senate, clubs, organizations
- **Internships**: Credit-bearing work with local agencies
- **Volunteer Boards**: Many cities seek young voices on boards
- **Campaign Work**: Gain experience with local campaigns

## Educational Programs
### Mock Elections
- Participate in school mock elections
- Learn about voting process and civic responsibility
- Understand how government works

### Government Simulations
- Model UN programs
- Mock trial competitions
- Student government simulations

### Field Trips & Tours
- Visit City Hall and meet officials
- Tour courthouses and government buildings
- Attend public meetings as observers

## Benefits of Early Engagement
- Develops civic responsibility
- Builds leadership skills
- Creates networking opportunities
- Enhances college applications
- Prepares for future civic participation

## How to Get Started
1. Talk to teachers about opportunities
2. Join relevant clubs (Key Club, Future Leaders, etc.)
3. Contact your city's Youth Services Department
4. Attend public meetings with family
5. Volunteer for local campaigns or causes

Would you like suggestions for specific opportunities based on your age or interests?""",
    "default": "I understand your question. As a civic engagement assistant, I'm here to help you learn about community involvement, local government, and civic participation. Could you please be more specific about what you'd like to know?"
}

@app.route("/")
def index():
    return send_from_directory('templates', 'index.html')

@app.route("/about")
def about():
    return send_from_directory('templates', 'about.html')

@app.route("/services")
def services():
    return send_from_directory('templates', 'services.html')

@app.route("/chat")
def chat():
    return send_from_directory('templates', 'chat.html')

@app.route("/dashboard")
def dashboard():
    return send_from_directory('templates', 'dashboard.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Simple authentication - in production, use proper user validation
        if username in users and users[username] == password:
            # Successful login - redirect to chat
            return jsonify({"status": "success", "redirect": "/chat"})
        else:
            # Failed login - return error
            return jsonify({"status": "error", "message": "Invalid credentials"})
    
    # GET request - show login page
    return send_from_directory('templates', 'login.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/<path:filename>')
def serve_templates(filename):
    return send_from_directory('templates', filename)

@app.route("/chatbot", methods=["POST", "OPTIONS"])
def chatbot():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})
    
    try:
        # Get the JSON message from the frontend
        data = request.get_json()
        user_message = data.get("message", "") if data else ""
        
        # Convert to lowercase for matching
        user_message_lower = user_message.lower().strip()
        
        # Default response
        ai_reply = sample_responses["default"]
        
        # More comprehensive matching logic
        # Check for specific phrases first
        if any(phrase in user_message_lower for phrase in ["participate in community", "ways to participate", "community involvement", "get involved in community"]):
            ai_reply = sample_responses["local government"]
        elif any(phrase in user_message_lower for phrase in ["attend city council", "city council meeting", "council meeting"]):
            ai_reply = sample_responses["local government"]
        elif any(phrase in user_message_lower for phrase in ["role of local government", "local government function"]):
            ai_reply = sample_responses["local government"]
        elif any(phrase in user_message_lower for phrase in ["register to vote", "voter registration", "how to vote"]):
            ai_reply = sample_responses["voting"]
        elif any(phrase in user_message_lower for phrase in ["next local election", "election date", "when is election"]):
            ai_reply = sample_responses["voting"]
        elif any(phrase in user_message_lower for phrase in ["voting requirement", "vote requirement", "eligibility to vote"]):
            ai_reply = sample_responses["voting"]
        elif any(phrase in user_message_lower for phrase in ["learn about candidate", "candidate information", "who are the candidates"]):
            ai_reply = sample_responses["voting"]
        elif any(phrase in user_message_lower for phrase in ["current issue", "local issue", "city issue"]):
            ai_reply = sample_responses["report problem"]
        elif any(phrase in user_message_lower for phrase in ["report problem", "report issue", "complain about"]):
            ai_reply = sample_responses["report problem"]
        elif any(phrase in user_message_lower for phrase in ["local policy", "city policy", "municipal policy"]):
            ai_reply = sample_responses["report problem"]
        elif any(phrase in user_message_lower for phrase in ["contact council member", "reach councilman", "talk to mayor"]):
            ai_reply = sample_responses["report problem"]
        elif any(phrase in user_message_lower for phrase in ["community organization", "local organization", "nonprofit"]):
            ai_reply = sample_responses["community organizations"]
        elif any(phrase in user_message_lower for phrase in ["volunteer locally", "volunteer opportunity", "where to volunteer"]):
            ai_reply = sample_responses["community organizations"]
        elif any(phrase in user_message_lower for phrase in ["neighborhood association", "start neighborhood group"]):
            ai_reply = sample_responses["community organizations"]
        elif any(phrase in user_message_lower for phrase in ["city service", "municipal service", "what service"]):
            ai_reply = sample_responses["community organizations"]
        elif any(phrase in user_message_lower for phrase in ["organize community event", "plan community event"]):
            ai_reply = sample_responses["petition"]
        elif any(phrase in user_message_lower for phrase in ["propose law", "new law", "local legislation"]):
            ai_reply = sample_responses["petition"]
        elif any(phrase in user_message_lower for phrase in ["business license", "apply for license"]):
            ai_reply = sample_responses["business license"]
        elif any(phrase in user_message_lower for phrase in ["zoning law", "land use", "property zoning"]):
            ai_reply = sample_responses["zoning laws"]
        elif any(phrase in user_message_lower for phrase in ["street repair", "road repair", "fix street", "pothole"]):
            ai_reply = sample_responses["street repair"]
        elif any(phrase in user_message_lower for phrase in ["public transportation", "bus service", "transit option"]):
            ai_reply = sample_responses["public transportation"]
        elif any(phrase in user_message_lower for phrase in ["student involvement", "youth program", "school volunteer"]):
            ai_reply = sample_responses["students"]
        else:
            # Fallback to keyword-based matching
            for key, value in sample_responses.items():
                # Skip the default response
                if key == "default":
                    continue
                    
                # Direct keyword matching
                if key in user_message_lower:
                    ai_reply = value
                    break
                
                # Additional checks for specific terms
                if key == "petition" and ("petition" in user_message_lower or "start a petition" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "running for office" and ("running for office" in user_message_lower or "run for office" in user_message_lower or "requirements for office" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "voting" and ("voting" in user_message_lower or "election" in user_message_lower or "vote" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "report problem" and ("report" in user_message_lower or "problem" in user_message_lower or "issue" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "community organizations" and ("organization" in user_message_lower or "volunteer" in user_message_lower or "nonprofit" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "business license" and ("business license" in user_message_lower or "license" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "zoning laws" and ("zoning" in user_message_lower or "land use" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "street repair" and ("street" in user_message_lower or "road" in user_message_lower or "repair" in user_message_lower or "pothole" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "public transportation" and ("transportation" in user_message_lower or "bus" in user_message_lower or "transit" in user_message_lower):
                    ai_reply = value
                    break
                    
                if key == "students" and ("student" in user_message_lower or "school" in user_message_lower or "youth" in user_message_lower):
                    ai_reply = value
                    break
        
        # Return the reply as JSON
        return jsonify({"reply": ai_reply})
    except Exception as e:
        # Generic fallback
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)