# Automated Article Generation and Emailing

This repository contains a Python script that uses a locally hosted Llama2 language model to generate an article on a given topic, create a PDF of the article, and email it to a specified recipient. The script defines classes for managing agents, tasks, and a crew to coordinate the task execution.

## Features 

- Agent-based Task Management: Define agents and tasks to handle content generation.
- PDF Creation: Generate a PDF from the content produced by the LLM.
- Email Sending: Automatically send the generated PDF to a specified email address.

## Requirements 

- Python 3.6+
- Required libraries: os, smtplib, email, fpdf, langchain_community

## Installation

- Install dependencies:

```bash
pip install fpdf langchain_community
```

- Ensure you have llama2 model hosted locally:
> The script expects the Llama2 model to be accessible at http://localhost:11434.


```bash
curl http://localhost:11434
```

## Usage

Set up environment variables:

- The script uses OPENAI_API_KEY environment variable, though it is not required for Llama2. Can give gpt 4.0 api if you want faster response.

Modify the email credentials:

- Update the smtp_user and smtp_password with your SMTP credentials. Give app password for security reasons.

Expected Output:

- The script will generate a PDF named Generated_Article.pdf. 
- The PDF will be emailed to the specified recipient.

