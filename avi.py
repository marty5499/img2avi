import requests, json, time, cv2, os, sys

class AVI:
    def download(imgFolder,fileId,date):
        urlPrefix = 'https://drive.google.com/uc?export=view&id='
        url = urlPrefix + fileId
        filename = date.replace('T',' ')[:-5]
        savePath = imgFolder+filename+".jpg"
        f = open(savePath,'wb')
        print("URL:",url)
        response = requests.get(url)
        f.write(response.content)
        f.close()

    def getFilesInfo(folderId):
        script = 'https://script.google.com/macros/s/AKfycbwk7UkYhW9A-vJluivlBdaPOPhxREDYsFT1-29tCYiBauAp_6UcwKluJAZPzZ4ThFiyiw/exec?fid='+folderId
        url = requests.get(script)
        return json.loads(url.text)['result']['fileList']

    def downloadFolder(folderId):
        filesInfo = AVI.getFilesInfo(folderId)
        count = filesInfo['count']
        files = filesInfo['files']
        print('total:',count)
        idx = 0
        for file in files:
            idx = idx +1
            print('download..',file['name'],file['id'],str(idx)+"/"+str(count))
            AVI.download("./"+folderId+"/",file['id'],file['date'])

    def toAVI(imgFolder,aviFile,fps=3):
        filelist = os.listdir(imgFolder)
        filelist.sort(key = str.lower)
        print("-=-=-=-=-=-")
        print("convert folder:",imgFolder," to ",aviFile,' , fps=',fps)
        print('convert...Total:',len(filelist))
        print("-=-=-=-=-=-")
        """ """
        size = (1600, 1200) #需要轉為視訊的圖片的尺寸
        # link https://kknews.cc/zh-tw/code/5p8g2j3.html
        video = cv2.VideoWriter(aviFile, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
        font = cv2.FONT_HERSHEY_SIMPLEX
        for item in filelist:
            if item.endswith('.jpg'):
            # 找到路徑中所有後綴名為.png的檔案，可以更換為.jpg或其它
                item = imgFolder + item
                print("item:",item)
                date = item[8:-4].split()
                str1 = date[0].replace('_','/')
                str2 = date[1].replace('_',':')
                text = str("2022/"+str1+" "+str2)
                img = cv2.imread(item)
                img = cv2.putText(img,text,(20,70),font,1,(0,255,255),2,cv2.LINE_AA)
                #img = cv2.resize(img,size)
                video.write(img)
        video.release()
        cv2.destroyAllWindows()

# 公司示範場域
id01 = '1MdB-TW4gQySkAX8LmVysdEheD-Gil79L'
# 公司示範場域 (吃電池)
id02 = '1oaJx5OUOK8FekcANGgr972thFjm-AFrv'
# 中庭
id03 = '14FQ5ICGN9i96EpGlbAABwiiRRKMe8ls3'
# 客廳
id04 = '1HajUgrVmrG7Avo7mL2qFgmI_1HlLJeHc'
"""
folderId = imgFolder = id04
try:
    os.mkdir(folderId)
except:
    pass
#AVI.downloadFolder(folderId)
#AVI.toAVI(imgFolder,"test.avi")
"""
if(len(sys.argv)==1):
    print("python avi.py ${folder}")
else:
    folder = str(sys.argv[1])
    print('folder:', folder)
    AVI.toAVI("./"+folder+"/","./"+folder+".avi",fps=3)
