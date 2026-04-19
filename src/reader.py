import pdfplumber
import docx
import io
import logging
import re
import os
import platform
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Detect OS and configure Tesseract path if needed
def _check_tesseract_available():
    """Check if Tesseract OCR is available, return True/False"""
    try:
        pytesseract.get_tesseract_version()
        return True
    except pytesseract.TesseractNotFoundError:
        # Try to find Tesseract in common Windows locations
        if platform.system() == 'Windows':
            common_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            ]
            for path in common_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    try:
                        pytesseract.get_tesseract_version()
                        return True
                    except:
                        continue
        return False
    except Exception:
        return False

def normalize_text(text):
    """
    Normalizes extracted text:
    - Lowercase
    - Strip extra whitespace
    - Remove null characters
    - Strip non-readable characters
    - Safely convert to UTF-8
    """
    if not text:
        return ""
    
    # Ensure text is string (in case bytes slip through)
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')
    
    # Remove null characters and other control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', ' ', text)
    
    # Lowercase and strip
    text = text.lower().strip()
    
    # Replace multiple spaces/newlines with single space
    text = " ".join(text.split())
    
    return text

def extract_text_from_resume(file):
    """
    ROBUST resume text extraction pipeline for PDF, DOCX, PNG, JPG, TXT.
    
    Pipeline:
    - PDF: Try text extraction → if < 300 chars, fallback to OCR
    - DOCX: Extract text + OCR embedded images
    - PNG/JPG: Always use OCR
    - TXT: Read directly
    
    Returns: (normalized_text, warning_message)
    - Never returns empty text unless file is truly unreadable
    - Warnings are non-blocking
    - OCR errors are handled gracefully
    """
    filename = getattr(file, 'filename', getattr(file, 'name', '')).lower()
    text = ""
    warning = None
    tesseract_available = _check_tesseract_available()
    
    logging.info(f"Starting text extraction for file: {filename}")
    
    try:
        # Ensure we're at the start of the file
        if hasattr(file, 'seek'):
            file.seek(0)
        
        # ========== PDF HANDLING ==========
        if filename.endswith('.pdf'):
            text_extracted = False
            
            # Step 1: Try text-based extraction first
            try:
                file.seek(0)
                with pdfplumber.open(file) as pdf:
                    pages_text = []
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            pages_text.append(extracted)
                    text = "\n".join(pages_text)
                    text_extracted = True
                    logging.info(f"PDF text extraction: {len(text)} chars")
            except Exception as e:
                logging.warning(f"PDF text extraction failed: {e}")
                text = ""
            
            # Step 2: If text extraction failed or too short (< 300 chars), try OCR
            if not text_extracted or len(text.strip()) < 300:
                if tesseract_available:
                    try:
                        file.seek(0)
                        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
                        ocr_text = ""
                        for page_num in range(pdf_document.page_count):
                            page = pdf_document[page_num]
                            pix = page.get_pixmap()
                            img_data = pix.tobytes("png")
                            img = Image.open(io.BytesIO(img_data))
                            ocr_text += pytesseract.image_to_string(img) + "\n"
                        pdf_document.close()
                        
                        # Use OCR text if it's better
                        if len(ocr_text.strip()) > len(text.strip()):
                            text = ocr_text
                            logging.info(f"PDF OCR successful: {len(ocr_text)} chars")
                            warning = "Scanned PDF detected. OCR was used - accuracy may be reduced."
                        elif len(text.strip()) < 300:
                            # Use OCR even if shorter, as it might be better quality
                            text = ocr_text if ocr_text.strip() else text
                            warning = "PDF text extraction was limited. OCR was used - accuracy may be reduced."
                    except Exception as ocr_e:
                        logging.warning(f"PDF OCR failed: {ocr_e}")
                        if not text:
                            warning = "Scanned resume detected. Please upload a text-based PDF or DOCX for best results."
                else:
                    # Tesseract not available
                    if not text or len(text.strip()) < 300:
                        warning = "Scanned resume detected. Please upload a text-based PDF or DOCX for best results."
        
        # ========== DOCX HANDLING ==========
        elif filename.endswith('.docx'):
            try:
                file.seek(0)
                doc = docx.Document(file)
                text = "\n".join([p.text for p in doc.paragraphs])
                logging.info(f"DOCX text extraction: {len(text)} chars")
                
                # Try OCR for embedded images (optional enhancement)
                if tesseract_available:
                    try:
                        ocr_text = ""
                        for rel in doc.part.rels.values():
                            if "image" in rel.reltype:
                                image_part = rel.target_part
                                image_data = image_part.blob
                                img = Image.open(io.BytesIO(image_data))
                                page_text = pytesseract.image_to_string(img)
                                ocr_text += page_text + "\n"
                        if ocr_text.strip():
                            text += "\n" + ocr_text
                            logging.info(f"DOCX OCR extracted additional {len(ocr_text)} chars from images")
                    except Exception as e:
                        logging.warning(f"DOCX image OCR failed: {e}")
            except Exception as e:
                logging.error(f"DOCX extraction failed: {e}")
                text = ""
                warning = f"Failed to extract text from DOCX: {str(e)}"
        
        # ========== IMAGE HANDLING (PNG/JPG) ==========
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            if tesseract_available:
                try:
                    file.seek(0)
                    image_bytes = file.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    text = pytesseract.image_to_string(image)
                    logging.info(f"Image OCR extracted {len(text)} chars")
                    warning = "Image resume detected. OCR was used - accuracy may be reduced."
                except Exception as e:
                    logging.error(f"Image OCR failed: {e}")
                    text = ""
                    warning = f"Failed to extract text from image: {str(e)}. Please ensure it's a clear, readable image."
            else:
                # Tesseract not available
                text = ""
                warning = "Scanned resume detected. Please upload a text-based PDF or DOCX for best results."
        
        # ========== TXT HANDLING ==========
        else:
            try:
                file.seek(0)
                content = file.read()
                if isinstance(content, bytes):
                    text = content.decode("utf-8", errors="ignore")
                else:
                    text = str(content)
                logging.info(f"TXT extraction: {len(text)} chars")
            except Exception as e:
                logging.error(f"TXT extraction failed: {e}")
                text = ""
                warning = f"Failed to read text file: {str(e)}"
        
        # ========== TEXT NORMALIZATION ==========
        cleaned_text = normalize_text(text)
        
        # ========== TEXT VALIDATION (NON-BLOCKING) ==========
        # Minimum threshold: 150 characters
        # If text is short, show WARNING (not error) and continue
        if len(cleaned_text) < 150:
            if not warning:
                warning = "Resume text is very short. ATS accuracy may be reduced."
            logging.warning(f"Extracted text very short: {len(cleaned_text)} chars")
        elif len(cleaned_text) < 300:
            logging.info(f"Extracted text somewhat short: {len(cleaned_text)} chars")
        
        # NEVER return empty text unless file is truly unreadable
        # If we have any text, use it (even if short)
        if cleaned_text:
            logging.info(f"Successfully extracted {len(cleaned_text)} chars from {filename}")
            return cleaned_text, warning
        else:
            # Only return empty if we truly couldn't extract anything
            logging.error(f"Failed to extract any text from {filename}")
            return "", warning or "Could not extract text from resume. Please try a different file format."
        
    except Exception as e:
        logging.error(f"Error parsing resume {filename}: {str(e)}", exc_info=True)
        # Return any partial text we might have, with warning
        partial_text = normalize_text(text) if text else ""
        return partial_text, f"Resume parsing encountered issues: {str(e)}. Results may be incomplete."

# Alias for backward compatibility with app.py
read_resume = extract_text_from_resume