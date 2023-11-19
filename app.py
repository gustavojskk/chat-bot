from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from filebot import FileBot
from pdf_parser import extrair_texto_do_pdf
import os

app = Flask(__name__)
CORS(app)
file_bot = FileBot()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])  
def ask():
    try:
        user_question = request.form.get('question', '').strip()

        if not user_question:
            return jsonify({'error': 'Por favor, digite algo para o bot responder.'}), 400

        answer = file_bot.answer_question(user_question)

        response = {'answer': answer}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro. Detalhes: {str(e)}'}), 500

@app.route('/train', methods=['POST'])
def train():
    try:
        pdf_path = request.form.get('pdf_path', '').strip()

        if not pdf_path:
            return jsonify({'error': 'Por favor, forneça o caminho de um arquivo PDF para treinar o bot.'}), 400

        pdf_text, pdf_metadata = extrair_texto_do_pdf(pdf_path)
        file_bot.train_with_text(pdf_text)

        return jsonify({'message': 'Treinamento concluído com sucesso.', 'metadata': pdf_metadata})

    except Exception as e:
        logger.exception('Erro durante o treinamento:')
        return jsonify({'error': 'Ocorreu um erro durante o treinamento.'}), 500


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'})

        pdf_file = request.files['pdf_file']

        if pdf_file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'})

        if not allowed_file(pdf_file.filename):
            return jsonify({'error': 'Arquivo PDF inválido'})

        pdf_content = pdf_file.read()  # Lê o conteúdo do arquivo PDF

        pdf_text, pdf_metadata = extrair_texto_do_pdf(pdf_content)

        
        file_bot.train_with_text(pdf_text)

        return jsonify({'message': 'PDF processado com sucesso', 'metadata': pdf_metadata})

    except Exception as e:
        logging.exception('Erro durante o upload e treinamento:')
        return jsonify({'error': 'Erro durante o processamento do PDF'})
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)