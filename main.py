import requests, os, csv
from bs4 import BeautifulSoup as bs

TIMEOUT = 10

START_URL = "http://repository.um-palembang.ac.id/view/subjects/subjects.html"
BASE_URL = "http://repository.um-palembang.ac.id/view/subjects/"

def main():
    with open('data.csv','w', encoding='UTF8') as f:
        writer = csv.writer(f)
        header = 'Name', 'NIM', 'Judul', 'Tipe Item', 'Tahun', 'Additional Information', 'Uncontrolled Keywords', 'Subjects', 'Divisions', 'Depositing User', 'Date Deposited', 'Last Modified', 'URL', 'Document File Names', 'Document Links'
        writer.writerow(header)
        html = requests.get(START_URL, timeout=TIMEOUT).content
        soup = bs(html,'html.parser')
        ep_toolbox_content = soup.find('div', class_='ep_toolbox_content')
        for a in ep_toolbox_content.find_all('a', href=True):
            SUBJECT_URL = BASE_URL+a['href']
            html = requests.get(SUBJECT_URL, timeout=TIMEOUT).content
            soup = bs(html,'html.parser')
            ep_toolbox_content = soup.find('div', class_='ep_toolbox_content')
            #print(a.text, SUBJECT_URL)
            for a in ep_toolbox_content.find_all('a', href=True):
                if a.text == 'Berdasarkan Subyek':
                    continue
                else:
                    SUBJECT_URL = BASE_URL+a['href']
                    #print('\t',a.text, SUBJECT_URL)
                    try:
                        html = requests.get(SUBJECT_URL, timeout=TIMEOUT).content
                        soup = bs(html,'html.parser')
                        ep_view_page = soup.find('div', class_='ep_view_page ep_view_page_view_subjects')
                        for p in ep_view_page.find_all('p'):
                            a = p.find('a', href=True)
                            doc_url = a['href']
                            html = requests.get(doc_url, timeout=TIMEOUT).content
                            soup = bs(html,'html.parser')
                            title = soup.find('h1', class_='ep_tm_pagetitle').text.strip()
                            ep_summary_content_main = soup.find('div', class_='ep_summary_content_main')
                            person_names = ep_summary_content_main.find_all('span', class_='person_name')
                            try:
                                year = ep_summary_content_main.text.split('(')[1].split(')')[0]
                            except:
                                year = 'NA'
                            if len(person_names)==2:
                                name_nim, mahasiswa = person_names
                                try:
                                    name,nim = name_nim.text.split(', NIM ')
                                except:
                                    name = name_nim.text
                                    nim = 'NA'
                            else:
                                r = ''
                                for name in person_names:
                                    r += name.text +" "
                                name = r
                                nim = 'NA'
                            item_type='NA'
                            document_table = soup.find_all('table')[0]
                            ep_document_links = document_table.find_all('a', class_='ep_document_link', href=True)
                            doc_links = ''
                            for ep_document_link in ep_document_links:
                                if 'Download' in ep_document_link.text:
                                    file_size = ep_document_link.text.split('(')[1].split(')')[0]
                                    #print(ep_document_link['href'], file_size)
                                    doc_links += ep_document_link['href']+'\n'
                            doc_links = doc_links.rstrip('\n')
                            doc_filenames = ''
                            for ep_document_citation in soup.find_all('span', class_='ep_document_citation'):
                                if len(ep_document_citation.text.split('\n')) == 4:
                                    _, document_format, document_filename, _ = ep_document_citation.text.split('\n')
                                else:
                                    try:
                                        _, document_format, document_filename, _, _, _, _ = ep_document_citation.text.split('\n') 
                                    except:
                                        document_format, document_filename = '',''                               
                                #print(document_format, document_filename)
                                doc_filenames += document_filename+'\n'
                            doc_filenames = doc_filenames.rstrip('\n')
                            for tr in soup.find_all('tr'):
                                try:
                                    th = tr.find('th')
                                    td = tr.find('td')
                                    if th.text == 'Item Type:':
                                        item_type = td.text.replace(' ','').replace('\n','')
                                    if th.text == 'Additional Information:':
                                        add_info = td.text.replace('\n','')
                                    if th.text == 'Uncontrolled Keywords:':
                                        uncontrolled_keywords = td.text
                                    if th.text == 'Subjects:':
                                        subjects = td.text
                                    if th.text == 'Divisions:':
                                        divisions = td.text
                                    if th.text == 'Depositing User:':
                                        depositing_user = td.text.replace('\n','')
                                    if th.text == 'Date Deposited:':
                                        deposited_date = td.text
                                    if th.text == 'Last Modified:':
                                        last_modified = td.text
                                except:pass
        #                        print(len(person_names),person_names)

                            res = f"""
        Name                    :   {name}
        NIM                     :   {nim}
        Judul                   :   {title}
        Tipe Item               :   {item_type}
        Tahun                   :   {year}
        Additional Information  :   {add_info}
        Uncontrolled Keywords   :   {uncontrolled_keywords}
        Subjects                :   {subjects}
        Divisions               :   {divisions}
        Depositing User         :   {depositing_user}
        Date Deposited          :   {deposited_date}
        Last Modified           :   {last_modified}
        URL                     :   {doc_url}
        Document File Names     :   {doc_filenames}
        Document Links          :   {doc_links}
        """
                            print(res)
                            row = name, nim, title, item_type, year, add_info, uncontrolled_keywords, subjects, divisions, depositing_user, deposited_date, last_modified, doc_url, doc_filenames, doc_links
                            writer.writerow(row)
                    except:pass

if __name__ == '__main__':
    main()