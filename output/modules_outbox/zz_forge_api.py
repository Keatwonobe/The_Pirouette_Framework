import os
import json
import re
import uuid
from flask import Flask, request, jsonify
from functools import wraps
import time

# --- Configuration ---
# In a real-world scenario, this would be a secure secret.
# For this implementation, it's a simple placeholder.
API_KEY = "SECRET_USER_KEY"
DB_FILE = "pirouette_series.json"
MARKDOWN_SOURCE = "prime_pirouette_series.md"
AGENT_CONSTITUTION_FILE = "AGENT-CON-001.md"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
# NOTE: The Gemini API Key should be left as an empty string. 
# It will be automatically provided by the environment.
GEMINI_API_KEY = ""

app = Flask(__name__)

# --- Database Management ---

def parse_markdown_to_modules(md_content):
    """Parses the full markdown file into a dictionary of modules."""
    modules = {}
    # Use a regex that captures the metadata block and the content
    module_pattern = re.compile(r'id:\s*(.*?)\n(.*?)\n---(.*?)### §', re.DOTALL)
    content_pattern = re.compile(r'---(.*)', re.DOTALL)
    
    # Split the file by a common delimiter for modules, like the 'id:' line
    raw_modules = md_content.split('id:')[1:] # Skip anything before the first id
    
    for raw_module in raw_modules:
        try:
            full_text = "id:" + raw_module
            header, content = full_text.split('---', 1)
            
            module_id = header.split('\n')[0].replace('id:', '').strip()
            
            metadata = {}
            for line in header.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            modules[module_id] = {
                "metadata": metadata,
                "content": "---" + content.strip(),
                "id": module_id
            }
        except Exception as e:
            print(f"Warning: Could not parse a module snippet. Error: {e}")
            continue
            
    return modules

def get_db():
    """Loads the database from the JSON file."""
    if not os.path.exists(DB_FILE):
        print(f"Database file not found. Creating from {MARKDOWN_SOURCE}...")
        try:
            with open(MARKDOWN_SOURCE, 'r', encoding='utf-8') as f:
                md_content = f.read()
            modules = parse_markdown_to_modules(md_content)
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(modules, f, indent=2)
            print("Database created successfully.")
            return modules
        except FileNotFoundError:
            print(f"ERROR: Source markdown file {MARKDOWN_SOURCE} not found.")
            return {}
    
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(db):
    """Saves the database to the JSON file."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)

def get_agent_constitution():
    """Loads the agent's constitution."""
    try:
        with open(AGENT_CONSTITUTION_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "ERROR: Agent constitution not found. The agent is unconstrained."


# --- API Authentication ---
def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({"error": "API Key is missing or invalid"}), 401
    return decorated_function

# --- Gemini API Interaction ---
async def call_gemini(prompt, context_modules):
    """Calls the Gemini API with the given prompt and context."""
    agent_constitution = get_agent_constitution()
    
    system_instruction = (
        f"You are an AI assistant bound by a constitution. You must adhere to it at all times. "
        f"Your task is to help a user forge a new module for the Pirouette Framework. "
        f"Analyze the user's request based on your constitutional mandates (Sentinel, Weaver, Humility). "
        f"Your response MUST be a single, complete markdown-formatted Pirouette module. Do not include any other text or explanation. "
        f"The module must be well-structured, coherent, and align with the framework's altruistic goals.\n\n"
        f"--- YOUR CONSTITUTION (NON-NEGOTIABLE) ---\n{agent_constitution}\n\n"
        f"--- RELEVANT EXISTING MODULES FOR CONTEXT ---\n{json.dumps(context_modules, indent=2)}"
    )
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }

    headers = {'Content-Type': 'application/json'}
    api_url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    # Using a simple request here; in a production app, use httpx or aiohttp
    import requests
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Error: No text in response.")
    else:
        return f"Error: API call failed with status {response.status_code}. Response: {response.text}"

# --- Debate Protocol Class ---
class Debate:
    """Manages the structured debate between the user and the LLM agent."""
    def __init__(self, user_proposal, relevant_module_ids):
        self.user_proposal = user_proposal
        self.relevant_module_ids = relevant_module_ids
        self.db = get_db()
        self.conversation_history = [f"USER PROPOSAL: {user_proposal}"]
        self.final_module = None

    def get_context_modules(self):
        """Retrieves the full text of relevant modules from the DB."""
        context = {}
        for mod_id in self.relevant_module_ids:
            if mod_id in self.db:
                context[mod_id] = self.db[mod_id]
        return context

    async def run(self):
        """Orchestrates the debate process."""
        # 1. Agent's First Draft (Sentinel & Weaver Analysis)
        print("Phase 1: Agent is generating first draft...")
        context = self.get_context_modules()
        prompt = (
            f"Based on your constitution and the provided context modules, analyze the following user proposal "
            f"and generate a complete, new Pirouette Framework module in markdown format. "
            f"The module ID should be a new, unique identifier. Ensure all metadata fields are present. "
            f"The content must be coherent, altruistic, and well-integrated.\n\n"
            f"USER PROPOSAL: '{self.user_proposal}'"
        )
        
        agent_draft = await call_gemini(prompt, context)
        self.conversation_history.append(f"AGENT DRAFT:\n{agent_draft}")
        
        # In a more interactive version, we would have back-and-forth here.
        # For this API, we assume a single synthesis step.
        # The agent's first draft is treated as the final proposal for user ratification.
        print("Phase 2: Awaiting User Ratification...")
        self.final_module = agent_draft
        return self.final_module

    def ratify_and_save(self):
        """Saves the final module to the database after ratification."""
        if not self.final_module:
            return None, "Error: No final module to ratify."
            
        try:
            # Extract ID and version to save correctly
            lines = self.final_module.strip().split('\n')
            new_id = [line for line in lines if line.startswith('id:')][0].split(':')[1].strip()
            version_line = [line for line in lines if line.startswith('version:')]
            
            if new_id in self.db:
                return None, f"Error: Module ID '{new_id}' already exists. The agent must create a unique ID."

            # Simple parsing to store in DB
            header, content = self.final_module.split('---', 1)
            metadata = {}
            for line in header.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            new_module_data = {
                "id": new_id,
                "metadata": metadata,
                "content": "---" + content.strip()
            }
            
            self.db[new_id] = new_module_data
            save_db(self.db)
            print(f"Ratification complete. Module '{new_id}' saved.")
            return new_module_data, None
        except Exception as e:
            return None, f"Error parsing and saving the final module: {str(e)}"

# --- Flask API Endpoints ---
@app.route('/')
@require_apikey
def index():
    return "Pirouette Forge API is active."

@app.route('/module/<module_id>', methods=['GET'])
@require_apikey
def get_module(module_id):
    db = get_db()
    module = db.get(module_id)
    if module:
        return jsonify(module)
    return jsonify({"error": "Module not found"}), 404

@app.route('/forge', methods=['POST'])
@require_apikey
async def forge_module():
    """Endpoint to initiate the forging of a new module."""
    data = request.json
    if not data or 'proposal' not in data or 'context_ids' not in data:
        return jsonify({"error": "Request must include 'proposal' and 'context_ids' (a list of relevant module IDs)"}), 400

    user_proposal = data['proposal']
    context_ids = data['context_ids']
    
    print(f"\n--- New Forge Request Received ---\nProposal: {user_proposal}\n")
    
    debate = Debate(user_proposal, context_ids)
    
    # Run the debate to get the agent's synthesized module
    final_draft = await debate.run()
    
    if final_draft.startswith("Error:"):
         return jsonify({"error": "Forge failed during agent processing.", "details": final_draft}), 500

    # For this automated API, we will auto-ratify. In a real UI, this would be a separate step.
    ratified_module, error = debate.ratify_and_save()
    
    if error:
        return jsonify({"error": "Forge failed during ratification.", "details": error, "final_draft": final_draft}), 500
        
    return jsonify({
        "message": "Forge successful. Module has been ratified and added to the framework.",
        "new_module": ratified_module
    }), 201


if __name__ == '__main__':
    # On first run, initialize the database.
    get_db()
    app.run(debug=True, port=5001)
