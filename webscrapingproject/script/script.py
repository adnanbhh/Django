import time

from webdriver_manager.chrome import ChromeDriverManager


def pubmed(term):
    import pymongo
    from selenium import webdriver
    import time


    #url to be scraped
    for i in range(1,5):
        pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/?term="+term+"&page="+str(i)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(pubmed_url)
    #collect new titles from pubmed

        time.sleep(1)
        d = []
        title = driver.find_elements_by_class_name("docsum-title")
        for i in range(len(title)):
            title_dict = {}
            title_dict['title'] = title[i].text
            d.append(title_dict)

        a = []
        author = driver.find_elements_by_class_name("full-authors")
        for i in range(len(author)):
            author_dict = {}
            author_dict['author'] = author[i].text
            a.append(author_dict)

        j = []
        journal = driver.find_elements_by_class_name("full-journal-citation")
        for i in range(len(journal)):
            journal_dict = {}
            journal_dict['journal'] = journal[i].text
            j.append(journal_dict)

        pm = []
        pmid = driver.find_elements_by_class_name("docsum-pmid")
        for i in range(len(pmid)):
            pmid_dict = {}
            pmid_dict['pmid'] = pmid[i].text
            pm.append(pmid_dict)

        driver.close()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["pubmed"]
        mycol = mydb[term]
        for i in range(len(title)):
            pubmed = {
                "title": d[i],
                "authors": a[i],
                "journal": j[i],
                "PMID": pm[i],
            }
            mycol.insert_one(pubmed)

def espacenet(term):

    import pymongo
    from selenium import webdriver
    import time


    # url to be scraped
    espacenet_url = "https://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=singleline&query=" + term

    # collect new titles from pubmed
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(espacenet_url)

    time.sleep(5)
    zz = []
    link = driver.find_elements_by_class_name("publicationLinkClass")
    for i in range(len(link)):
        link_dict = {}
        link_dict['link'] = link[i].get_attribute('href')
        zz.append(link_dict)

    d = []
    title = driver.find_elements_by_class_name("publicationLinkClass")
    for i in range(len(title)):
        title_dict = {}
        title_dict['title'] = title[i].text
        d.append(title_dict)

    IN = []
    inventor = driver.find_elements_by_class_name("inventorColumn")
    for i in range(len(inventor)):
        inventor_dict = {}
        inventor_dict['inventor'] = inventor[i].text
        IN.append(inventor_dict)

    ap = []
    applicant = driver.find_elements_by_class_name("applicantColumn")
    for i in range(len(applicant)):
        applicant_dict = {}
        applicant_dict['applicant'] = applicant[i].text
        ap.append(applicant_dict)

    cpc = []
    CPC = driver.find_elements_by_class_name("cpcColumn")
    for i in range(len(CPC)):
        CPC_dict = {}
        CPC_dict['CPC'] = CPC[i].text
        cpc.append(CPC_dict)

    ipc = []
    IPC = driver.find_elements_by_class_name("ipcColumn")
    for i in range(len(IPC)):
        IPC_dict = {}
        IPC_dict['IPC'] = IPC[i].text
        ipc.append(IPC_dict)

    pb = []
    publication_info = driver.find_elements_by_class_name("publicationInfoColumn")
    for i in range(len(publication_info)):
        publication_info_dict = {}
        publication_info_dict['publication info'] = publication_info[i].text
        pb.append(publication_info_dict)

    pd = []
    priority_date = driver.find_elements_by_class_name("nowrap")
    for i in range(len(priority_date)):
        priority_date_dict = {}
        priority_date_dict['priority date'] = priority_date[i].text
        pd.append(priority_date_dict)

    driver.close()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["espacenet"]
    mycol = mydb[term]

    for i in range(len(title)):
        espacenet = {
            "link": zz[i],
            "title": d[i],
            "inventor": IN[i],
            "applicant": ap[i],
            "CPC": cpc[i],
            "IPC": ipc[i],
            "publication info": pb[i],
            "priority date": pd[i],
        }
        mycol.insert_one(espacenet)

def scopus(term):


    import pymongo
    from selenium import webdriver
    import time


    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get("https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D723f8bda4be8d03a90d37a5f1e445a26&state=forceLogin%7CtxId%3D343759EFCEF0AA9D5E93AEB9A8B1A82A.i-04f6af96501b6f883%3A5&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS")
    driver.find_element_by_xpath("/html/body/div/section/main/form/div[3]/div[2]/button").click()
    driver.find_element_by_xpath("/html/body/div/section/main/div[2]/div[2]/div/form/div[1]/input").send_keys("@@email")
    driver.find_element_by_xpath("/html/body/div/section/main/div[2]/div[2]/div/form/div[3]/div/button").click()
    driver.find_element_by_xpath("/html/body/div/section/main/form/div[2]/div[2]/input").send_keys("@@password")
    driver.find_element_by_xpath("/html/body/div/section/main/form/div[3]/div[2]/button").click()
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/micro-ui/scopus-homepage/div/div/els-tab/els-tab-panel[1]/div/form/div[1]/div/div[2]/els-input/div/label/input").send_keys(term)

    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/micro-ui/scopus-homepage/div/div/els-tab/els-tab-panel[1]/div/form/div[2]/div[2]/button").click()
    # url to be scraped
    scopus_url = "https://www.scopus.com/results/results.uri?sid=a79efacd2d76adb4647cff9908724ada&src=s&sot=b&sdt=b&origin=searchbasic&rr=&sl=19&s=TITLE-ABS-KEY("+term+")&searchterm1=data&searchTerms=&connectors=&field1=TITLE_ABS_KEY&fields="

    # collect new titles from pubmed
    time.sleep(4)

    driver.get(scopus_url)

    time.sleep(5)
    zz = []
    link = driver.find_elements_by_class_name("ddmDocTitle")
    for i in range(len(link)):
        link_dict = {}
        link_dict['link'] = link[i].get_attribute('href')
        zz.append(link_dict)

    d = []
    title = driver.find_elements_by_class_name("ddmDocTitle")
    for i in range(len(title)):
        title_dict = {}
        title_dict['title'] = title[i].text
        d.append(title_dict)

    au = []
    author = driver.find_elements_by_class_name("ddmAuthorList")
    for i in range(len(author)):
        author_dict = {}
        author_dict['author'] = author[i].text
        au.append(author_dict)

    y = []
    year = driver.find_elements_by_class_name("ddmPubYr")
    for i in range(len(year)):
        year_dict = {}
        year_dict['year'] = year[i].text
        y.append(year_dict)

    src = []
    source = driver.find_elements_by_class_name("ddmDocSource")
    for i in range(len(source)):
        source_dict = {}
        source_dict['source'] = source[i].text
        src.append(source_dict)

    j = 2
    ab = []
    abstract = driver.find_elements_by_class_name("dropdownContentWrap")
    try:
        for i in range(len(abstract)):
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[1]/div[1]/div/div[3]/form/div[4]/div[2]/div/div/section[1]/div/div[3]/table/tbody/tr[" + str(
                    j) + "]/td/ul/li[1]/span/a/span[1]").click()
            j = j + 3
            if j == 59:
                break
        time.sleep(3)
    except Exception as e:
        return e

    for i in range(len(abstract)):
        abstract_dict = {}
        abstract_dict['abstract'] = abstract[i].text
        ab.append(abstract_dict)

    driver.close()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["scopus"]
    mycol = mydb[term]
    try:
        for i in range(len(title)):
            scopus = {
                "link": zz[i],
                "title": d[i],
                "authors": au[i],
                "year": y[i],
                "source": src[i],
                "abstract": ab[i],

            }
            mycol.insert_one(scopus)
    except Exception as e:
        return e

def IEEE(term):
    from selenium import webdriver
    from pymongo import MongoClient
    import numpy as np
    import pandas as pd
    import time

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://ieeexplore.ieee.org/Xplore/home.jsp')  # put here the adress of your page
    time.sleep(3)
    InputElement = driver.find_element_by_xpath(
        '/html/body/div[5]/div/div/div/div[3]/div/xpl-root/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[1]/xpl-typeahead-migr/div/input')
    InputElement.send_keys(term)
    btnSearch = driver.find_element_by_xpath(
        '/html/body/div[5]/div/div/div/div[3]/div/xpl-root/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[2]/button')
    btnSearch.click()
    time.sleep(6)

    BtnExport = driver.find_element_by_xpath(
        '/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[1]/div[1]/ul/li[2]/xpl-export-search-results/button')
    BtnExport.click()
    time.sleep(6)
    BtnDownload = driver.find_element_by_xpath(
        "/html/body/div[5]/div/div/div/div[3]/div/xpl-root/div/xpl-search-results/main/div[1]/div[1]/ul/li[2]/xpl-export-search-results/ngb-tooltip-window/div[2]/div/div/div/div/div/button")
    BtnDownload.click()
    time.sleep(60)

    driver.get('chrome://downloads')
    time.sleep(6)

    TitleCSV = driver.execute_script(
        "return document.querySelector('body > downloads-manager').shadowRoot.querySelector('#frb0').shadowRoot.querySelector('#file-link').text")
    print(TitleCSV)
    csv_path = '/Users/hp/Downloads/'+TitleCSV+''
    print(csv_path)
    db_name = "IEEE"
    coll_name = term
    db_url = 'localhost'
    db_port = 27017
    client = MongoClient(db_url, db_port)
    db = client[db_name]
    coll = db[coll_name]
    df = pd.read_csv(csv_path, error_bad_lines=False)
    dfc = df.replace(np.nan, "null", regex=True)
    data = dfc.to_dict(orient="records")
    db.ieeExport.insert_many(data)
def google(term):
    pass
def wikipedia(term):
    pass
def uptdo(term):
    pass
