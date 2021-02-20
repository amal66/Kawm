import fitz
doc = fitz.open("CS152_Textbook.pdf")
for i in range(len(doc)):
    for img in doc.getPageImageList(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n < 5:       # this is GRAY or RGB
            pix.writePNG("p%s-%s.png" % (i, xref))
        else:               # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG("p%s-%s.png" % (i, xref))
            pix1 = None
        pix = None

def convert_image_to_pdf(input_image_address, destination_name_address):
    image1 = Image.open(input_image_address, 'r')
    im1 = image1.convert('RGB')
    im1.save(destination_name_address, 'r')