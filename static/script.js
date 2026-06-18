// Global state
let resumeData = null;
let questions = [];
let currentQuestionIndex = 0;
let interviewAnswers = [];

// Elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadStatus = document.getElementById('upload-status');
const uploadSection = document.getElementById('upload-section');
const summarySection = document.getElementById('summary-section');
const settingsSection = document.getElementById('settings-section');
const generateBtn = document.getElementById('generate-btn');
const questionsSection = document.getElementById('questions-section');
const questionsContainer = document.getElementById('questions-container');
const interviewSection = document.getElementById('interview-section');
const interviewContainer = document.getElementById('interview-container');
const interviewBtn = document.getElementById('interview-btn');

// Upload area event listeners
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFileUpload(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) {
        handleFileUpload(e.target.files[0]);
    }
});

generateBtn.addEventListener('click', generateQuestions);
interviewBtn.addEventListener('click', startInterview);

// File upload handler
async function handleFileUpload(file) {
    if (!file) return;

    // Validate file type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.docx')) {
        showStatus('Invalid file type. Please upload PDF, DOCX, or TXT.', 'error');
        return;
    }

    showStatus('Uploading and parsing your resume...', 'loading');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        resumeData = data.resume_data;
        showStatus(`Resume uploaded successfully! Found ${resumeData.skills.length} skills.`, 'success');

        // Show summary
        displayResumeSummary(resumeData);
        summarySection.style.display = 'block';
        settingsSection.style.display = 'block';

    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Display resume summary
function displayResumeSummary(data) {
    const summaryDiv = document.getElementById('resume-summary');
    
    let html = '';

    if (data.skills && data.skills.length > 0) {
        html += `
            <div class="summary-item">
                <h3>Skills (${data.skills.length})</h3>
                <ul>${data.skills.slice(0, 8).map(skill => `<li>${skill}</li>`).join('')}</ul>
            </div>
        `;
    }

    if (data.experience && data.experience.length > 0) {
        html += `
            <div class="summary-item">
                <h3>Experience</h3>
                <ul>${data.experience.slice(0, 3).map(exp => `<li>${exp}</li>`).join('')}</ul>
            </div>
        `;
    }

    if (data.education && data.education.length > 0) {
        html += `
            <div class="summary-item">
                <h3>Education</h3>
                <ul>${data.education.map(edu => `<li>${edu}</li>`).join('')}</ul>
            </div>
        `;
    }

    if (data.key_highlights && data.key_highlights.length > 0) {
        html += `
            <div class="summary-item">
                <h3>Key Highlights</h3>
                <ul>${data.key_highlights.slice(0, 3).map(highlight => `<li>${highlight}</li>`).join('')}</ul>
            </div>
        `;
    }

    summaryDiv.innerHTML = html;
}

// Generate questions
async function generateQuestions() {
    const numQuestions = document.getElementById('question-count').value;
    const questionType = document.getElementById('question-type').value;

    if (!resumeData) {
        showStatus('Please upload a resume first', 'error');
        return;
    }

    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner"></span> Generating questions...';

    try {
        const response = await fetch('/generate-questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_data: resumeData,
                num_questions: parseInt(numQuestions),
                question_type: questionType
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate questions');
        }

        questions = data.data.questions;
        displayQuestions(questions);
        questionsSection.style.display = 'block';
        showStatus('Questions generated successfully!', 'success');

    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerHTML = 'Generate Interview Questions';
    }
}

// Display questions
function displayQuestions(questionsList) {
    questionsContainer.innerHTML = '';

    questionsList.forEach((question, index) => {
        const div = document.createElement('div');
        div.className = 'question-item';
        div.innerHTML = `<p><strong>${index + 1}.</strong> ${question}</p>`;
        questionsContainer.appendChild(div);
    });
}

// Start interview
function startInterview() {
    if (questions.length === 0) {
        showStatus('Please generate questions first', 'error');
        return;
    }

    currentQuestionIndex = 0;
    interviewAnswers = [];
    interviewSection.style.display = 'block';
    displayInterviewQuestion(0);
}

// Display interview question
function displayInterviewQuestion(index) {
    if (index >= questions.length) {
        showInterviewSummary();
        return;
    }

    const question = questions[index];
    const progress = ((index) / questions.length * 100).toFixed(0);

    interviewContainer.innerHTML = `
        <div class="progress">
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progress}%"></div>
            </div>
            <small>${index + 1} of ${questions.length}</small>
        </div>

        <div class="interview-question">
            <h3>Question ${index + 1}</h3>
            <p>${question}</p>
            <textarea id="answer-input" placeholder="Type your answer here..." autofocus></textarea>
            
            <div class="interview-controls">
                ${index > 0 ? `<button class="btn btn-secondary" onclick="previousQuestion()">← Previous</button>` : ''}
                <button class="btn btn-primary" onclick="submitAnswer()">
                    ${index === questions.length - 1 ? 'Finish Interview' : 'Next →'}
                </button>
            </div>
        </div>
    `;

    // Focus on textarea
    setTimeout(() => document.getElementById('answer-input').focus(), 100);
}

// Submit answer
function submitAnswer() {
    const answerInput = document.getElementById('answer-input');
    const answer = answerInput.value.trim();

    if (!answer) {
        showStatus('Please provide an answer', 'error');
        return;
    }

    interviewAnswers.push({
        question: questions[currentQuestionIndex],
        answer: answer
    });

    currentQuestionIndex++;
    displayInterviewQuestion(currentQuestionIndex);
}

// Previous question
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        const previousAnswer = interviewAnswers[currentQuestionIndex];
        
        interviewContainer.innerHTML = `
            <div class="progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(currentQuestionIndex / questions.length * 100).toFixed(0)}%"></div>
                </div>
                <small>${currentQuestionIndex + 1} of ${questions.length}</small>
            </div>

            <div class="interview-question">
                <h3>Question ${currentQuestionIndex + 1}</h3>
                <p>${questions[currentQuestionIndex]}</p>
                <textarea id="answer-input" placeholder="Type your answer here...">${previousAnswer.answer}</textarea>
                
                <div class="interview-controls">
                    ${currentQuestionIndex > 0 ? `<button class="btn btn-secondary" onclick="previousQuestion()">← Previous</button>` : ''}
                    <button class="btn btn-primary" onclick="submitAnswer()">
                        ${currentQuestionIndex === questions.length - 1 ? 'Finish Interview' : 'Next →'}
                    </button>
                </div>
            </div>
        `;
    }
}

// Show interview summary
function showInterviewSummary() {
    let html = '<h3>Interview Complete! 🎉</h3>';
    html += '<p>Thank you for completing the interview. Here are your responses:</p>';

    interviewAnswers.forEach((item, index) => {
        html += `
            <div class="interview-question">
                <h4>Q${index + 1}: ${item.question}</h4>
                <p><strong>Your Answer:</strong></p>
                <p>${item.answer}</p>
            </div>
        `;
    });

    html += `
        <button class="btn btn-primary" onclick="downloadResults()">📥 Download Results</button>
        <button class="btn btn-secondary" onclick="location.reload()">↻ Start Over</button>
    `;

    interviewContainer.innerHTML = html;
}

// Download results
function downloadResults() {
    let content = 'AI Interview Bot Results\n';
    content += '========================\n\n';
    content += `Date: ${new Date().toLocaleDateString()}\n\n`;

    content += 'Resume Summary:\n';
    content += `Skills: ${resumeData.skills.join(', ')}\n\n`;

    content += 'Interview Q&A:\n';
    interviewAnswers.forEach((item, index) => {
        content += `\nQuestion ${index + 1}: ${item.question}\n`;
        content += `Answer: ${item.answer}\n`;
    });

    // Create blob and download
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `interview-results-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Helper functions
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = type;
}
