
import PyPDF2 as pypdf
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from PIL import Image
from reportlab.lib.colors import white, grey, black, HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch ,cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import textract
import re
import textwrap
import os
import csv
import collections

def get_definitions_dict(input_file): 
    pdf_reader = PdfFileReader(open(input_file, "rb"))
    definitions_dict = {}
    
    for page_counter in range(pdf_reader.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(page_counter))
        with open('{0}.pdf'.format(page_counter), 'wb') as f:
            pdf_writer.write(f)
            f.close()
        text = textract.process('{0}.pdf'.format(page_counter))
        text = text.decode("utf8")

        lines = list(filter(lambda x : x != '', text.split('\n')))

        passed_page_number = 0 
        regex = re.compile('.\..')

        for line in lines: 
            if line.isupper(): #and re.search(r'.\..', row[0]): 
                definitions_dict[line] = ''
        abbreviations_set = {'vs', 'etc', 'est', 'bc' }

        sentences = list(filter(lambda x : x != '', text.split('.')))
        for sentence_index in range(len(sentences) - 1): 
            sentence = sentences[sentence_index]
            words = sentence.split(' ')
            if words[-1] in abbreviations_set or len(words) < 5: 
                sentences[sentence_index+1] = sentence + sentences[sentence_index+1]
            else: 
                for word in words:
                    word = re.sub(r'[^\w\s]', '', word) 
                    if word.upper() in definitions_dict: 
                        if definitions_dict[word.upper()] == '': 
                            if ('Thus' in sentence or 'Because' in sentence) and sentence_index > 0: 
                                sentence = sentences[sentence_index-1] + sentence
                            definitions_dict[word.upper()] = sentence.replace('\n',' ')
                    

    csv_data = []
    for value in definitions_dict: 
        csv_data.append([value, definitions_dict[value]])
    with open("definitions.csv", "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(csv_data)
    
    for file in os.listdir("."):
        if os.path.isfile(file) and file.endswith(".pdf"):
            os.remove(file)
    



def append_definitions(filename):
    pdf_reader = PdfFileReader(open(filename, "rb"))
    pdf_writer1 = PdfFileWriter()
    definitions_dictionary = {}

    with open('definitions_edited.csv', newline='', encoding = "ISO-8859-1") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        for row in csv_reader:
            term = row[0]
            definition = row[1]
            definitions_dictionary[term] = definition
    merger = PdfFileMerger()
    
    for page_counter in range(pdf_reader.getNumPages()):
        page_file_name = f"{page_counter}.pdf"
        with open(page_file_name, 'wb') as intermediate_file:
            pdf_writer1.write(intermediate_file)
        definitions_dictionary = add_local_definitions(filename, page_counter, page_file_name, definitions_dictionary)
        merger.append('processed_' + page_file_name)
    
    merger.write("result.pdf")
    merger.close()
    for file in os.listdir("."):
        if os.path.isfile(file) and file.startswith("processed"):
                try:
                    os.remove(file)
                except e:
                    print(e)




def add_local_definitions(input_file, page_counter, intermediate_file_name, definitions_dict): 
    input1 = PdfFileReader(open(input_file, 'rb')).getPage(page_counter)
    page_length = input1.mediaBox[3]
    page_width = input1.mediaBox[2]
    page_width = float(page_width)
    background_canvas = Canvas("background.pdf", pagesize=(page_width*1.5, page_length))
    background_canvas.setFont("Times-Roman", 12)
    background_canvas.setFillColor(white)
    background_canvas.drawString(1 * inch, 10 * inch, "White text")
    background_canvas.save()

    with open("background.pdf", "rb") as inFile, open(input_file, "rb") as overlay:
        original = pypdf.PdfFileReader(inFile)
        background = original.getPage(0)
        foreground = pypdf.PdfFileReader(overlay).getPage(page_counter)
        background.mergePage(foreground)
        writer = pypdf.PdfFileWriter()
        for i in range(original.getNumPages()):
            page = original.getPage(i)
            writer.addPage(page)

        with open("modified1.pdf", "wb") as outFile:
            writer.write(outFile)
    text = textract.process("modified1.pdf")
    text = text.decode("utf8")

    abbreviations_set = {'vs', 'etc', 'est', 'bc' }

    local_dict = {} 

    text = ''.join(text.splitlines())

    sentences = list(filter(lambda x : x != '', text.split('.')))
    words_queue = collections.deque(3*['0'], 3)
    for sentence_index in range(len(sentences) - 1): 
        sentence = sentences[sentence_index]
        words = sentence.split(' ')
        for word in words: 
            if word != '': 
                words_queue.append(word)
            
            for word_sample in [words_queue[0].upper(), (words_queue[0] + ' ' + words_queue[1]).upper(),(words_queue[0] + ' ' + words_queue[1] + ' ' + words_queue[2]).upper()]: 
                if word_sample in definitions_dict:
                    local_dict[word_sample] = definitions_dict[word_sample]

    insert_canvas = Canvas("insert.pdf", pagesize=(page_width*0.5, page_length))
    insert_canvas.setFillColor(HexColor("#D3D3D3"))
    insert_canvas.rect(5,5,page_width*0.5,page_length,fill=1)
    insert_canvas.setFillColor(black)
    insert_canvas.setFont('Times-Bold',16)
    insert_canvas.drawString(page_width*0.16, page_length - 0.25*inch, "DEFINITIONS")
    lines = 4
    
    for item in local_dict: 
        insert_canvas.setFont("Times-Roman", 12)
        
        textobject = insert_canvas.beginText(10, page_length - (0.17*inch * lines))
        my_text = f"{item} : {local_dict[item]}"
        my_text = textwrap.fill(my_text, 52) + '\n'
        for line in my_text.splitlines(False):
            textobject.textLine(line.rstrip())
        insert_canvas.drawText(textobject)
        lines += my_text.count('\n') + 2 
    insert_canvas.save()

    with open("modified1.pdf", "rb") as inFile, open("insert.pdf", "rb") as overlay:
        original = pypdf.PdfFileReader(inFile)
        background = original.getPage(0)
        foreground = pypdf.PdfFileReader(overlay).getPage(0)

        # merge the first two pages
        background.mergeTranslatedPage(foreground, 620, 0)

        # add all pages to a writer
        writer = pypdf.PdfFileWriter()
        for i in range(original.getNumPages()):
            page = original.getPage(i)
            writer.addPage(page)

        final_name = 'processed_' + intermediate_file_name
        # write everything in the writer to a file
        with open(final_name, "wb") as outFile:
            writer.write(outFile)
    os.remove('background.pdf')
    os.remove('modified1.pdf')
    os.remove('insert.pdf')
    os.remove(intermediate_file_name)
    return definitions_dict

get_definitions_dict('input/chapter.pdf')
x = input("Press any key once the dictionary has been edited")
confirm_next_step = input("Confirm?")
if 'y' in confirm_next_step.lower(): 
    append_definitions('input/chapter.pdf')

def convert_image_to_pdf(input_image_address, destination_name_address):
    image1 = Image.open(input_image_address, 'r')
    im1 = image1.convert('RGB')
    im1.save(destination_name_address, 'r')