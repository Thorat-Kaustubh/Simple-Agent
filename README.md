**🤖 Dynamic Conversational Agent with Streamlit and Gemini**

This repository contains the code for a sophisticated conversational agent built with Python, Streamlit, and Google's Gemini API. The agent is designed to be context-aware, capable of understanding user intent, and can provide both structured data and executable code with detailed explanations.

Note: You will need to replace the placeholder image above with a screenshot of your running application.

**✨ Key Features**

Intelligent Intent Detection: The agent automatically determines if a user is asking for information or requesting a code snippet.

Context-Aware Responses: It remembers the last few messages in a conversation, allowing for natural follow-up questions (e.g., "explain the code you just gave me").

Code Generation with Explanations: When asked to generate code, the agent provides a formatted code block along with a clear, concept-by-concept explanation.

Structured Data Output: For informational queries, the agent responds with well-structured JSON, which is then formatted for easy reading.

High-Performance Async Backend: The agent's logic is built with Python's asyncio to ensure fast and non-blocking responses.

Polished User Interface: The frontend, built with Streamlit, is clean, modern, and features a card-based layout for a professional user experience.

**🛠️ Tech Stack**
Frontend: Streamlit

Backend & AI Logic: Python, asyncio

Language Model: Google Gemini API (gemini-2.5-flash-preview-05-20)

**🚀 Getting Started**

Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites

Python 3.8 or higher

A Google Gemini API Key

Installation & Setup

**Clone the repository:**

git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME


**Create and activate a virtual environment:**

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate


Install the required packages:

pip install -r requirements.txt


Set up your API Key:

Create a folder named .streamlit in the root of your project directory.

Inside the .streamlit folder, create a new file named secrets.toml.

Add your Gemini API key to the secrets.toml file like this:

GEMINI_API_KEY = "YOUR_API_KEY_HERE"


**Run the application:**
streamlit run app.py


The application should now be running in your web browser!
