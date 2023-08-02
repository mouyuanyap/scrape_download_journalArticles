import scrapy
import requests,re
import json,pprint,codecs
import w3lib.html
import time,os
import undetected_chromedriver as uc
import glob
header = {'User-Agent':'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
# cookies = {'_uetsid': '8486f4608fe511edb17adb1ba4d04c54',
#             'user.uuid': '"c23ef31e-ba5f-40b4-aac9-5589e8c04651"',
#             'sncc':'P=17:V=17.0.0&C=C01,C02,C03,C04&D=true',
#             'trackid':'"fggmwwbgjyvznd9zlyfwj7bnn"',
#             'idp_session':'sVERSION_171fb0e67-e97d-4cd3-a472-fe9c959ac0f0',
#             "sim-inst-token":'"1::1673301090811:c5d698df"',
#             "idp_session_http": 'hVERSION_17294c026-2133-42db-8485-b24f67447a3d'
#             }

wd = uc.Chrome()

volume = 120
no_issue= 2
issues  = [i+1 for i in range(no_issue)]
baseurl = 'https://www.pnas.org/toc/pnas/'
urlDownload = 'https://www.pnas.org/'
for issue in issues:
    r = requests.get(baseurl + str(volume) + '/' + str(issue), headers= header, timeout=10)
    r.raise_for_status()
    # print(r.text)
    file = codecs.open("./webPageText.txt", 'w',encoding= "UTF-8")
    file.write(r.text)
    response = scrapy.Selector(text=r.text)
    
    article_type = response.xpath('//span[@class="card__meta__type"]').extract()
    article_type_text = [re.findall(r'<span class="card__meta__type">(.*?)</span>',at)[0] for i,at in enumerate(article_type)]
    article_name = response.xpath('//h3[@class="article-title card__title"]').extract()
    article_name_text = [re.findall(r'<h3 class="article-title card__title"><a class="text-reset animation-underline".*?title="(.*?)"',an)[0] for i,an in enumerate(article_name) if article_type_text[i]=="Research Article"]
    article_footer = response.xpath('//div[@class="card-footer card__footer"]').extract()
    article_link_text = ['https://www.pnas.org'+re.findall(r'<a title="PDF" data-toggle="tooltip" role="button" class="btn btn-bookmark" data-original-title="title" href="(.*?)">',af)[0].replace('epdf','pdf') for i,af in enumerate(article_footer) if article_type_text[i]=="Research Article"]

    # print(article_type_text)
    print(len(article_type_text))
    print(article_name_text[-2])
    print(len(article_name_text))
    print(article_link_text[-2])
    print(len(article_link_text))
    if not os.path.exists('/Users/mouyuanyap/Downloads/' +"./Vol{}Issue{}".format(volume,no_issue)):
        os.mkdir('/Users/mouyuanyap/Downloads/' +"./Vol{}Issue{}".format(volume,no_issue))
    for a,x in enumerate(article_type_text):
        
        print(article_name_text[a])
        print(article_link_text[a])
        wd.get(article_link_text[a]+'?download=true')
        time.sleep(10)
        # r = requests.get(article_link_text[a], headers= header, timeout=10)
        # folder = glob.glob(os.path.join('/Users/mouyuanyap/Downloads',"*"))
        # latest_file = max(folder, key=os.path.getctime)
        # bad_letter =['/','\\',':','*','?','\"','<','>','|']
        # name = article_name_text[a]
        # for aa in bad_letter:
        #     name = name.replace(aa,',')
        
        # print(latest_file)
        # print(name)
        # os.rename(latest_file,os.path.join('/Users/mouyuanyap/Downloads/' +"Vol{}Issue{}/".format(volume,no_issue)+name+".pdf"))
        
        # print(r.content)
        # f.write(r.content)
    # for article in response.xpath('//span[@class="card__meta__type"]'):
    
        
    
    # for i in a[0]:
    #     try:
    #         pl = re.findall(r'<a href="(.*?)"',i)[0]
    #         pn = re.findall(r'>(.*?)</a>',i)[0]
    #     except:
    #         print("error")
    #         continue
    #     paperLink.append(pl)
    #     paperName.append(pn)
    #     paperCode = pl[len("https://link.springer.com/article/"):]
    #     plk = "https://link.springer.com/content/pdf/{}.pdf?pdf=button".format(paperCode)
    #     # print(plk)
    #     pdfLink.append(plk)
    #     time.sleep(0.5)
        
    # if not os.path.exists("./Vol{}Issue{}".format(volume,issue)):
    #     os.mkdir("./Vol{}Issue{}".format(volume,issue))
    # for pL,pN in enumerate(paperName):
    #     ppN =  re.sub(r'[\\/*?:"<>|]',"",pN)
    #     with open("./Vol{}Issue{}/{}.pdf".format(volume,issue,ppN), 'wb')as f:
    #         print(ppN)
    #         print(pdfLink[pL])
    #         r = requests.get(pdfLink[pL], headers= header,cookies = cookies, timeout=10)
    #         time.sleep(2)
    #         f.write(r.content)