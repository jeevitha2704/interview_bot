# AI Interview Bot 🤖

An intelligent interview preparation tool that generates personalized interview questions based on your resume using AI.

## Features

✨ **Resume Parsing**
- Supports PDF, DOCX, DOC, and TXT formats
- Extracts skills, experience, education, and certifications
- Identifies key accomplishments

🤖 **AI-Powered Question Generation**
- Generates interview questions tailored to your background
- Multiple question types: Technical, Behavioral, Mixed
- Questions based on your actual resume content

💬 **Interactive Interview**
- Practice answering questions in a realistic interview format
- Progress tracking through the interview
- Review and edit your answers
- Download interview results

## Prerequisites

- Python 3.8+
- OpenAI API Key (get it at https://platform.openai.com/api-keys)
- pip (Python package manager)

## Installation

1. **Clone or download the project**
```bash
cd /Users/jeevithaj/Downloads/INTERVIEW_BOT
```

2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

5. **Add your OpenAI API Key to `.env`**
```
OPENAI_API_KEY=sk-your-api-key-here
```

## Running the Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Open your browser**
```
http://localhost:5000
```

## Usage

1. **Upload Your Resume**
   - Click the upload area or drag and drop your resume
   - Supported formats: PDF, DOCX, DOC, TXT

2. **Review Resume Summary**
   - Check the extracted skills, experience, and education
   - Confirm all information is correct

3. **Configure Interview Settings**
   - Choose number of questions (3-10)
   - Select question type: Technical, Behavioral, or Mixed

4. **Generate Questions**
   - Click "Generate Interview Questions"
   - AI will create personalized questions based on your resume

5. **Take the Interview**
   - Start the interview and answer each question
   - Use navigation to review previous answers
   - Complete all questions

6. **Review Results**
   - See all your Q&A responses
   - Download results as a text file

## Project Structure

```
INTERVIEW_BOT/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── routes.py         # API endpoints
│   ├── resume_parser.py  # Resume parsing logic
│   └── question_generator.py  # AI question generation
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
└── uploads/              # Uploaded resumes (auto-created)
```

## API Endpoints

### `POST /upload`
Upload and parse a resume
- **Request**: Form data with `file` field
- **Response**: Parsed resume data with skills, experience, etc.

### `POST /generate-questions`
Generate interview questions
- **Request**: JSON with `resume_data`, `num_questions`, `question_type`
- **Response**: List of generated questions

### `POST /followup-question`
Generate a follow-up question
- **Request**: JSON with `previous_question`, `candidate_answer`, `resume_data`
- **Response**: Follow-up question

### `POST /evaluate-answer`
Evaluate a candidate's answer
- **Request**: JSON with `question`, `answer`, `resume_data`
- **Response**: Evaluation and score

## Customization

### Change Number of Questions
Edit the dropdown in the settings section or modify `num_questions` in the generate request.

### Modify Question Types
Add new question type categories in `question_generator.py`:
```python
if question_type == 'custom':
    # Add your custom logic
```

### Adjust Model or Temperature
In `app/question_generator.py`, modify:
```python
self.model = "gpt-4"  # Change model
temperature=0.7  # Adjust creativity (0-1)
```

## Troubleshooting

### "OpenAI API key not provided"
- Make sure you've created `.env` file with your API key
- Restart the server after adding the key

### "Resume parsing failed"
- Ensure your file is in a supported format (PDF, DOCX, DOC, TXT)
- Check file size (max 16MB)
- Try re-saving the file in the supported format

### Resume data not extracting correctly
- Some formatted PDFs may not parse perfectly
- Try converting to DOCX format first
- Ensure text is selectable (not scanned image)

## Performance Tips

- Generating 10 questions may take 30-60 seconds
- Keep resume to 1-2 pages for best results
- Use clear formatting and standard section headers

## Security

- Uploaded resumes are stored temporarily in the `uploads/` folder
- Files are automatically overwritten with new uploads
- No resume data is sent to OpenAI (only extracted information)

## Limitations

- Max file size: 16MB
- Max questions per session: 10
- Requires stable internet connection for OpenAI API

## Future Enhancements

- [ ] Real-time answer evaluation
- [ ] Mock interview video recording
- [ ] Detailed performance analytics
- [ ] Interview difficulty levels
- [ ] Support for more file formats
- [ ] Multi-language support
- [ ] Interview question database
- [ ] Peer comparison features

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for personal and commercial purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify your OpenAI API key is valid
3. Review error messages in browser console (F12)
4. Check server logs in terminal

## Credits

Built with:
- Flask - Web framework
- OpenAI GPT-3.5-turbo - AI language model
- PyPDF2 - PDF parsing
- python-docx - DOCX parsing

Enjoy your interview preparation! 🎉
