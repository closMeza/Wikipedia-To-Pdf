# Wikipedia to pdf script
# Author: Carlos Meza
# Desctription: This script is able to pull all html and corressponding text and place it into defualtdic
# Requirements: Need NotoSans on your systems Font file

from collections import defaultdict
from bs4 import BeautifulSoup
from fpdf import FPDF
import urllib.request
import re
import fpdf 

#places dict into pdf file utilizies FPDF module can be optimized to output any file name
def dict_to_pdf(dict):
    pdf = FPDF()
    pdf.add_font("NotoSans", style="", fname= r"C:\WINDOWS\Fonts\NotoSans-Regular.ttf", uni=True) #adds utf-8 font family that allows chars past latin-1
    pdf.add_font("NotoSans-Bold", style="", fname= r"C:\WINDOWS\Fonts\NotoSans-Bold.ttf", uni=True) #adds utf-8 font family that allows chars past latin-1
    pdf.add_page()
    hdr_size = 20
    pr_size = 12
    #main logic to place dict into pdf
    for headers in dict:
        #prints Headers first then corresonding paragraphs
        hdr_str = headers
        pdf.set_font("NotoSans-Bold", style='' ,size = hdr_size)
        pdf.multi_cell(200, 10 , txt=hdr_str, align='L')
        for para in dict[headers]:
            if para == '\n':
                continue
            para_str = para + '\n'
            pdf.set_font("NotoSans", size = pr_size)
            pdf.multi_cell(200, 5, txt=para_str, align='L')
            
    pdf.output("Mac_Miller.pdf")
    

if __name__ == '__main__':

    #data
    web_page_info = defaultdict(list)

    #opens url and pulls html data
    web_url = urllib.request.urlopen('https://en.wikipedia.org/wiki/Mac_Miller')
    data = web_url.read()
    soup = BeautifulSoup(data, 'html.parser')

    #places first header into dict
    first_h = soup.find('h1', {'id:','firstHeading'})
    cnt_text = soup.find('div', {'class:', 'hatnote navigation-not-searchable'})
    for p in cnt_text.next_siblings:
        if p.name and p.name.startswith('h'):
            break
        if p.name == 'p':
            web_page_info[first_h.text].append(p.text)
        

    #for loops through all headers
    for h in soup.find_all(re.compile('^h[1-6]$')): #soup.find_all('h1', {'id': 'firstHeading'}) + soup.find_all('span', {'class': 'mw-headline'}):
        for tmp in h.next_siblings:
            if tmp.name and tmp.name.startswith('h'):
                break
            if tmp.name == 'p':
                web_page_info[h.text].append(tmp.text)

        
    dict_to_pdf(web_page_info)   

    #prints dict
    for header, para in web_page_info.items():
        print(header, "\n", para)

'''
   
    #things that worked but not as intended for this project
    #places header and correlated paragraphs into a dict with header as key
    for headers in soup.find_all(re.compile('^h[1-6]$')):
        html = headers.nextSibling
        while html is not None and html.name != ("h1" or "h2" or "h3" or "h4" or "h5" or "h6"):
            if html.name == "p":
                web_page_info[headers.text].append(html.text)
            html = html.nextSibling



            
        #hdr_str = hdr_str.encode('latin-1', 'replace').decode('utf-8','replace')
        #hdr_str = hdr_str.replace('?', '-') #replaces characters if they occur used for timelines ex) 2001 - 2002
         
        #pdf.cell(0,10, txt='\n', ln=2)
        para_str = para + '\n'
        #para_str.encode('latin-1', 'replace').decode('utf-8','replace')
'''
