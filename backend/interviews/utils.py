"""
Utility functions for audio transcription and PDF generation
"""
import os
import tempfile
from django.core.files import File
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def transcribe_audio(audio_file):
    """
    Transcribe audio file to text using speech recognition
    
    Currently using Google Speech Recognition (free)
    For production, consider using:
    - Google Cloud Speech-to-Text
    - AWS Transcribe
    - Azure Speech Services
    - AssemblyAI
    """
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
        
        try:
            # Load audio file
            with sr.AudioFile(tmp_file_path) as source:
                audio_data = recognizer.record(source)
            
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            
            return text
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
    
    except ImportError:
        logger.error("speech_recognition library not installed")
        raise Exception("Speech recognition library not available. Please install: pip install SpeechRecognition pydub")
    
    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand audio")
        raise Exception("Could not understand audio")
    
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service: {e}")
        raise Exception("Speech recognition service error")
    
    except Exception as e:
        logger.error(f"Error in audio transcription: {str(e)}")
        raise Exception(f"Transcription error: {str(e)}")

def generate_pdf_report(session):
    """
    Generate a PDF report for an interview session
    
    Args:
        session: InterviewSession instance
    
    Returns:
        File object containing the generated PDF
    """
    try:
        # Create a BytesIO buffer
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            bold=True,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            bold=True,
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
        )
        
        # Add title
        title = Paragraph(f"<b>Interview Report</b>", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Add session information
        session_info_data = [
            ['Interview Title:', session.title],
            ['Student Name:', session.student.name],
            ['Student Email:', session.student.email],
            ['Interviewer:', session.interviewer.name],
            ['Date:', session.scheduled_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Duration:', f"{session.duration_minutes} minutes"],
            ['Status:', session.status.upper()],
        ]
        
        if session.started_at:
            session_info_data.append(['Started At:', session.started_at.strftime('%Y-%m-%d %H:%M:%S')])
        
        if session.ended_at:
            session_info_data.append(['Ended At:', session.ended_at.strftime('%Y-%m-%d %H:%M:%S')])
        
        session_table = Table(session_info_data, colWidths=[2*inch, 4*inch])
        session_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ]))
        
        elements.append(session_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Add conversation section
        heading = Paragraph("<b>Interview Conversation</b>", heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Get all conversations
        conversations = session.conversations.all().order_by('timestamp')
        
        if conversations.exists():
            for conv in conversations:
                speaker_label = "AI Interviewer" if conv.speaker == 'ai' else "Student"
                
                # Create conversation entry
                conv_data = [
                    [
                        Paragraph(f"<b>{speaker_label}</b>", normal_style),
                        Paragraph(f"<i>{conv.timestamp.strftime('%H:%M:%S')}</i>", normal_style)
                    ],
                    [
                        Paragraph(conv.message, normal_style),
                        ''
                    ]
                ]
                
                conv_table = Table(conv_data, colWidths=[5*inch, 1.5*inch])
                
                # Different styling for AI and Student
                bg_color = colors.HexColor('#e3f2fd') if conv.speaker == 'ai' else colors.HexColor('#f5f5f5')
                
                conv_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), bg_color),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
                ]))
                
                elements.append(conv_table)
                elements.append(Spacer(1, 0.1 * inch))
        else:
            no_conv_text = Paragraph("<i>No conversation recorded</i>", normal_style)
            elements.append(no_conv_text)
        
        elements.append(Spacer(1, 0.2 * inch))
        
        # Add questions section
        heading = Paragraph("<b>Interview Questions</b>", heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 0.1 * inch))
        
        questions = session.questions.all().order_by('order')
        
        if questions.exists():
            for i, question in enumerate(questions, 1):
                q_text = Paragraph(f"<b>Q{i}:</b> {question.question_text}", normal_style)
                elements.append(q_text)
                
                if question.category:
                    category_text = Paragraph(f"<i>Category: {question.category}</i>", normal_style)
                    elements.append(category_text)
                
                if question.difficulty:
                    difficulty_text = Paragraph(f"<i>Difficulty: {question.difficulty.upper()}</i>", normal_style)
                    elements.append(difficulty_text)
                
                elements.append(Spacer(1, 0.1 * inch))
        else:
            no_q_text = Paragraph("<i>No questions configured</i>", normal_style)
            elements.append(no_q_text)
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Create a Django File object
        filename = f"interview_report_{session.session_id}.pdf"
        pdf_file = ContentFile(pdf_content, name=filename)
        
        return pdf_file
    
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        raise Exception(f"PDF generation error: {str(e)}")
