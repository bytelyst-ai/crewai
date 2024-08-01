import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from langchain_community.llms import Ollama

# Set environment variable for API key
#  (if needed ie it is used for gpt api since i dont have chatgpt 4 so i couldnt give it gpt (open ai api)
# so i used llama model which is free to use and also it doesnt require any apis)
os.environ["OPENAI_API_KEY"] = "NA"

# Initialize the LLM with correct base URL and model
llm = Ollama(
    model="llama2",
    base_url="http://localhost:11434"  # Ensure this URL is correct which can be done by 
)

# Define the Agent class
class Agent:
    def __init__(self, role, goal, backstory, allow_delegation, verbose, llm):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.allow_delegation = allow_delegation
        self.verbose = verbose
        self.llm = llm

    def perform_task(self, task):
        try:
            # Generate the article using the LLM
            prompt = f"Write an article of at least 500 words on the topic: {task.description}"
            response = self.llm.predict(prompt)
            result = response.strip()  # Clean up the response
            
            # Ensure the result meets the minimum word count requirement
            if len(result.split()) < 500:
                result = "Generated article is too short. Please try again."
        except Exception as e:
            result = f"Error: {e}"
        
        if self.verbose:
            print(f"{self.role} is performing the task: {task.description}")
        
        return result

# Define the Task class
class Task:
    def __init__(self, description, agent, expected_output):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output

# Define the Crew class
class Crew:
    def __init__(self, agents, tasks, verbose):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose

    def kickoff(self):
        results = {}
        for task in self.tasks:
            result = task.agent.perform_task(task)
            results[task] = result
        return results

# Define PDF creation function
def create_pdf(title, content, filename):
    pdf = FPDF()
    pdf.add_page()

    # Title Page
    #b-bold and c-centre
    pdf.set_font("Arial", size=24,style='B')
    pdf.set_y(90)
    pdf.multi_cell(0, 10, title, align="C")

    pdf.set_font("Arial", size=16,style='B')

    
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)

    pdf.output(filename)

# Define email sending function
def send_email(pdf_path, subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach body
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF
    with open(pdf_path, 'rb') as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(pdf_path))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
    msg.attach(part)

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

#since my laptop couldnt import agents,tasks,crew and process i had to initalise all those components i could find answers on github how to initialise all the components
# Initialize the agent
content_agent = Agent(
    role="Content Generator",
    goal="Generate a comprehensive article on the given topic.",
    backstory="You are an expert content writer with the ability to create detailed and informative articles.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Create a task
task = Task(
    description="The impact of renewable energy on global warming",
    agent=content_agent,
    expected_output="A comprehensive article of at least 500 words."
)

# Initialize the crew with agents and tasks
crew = Crew(
    agents=[content_agent],
    tasks=[task],
    verbose=2
)

# Start the crew and get the result
result = crew.kickoff()

# PDF file path
pdf_filename = "Generated_Article.pdf"

# Process result and create the PDF
for task, article in result.items():
    print(f"Task description: {task.description}")
    print(f"Result: {article}")

    # Create the PDF with the generated article
    title = task.description
    create_pdf(title, article, pdf_filename)
    print(f"PDF created: {pdf_filename}")

     # Defining email parameters
    subject = f"Article: {title}"
    body = "Please find the attached article."
    to_email = "Bytelyst+interviews@gmail.com"
    from_email = "malvika.malu6@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "malvika.malu6@gmail.com"
    smtp_password = "rewu hevg emum preg" #we need to use app password instead of our own to avoid security issues

    # Sending the email with the attached PDF
    send_email(pdf_filename, subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password)
    print(f"Email sent to: {to_email}")
