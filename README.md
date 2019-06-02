# TableExtraction
A solution to extract tabular data from PDF and Image Files

## Installation and Setup

### NOTE : Python2 environment

Install Requirements
```
pip install -r requirements.txt
```
Run flask app (server)
```
sudo python app.py
```
Web app - Open webapp/home.html in browser

## PDF Module - Extracting tables from PDF

### Step 1: Loading the PDF using pyPDF module

Using pyPDF module, the number of pages present inside the PDF is extracted for further iteration

*Follow the commands below to cd into data directory and convert image to searchable pdf.*

```
    cd TableExtraction/PDF Module/
    python table_extract.py 
```
Then the programme displays a prompt as shown below to enter the name of PDF file. 
### Note: Just Enter the Name of the file (without the ".pdf" extension) 

```
    Enter the pdf you want to extract the table --> 006  
```
The above line loads the 015.pdf file from the dataset and extracts the table content out of it.

### Step 1: Page segmentation and data logging using pyPDF module

Now, all the pages present in the pdf are segmented individually with the name ``` Page_0.pdf ```, ``` Page_1.pdf ``` , so on upto the last page of the pdf. Advantages of Page Segmentation is that,

1. Boosts the speed of algorithm by reducing the file size.
2. Reduces Spurious inputs to algorithm.
3. Enables to recognise the exact location of table.

**Sample Page Segmentation view**

![image](https://drive.google.com/uc?export=view&id=1bgM2aXnMoRnO-EfRv-c-2xGAD2WE7dyY)

### Step 2: Iterating and extracting tables from all PDF's using tabula-py

Tabula-py is a python library which is written upon the java. It uses python commands to recieve the arguments and invoke the ``` .jar ``` files in order to find the tables in a pdf.

```
    for i in range(0,pag_no): 
        convert_into('Page_'+str(i)+'.pdf', 'result_'+str(i)+'.csv', output_format = 'CSV')
        convert_into('Page_'+str(i)+'.pdf', 'result_'+str(i)+'.xml', output_format = 'xml')
``` 
 
The above code is used to iterate over all the ``` Page_.pdf ``` files to extract the table data.

### Step 3: Output data logging and Visualisation
The tables extracted are stored in the  ``` .CSV ```  format, which enables the user to directly access the tables in pdf's without manual entry.

```    results_0.csv 
       results_1.csv
       results_2.csv 
       ......
```    
The above shown is the format of output result logging which contains the table information. The found tables in the pdf are shown in the following format 

```
    Table found in -----> PAGE3 and stored in -----> result_0.csv
``` 

### Step 4: Complete sample Output

PDF file with table in it's 3rd Page.

![image](https://drive.google.com/uc?export=view&id=1yU2iDmcxB4ULMq07qstO71qZsd9mXjB7) 

Image of result extracted with the Table Information into the CSV file.

![image](https://drive.google.com/uc?export=view&id=1V3-rMcZffvQZHSR13A3C40DwefsSN5YV)

### Advantages of PDF Module: 
1. No Preprocesssing of PDF's is required.
2. Faster processing due to Page segmentation technique.
3. Higher Accuracy to even noisy pages. 
4. Better ROI(Region of Interest) extraction and higher text rejection rate. 

### OUTPUT
*Generated output CSV files in PDF Module/pdfname*




## Image Module - Extracting table data from Images

### Step 1: Generate Searchable PDF from image using OCR

Using tesseract for OCR on input image to produce a sandwich pdf with existing image and extracted OCR data

*Follow the commands below to cd into data directory and convert image to searchable pdf.*

```
    cd TableExtraction/Image Module/data
    tesseract 29.jpg 29 -l eng pdf
```
 **Sample Searchable PDF**
 ![image](https://drive.google.com/uc?export=view&id=1e2PiOngGV4LMGGufCvqQS-ISXb7tWrOv)
 
 ### Step 2: Generate XML from Searchable PDF
```
    pdftohtml -c -hidden -xml 29.pdf 29.xml
```
*Find sample XML in Image/data folder*

 ### Step 3: Cluster lines in Image and generate CSV
```
  python extract.py
```
**Sample Line Clustering**
![image](https://drive.google.com/uc?export=view&id=10lRnS1XB9G_E1yLxORPSK7h1MK9X8KGQ)

### OUTPUT
*Generated output images and CSV files in Image/generated_output folder*
