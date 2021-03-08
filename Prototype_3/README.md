
# Prototype 3
The purpose of this prototype is to enable user testing of the hypotheses underlying the resource embedding and moving dictionary features for the final product. It works by scraping textbooks for definitions and images, allowing users to modify the positioning of these definitions and images, and creating a final pdf that contains the moving dictionary. This moving dictionary can then be uploaded in the Perusall platform to allow embedding of resources. With this combination, user testing and experimentation can be conducted on both the moving dictionary and resource embedding features.

Currently, the definitions scraping function is optimized to work for pdfs published by Pearson. However, by editing the csv that is created from the definitions scraping function, users can create the dictionary feature for any pdf file. 

## Running the program
1. Put the PDF textbook in the input folder
2. Run page_modifications.py
3. After the first part of page_modifications.py is run, definitions.csv will be created and the program will pause and wait for user input. Modify definitions.csv for accuracy and save as definitions_edited.csv. For convenience, an edited definitions_edited file is included as definitions_edited copy.csv. Copy and rename this file to definitions_edited.csv
4. Type "Yes" in response to the program and the program will continue running to create the final pdf, which will be returned as result.pdf. 
5. Upload result.pdf onto your Perusall instructor account, and share with target users. 