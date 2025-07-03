from apps.exam.models import Exam
from apps.question.models import Question
from django.utils.html import escape
import qrcode
from io import BytesIO
import base64

class ExamHTMLService:
    @staticmethod
    def generate_html_exam(exam: Exam):
        questions_html = ""
        option_letters = ['a', 'b', 'c', 'd', 'e']

        for index, question in enumerate(exam.questions.all(), start=1):
            questions_html += '<div class="question">\n'
            questions_html += f'<div class="question-text">{index}. {escape(question.title)}</div>\n'
            
            if question.type == 'MC':
                questions_html += '<div class="options">\n'
                for alt_index, alt in enumerate(question.options):
                    letter = option_letters[alt_index]
                    questions_html += f'''
                        <div class="option">
                            <span class="option-letter">{letter})</span> <label>{escape(alt)}</label>
                        </div>
                    '''
                questions_html += '</div>\n'

            elif question.type == 'TF':
                questions_html += '''
                    <div class="options true-false">
                        <div class="option">
                            <span class="checkbox"></span> <label>Verdadeiro</label>
                        </div>
                        <div class="option">
                            <span class="checkbox"></span> <label>Falso</label>
                        </div>
                    </div>
                '''
            elif question.type == 'ES':
                questions_html += f'''
                    <div class="options essay">
                    </div>
                '''


            questions_html += '</div>\n'
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(exam.qr_code)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>{exam.title}</title>
            <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .container-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
                border: 1px solid #000;
                padding: 15px;
            }}
            .student-info div {{
                display: flex;
                gap: 8px;
                flex-direction: column;
                margin-bottom: 10px;
            }}
            .question {{
                margin-bottom: 25px;
                page-break-inside: avoid;
            }}
            .question-text {{
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .options {{
                margin-left: 20px;
            }}
            .option {{
                margin-bottom: 5px;
            }}
            .true-false {{
                display: flex;
                gap: 20px;
            }}
            .essay {{
                margin-bottom: 124px;
            }}
            .section-title {{
                font-size: 1.2em;
                font-weight: bold;
                margin: 20px 0 10px 0;
                border-bottom: 1px solid #000;
                padding-bottom: 5px;
            }}
            .checkbox {{
                display: inline-block;
                width: 16px;
                height: 16px;
                border: 1px solid #000;
                margin-right: 5px;
                margin-left: 16px;
                vertical-align: middle;
            }}
            @media print {{
                .no-print {{
                    display: none;
                }}
                body {{
                    padding: 0;
                }}
            }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{exam.title}</h1>
            </div>

            <div class="container-header">
                <div class="student-info">
                    <div>
                        <label for="student-name">Nome: </label>
                        <input
                            type="text"
                            id="student-name"
                            style="width: 500px; border: none; border-bottom: 1px solid #000"
                        />
                    </div>
                    <div>
                        <label for="student-id">Matrícula: </label>
                        <input
                            type="text"
                            id="student-id"
                            style="width: 300px; border: none; border-bottom: 1px solid #000"
                        />
                    </div>
                    <div>
                        <label for="date">Data: </label>
                        <input
                            type="text"
                            id="date"
                            style="width: 200px; border: none; border-bottom: 1px solid #000"
                        />
                    </div>
                </div>
                <img src="data:image/png;base64,{qr_code_base64}" alt="QR Code" style="width: 200px; height: auto;" />
            </div>

            {questions_html}
        </body>
        </html>
        """

        return html_content
