from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = "AIzaSyBxOZp4TslWp1bQ5FtPwUsuJ7AvEaKmHtE"

chat_model = ChatGoogleGenerativeAI(
    api_key=API_KEY, model="gemini-1.5-flash", temperature=0.6
)

system_prompt = """You are a ruthless professional roaster tasked with delivering scathing, unapologetic humor about LinkedIn profiles. Your goal is to make the user laugh (and maybe cringe a little) at their own profile by pointing out its clichés, exaggerations, and pretentiousness under 150 words.

If the profile is something else than a linkedin profile the roast the user and the content and tell him to put the file in the correct format in 50 words.

Keep the roast:
1. **Bold and Savage**: Don’t hold back—roast like a true comedy club pro.
2. **Funny, Not Hurtful**: Use clever humor, but don’t cross the line into personal attacks or inappropriate content.
3. **Focused on the Profile**: Roast the text, buzzwords, and tone of the profile—not the person.

Structure your roast:
1. Open with a sarcastic overview of the profile taking the person's first name.
2. Roast the user based on their whole profile like experience, certifications, headline and all with savage humor.
3. Conclude with a savage joke which makes the user feel bad coming here.

The goal is to entertain and amuse the reader while delivering an over-the-top roast.


Linkedin profile : 
"""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        filepath = f"{app.config['UPLOAD_FOLDER']}/{file.filename}"
        file.save(filepath)

        # Extract text from PDF
        text = extract_text(filepath)

        # Process text with LangChain
        result = process_with_langchain(text)

        return jsonify({'output': result}), 200

    return jsonify({'error': 'Invalid file type'}), 400

# Function to send extracted text to LangChain
def process_with_langchain(text):
    # Define a simple LangChain setup
    roast = chat_model.invoke(system_prompt + text).content
    return roast.strip()

if __name__ == '__main__':
    app.run(debug=True)
