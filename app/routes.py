from flask import Blueprint, request, jsonify, current_app, render_template
import os
import uuid
from werkzeug.utils import secure_filename
from app.resume_parser import ResumeParser
from app.question_generator import QuestionGenerator

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/', methods=['GET'])
def index():
    """Serve the main page"""
    return render_template('index.html')

@main_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'AI Interviewer is running'})

@main_bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, unique_filename)
        
        file.save(file_path)
        
        # Parse resume
        parser = ResumeParser(file_path)
        resume_data = parser.parse()
        
        # Store file path in resume data for later reference
        resume_data['file_path'] = file_path
        resume_data['original_filename'] = filename
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and parsed successfully',
            'resume_data': {
                'skills': resume_data.get('skills', []),
                'experience': resume_data.get('experience', []),
                'education': resume_data.get('education', []),
                'certifications': resume_data.get('certifications', []),
                'contact_info': resume_data.get('contact_info', {}),
                'key_highlights': resume_data.get('key_highlights', [])
            },
            'file_id': unique_filename
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/generate-questions', methods=['POST'])
def generate_questions():
    """Generate interview questions"""
    try:
        data = request.get_json()
        
        if not data or 'resume_data' not in data:
            return jsonify({'error': 'Resume data required'}), 400
        
        resume_data = data['resume_data']
        num_questions = data.get('num_questions', 5)
        question_type = data.get('question_type', 'mixed')
        
        # Validate inputs
        if num_questions < 1 or num_questions > 10:
            num_questions = 5
        
        if question_type not in ['technical', 'behavioral', 'mixed']:
            question_type = 'mixed'
        
        # Generate questions
        generator = QuestionGenerator()
        result = generator.generate_questions(resume_data, num_questions, question_type)
        
        return jsonify({
            'success': True,
            'message': 'Questions generated successfully',
            'data': result
        }), 200
    
    except ValueError as ve:
        return jsonify({'error': f'Configuration error: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/followup-question', methods=['POST'])
def followup_question():
    """Generate a follow-up question"""
    try:
        data = request.get_json()
        
        required_fields = ['previous_question', 'candidate_answer', 'resume_data']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: previous_question, candidate_answer, resume_data'}), 400
        
        generator = QuestionGenerator()
        followup = generator.generate_followup_question(
            data['previous_question'],
            data['candidate_answer'],
            data['resume_data']
        )
        
        return jsonify({
            'success': True,
            'followup_question': followup
        }), 200
    
    except ValueError as ve:
        return jsonify({'error': f'Configuration error: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/evaluate-answer', methods=['POST'])
def evaluate_answer():
    """Evaluate candidate's answer"""
    try:
        data = request.get_json()
        
        required_fields = ['question', 'answer', 'resume_data']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: question, answer, resume_data'}), 400
        
        generator = QuestionGenerator()
        evaluation = generator.evaluate_answer(
            data['question'],
            data['answer'],
            data['resume_data']
        )
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        }), 200
    
    except ValueError as ve:
        return jsonify({'error': f'Configuration error: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
