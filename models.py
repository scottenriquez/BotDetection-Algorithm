import praw, operator, string, csv, numpy as np
from nltk.corpus import stopwords 

np.random.seed(1)

r = praw.Reddit(
    client_id='QMGJWHgnQGIJNA',
    client_secret='Vq5vDuub6xb_ik8jzOsm33Wpl5M',
    password='1lafot12',
    username='doggobotbotbot',
    user_agent='Smiles all around!'
    )
 


blacklisted = ['askouija', 'test', 'freekarma4you'] #Subreddits where people engage in bot-like behavior

def scrapeTrain():
    all_users = list(set(open('/Users/Account1/Desktop/GitHubProjs/BotDetection/Train/humansnew.txt').read().split('\n')))
    all_data = []

    for user in all_users:
        print(user)
        try:
            all_data.append([0] + list(User(user).__dict__.values()))
        except Exception as e:
            print(str(e))
            continue 

        with open('/Users/Account1/Desktop/GitHubProjs/BotDetection/data2.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(all_data) 


def botInName(user):
    return 1 if 'bot' in str(user).lower() else 0.01

def getSpread(user, comlist):
    subsList = []
    for item in comlist:
        if str(item.subreddit) not in subsList: 
            subsList.append(str(item.subreddit))
    # print(subsList)
    return 0.01 if float(len(comlist))/float(len(subsList)) == 0 else float(len(comlist))/float(len(subsList))  


def getSameLevels(user, comlist):
    # print(user)
    total = 0
    tlevel = 0
    for comment in comlist:
        total += 1
        if comment.is_root:
            tlevel += 1
    pcount = max(float(tlevel)/float(total), (float(total)-float(tlevel))/float(total))
    return 0.01 if pcount == 0 else pcount 

def uniqueComments(user, comlist):
    comlist = [x for x in comlist if x.distinguished == None]
    x = 0 
    uniqueComments = []
    flist = [j for j in comlist]
    flength = len(flist)
    freqDict = {}
    while x < len(flist):
        content = flist[x].body
        if content.lower() not in uniqueComments:
            uniqueComments.append(content.lower())
        x += 1
    return len(uniqueComments)/len(comlist)

def getSpread(user, comlist):
    subsList = []
    for item in comlist:
        if str(item.subreddit) not in subsList: 
            subsList.append(str(item.subreddit))
    return 0.01 if float(len(comlist))/float(len(subsList)) == 0 else float(len(comlist))/float(len(subsList))  

def isRepetitive(user, comlist):
    comlist = [x for x in comlist if x.distinguished == None]
    if len(comlist) < 15:
        return 0.01
    
    x = 0 
    uniqueComments = []
    flist = [j for j in comlist]
    #print('FLIST', flist)
    #print(len(flist))
    flength = len(flist)
    #print(flength)
    freqDict = {}
    while x < len(flist):
        #print(x)
        aldone = []
        bad = stopwords.words('english') + stopwords.words('spanish') + stopwords.words('portuguese') + list(string.punctuation) 
        content = flist[x].body.replace("["," ").replace("]"," ")
        if 'http' in content.lower() or 'www.' in content.lower():
            content = content.replace('/', ' ')
        #print("check1") 
        if content.lower() not in uniqueComments:
            uniqueComments.append(content.lower())
        for key in list(string.punctuation) + ['\n']:
            content = content.replace(key, '')
        words = [i for i in content.lower().split(' ') if i.replace("'s",'').replace("'nt",'').replace("'ve",'').replace("'ll",'').replace("'m",'') not in bad and i.strip("'`").strip('`') != '']
        for thing in words:
            if  thing not in aldone:
                aldone.append(thing)
                try: 
                    freqDict[thing] += 1
                except:
                    freqDict[thing] = 1
            
        x += 1
    oDict = sorted(freqDict.items(), key=operator.itemgetter(1))
    #print('ODICT', oDict)
    #print(flength)
    try:
        return (float(oDict[-1][1])/float(flength) + float(oDict[-2][1])/float(flength))/2 
    except IndexError:
        return (float(oDict[-1][1])/float(flength))

def keyWordPres(user, comlist):
    comlist = [x for x in comlist if x.distinguished == None]
    tcount = 0
    hopeful = {"bot":0, "source code":0, "feedback":0, "contact":0, "faq":0, "*":0, "**":0, "^":0}
    for comment in comlist:
        tcount += 1
        for item in hopeful:
            if item in comment.body.lower():
                hopeful[item] += 1
    hopeful_sort = sorted(hopeful.items(), key=operator.itemgetter(1))
    return 0.01 if float(hopeful_sort[-1][1])/float(tcount) == 0 else float(hopeful_sort[-1][1])/float(tcount) 

def fewPosts(user, innum):
    tplist = [post for post in r.redditor(user).submissions.new(limit=100)]
    return 100.0 if len(tplist) == 0 else float(innum)/float(len(tplist))


def avTime(user, comlist):
    x = 0 
    totals = []
    flist = [j for j in comlist]
    while x < len(flist)-1:
        totals.append(flist[x].created_utc - flist[x+1].created_utc)
        x+=1
    # print(sum(totals))
    # print(len(totals))
    result = float(sum(totals))/float(len(totals)) #CAUSE FOR QUITE A FEW ERRORS
    return result 

meanList = [0.26882352941176468, 0.81103500008282825, 0.30068612106439713, 0.84628547896566597, 34.195187552394998, 0.42117868625821758, 7.9323057789799902, 62143.172017787212]
stdList = [0.43502376342044174, 0.17692329372199109, 0.4103803095640271, 0.31432681573818694, 43.278973928533802, 0.40117225759820513, 15.443142775982409, 147452.60000900787]


def normalize_alone(single):
    newList = []
    x = np.array(single)
    for idx in range(len(single)):
        y = np.array(x[idx])
        new = (y-meanList[idx])/stdList[idx]
        newList.append(new.tolist())
    return np.array(newList).T.tolist()

class User:
    def __init__(self, usr):
        comment_list = [x for x in r.redditor(usr).comments.new(limit=100) if str(x.subreddit).lower() not in blacklisted]
        if len(comment_list) < 15:
            self.invalid_flag = True 
        else: 
            self.invalid_flag = False 
            self.bot_in_name = botInName(usr)
            self.same_level_comments = getSameLevels(usr, comment_list)
            self.keyword_present = keyWordPres(usr, comment_list)
            self.unique_comments = uniqueComments(usr, comment_list)
            self.few_posts = fewPosts(usr, len(comment_list))
            self.is_repetitive = isRepetitive(usr, comment_list)
            self.spread = getSpread(usr, comment_list)
            self.average_time_beetween_comments = avTime(usr, comment_list)


class Classifier:
    def __init__(self, threshold): 
        self.threshold = threshold
        self.wih = np.array([[2.69201043e-01,-7.66616015e-02, 5.37590287e-02,-3.97873730e-01
,5.99034137e-02,-1.65300133e-01, 1.69002916e-01,-1.27212345e-01]
 ,[ -1.05991397e-01,-4.11156476e-01,-5.11020321e-01, 1.69261709e+00
,1.64746169e-01,-7.77246989e-01, 1.33937963e+00, 3.28459518e-02]
,[2.06643111e-01, 4.85683056e-02, 4.41266255e-01,-1.06308484e+00
, -2.17737269e-01, 7.76239440e-01,-1.22464070e-02,-3.17771332e-02]
,[ -1.41573443e-01,-3.04611663e-01,-5.74945755e-01, 1.17999135e+00
,1.20915907e-01,-5.94478996e-01, 1.13528085e-01, 6.72478186e-02]
,[ -2.28950660e-01,-3.24794564e-01,-5.37459949e-01, 1.41047789e+00
,7.74998200e-02,-5.10754063e-01, 1.06588535e+00, 1.18869828e-01]
,[1.59138024e-01, 1.64332208e-02, 3.24109756e-01,-7.45074471e-01
, -1.03254040e-01, 4.13048308e-01,-2.82940292e-02, 1.21081843e-01]
,[1.00072380e-01, 9.20597912e-02, 2.07490602e-01,-4.11541526e-01
, -1.81249332e-01, 1.42513322e-01,-4.92596801e-02, 1.70184103e-02]
,[3.12570818e-01, 5.07755025e-01, 7.99758276e-01,-1.63859771e+00
, -1.58640376e-01, 1.04454600e+00,-2.01986067e-01,-9.25766922e-02]
,[2.75542641e-01, 6.19160578e-01, 8.71133768e-01,-2.04872939e+00
, -6.83477657e-02, 7.86638051e-01,-1.11013966e+00,-1.06634807e-01]
,[ -1.53585194e-01,-4.49980553e-02,-3.72068587e-01, 6.36085042e-01
,6.38797800e-02,-3.61838469e-01, 9.85935942e-02, 1.37879050e-01]
,[4.12251200e-02,-2.71299112e-02, 1.35835530e-01,-2.02469529e-01
, -1.71733513e-02, 1.38925195e-01,-1.09821733e-01, 8.44875563e-03]
,[2.78102483e-01, 1.06807612e+00, 1.21235330e+00,-2.53614668e+00
, -1.17519691e-01, 1.20483764e+00,-3.71075156e-01,-1.01154780e-01]
,[2.25389570e-01, 3.09370386e-01, 5.44547807e-01,-1.49165542e+00
, -1.99947871e-01, 1.00929785e+00,-1.06430638e-01,-4.78790048e-02]
,[2.54594090e-02, 2.37898864e-01, 5.63143892e-01,-1.39453030e+00
, -1.76180727e-01, 4.77656132e-01,-9.10164438e-01,-2.82810725e-02]
,[3.28965720e-01, 5.21833167e-01, 9.17969457e-01,-2.07818687e+00
, -5.81314566e-02, 7.63236669e-01,-1.31028428e-01,-1.18704268e-01]
,[ -1.29633626e-01,-1.69051323e-01,-2.15957762e-01, 1.41134564e+00
,1.48512404e-02,-2.14510314e-01, 1.14914144e+00, 1.06685451e-01]
,[1.00092676e-01, 2.75198776e-01, 4.39135632e-01,-1.20503590e+00
, -2.03239914e-01, 6.50391289e-01,-7.10173947e-02,-9.99902978e-02]
,[3.23926404e-01, 5.57635819e-01, 1.00120707e+00,-2.01821838e+00
, -1.01963166e-01, 1.01328674e+00,-1.89362723e-01,-8.13646844e-02]
,[3.21827056e-01, 8.87919012e-01, 1.04329572e+00,-2.29413309e+00
, -9.66993447e-02, 1.20613399e+00,-3.22749086e-01,-1.29832318e-01]
,[ -1.27558486e-01,-4.86239046e-02,-4.89004722e-01, 1.24832326e+00
,1.38180084e-01,-7.06346196e-01, 4.72076492e-02, 5.80445915e-03]
,[ -1.46006270e-01,-1.89286239e-01,-1.78092084e-01, 4.33329293e-01
,1.13966626e-01,-2.62479104e-01, 2.06753831e-01, 7.07932612e-02]
,[3.66512478e-01,-1.82682495e-01, 2.01707403e-01,-4.54146623e-01
,1.83864766e-01, 2.41694494e-01,-6.43353929e-02,-1.09329263e-01]
,[5.39024204e-02,-1.28627839e-01,-1.40163887e-01, 4.82343704e-01
, -9.04652845e-02,-2.27451957e-01, 1.03130029e-01, 2.01471007e-01]
,[ -1.39615945e-01,-1.64959741e-01,-2.20166078e-01, 7.62747165e-01
,1.10194009e-01,-3.54911747e-01, 3.93171518e-01, 9.71666412e-02]
,[3.63112136e-01, 3.18736091e-01, 5.92318967e-01,-1.33099806e+00
, -8.05678723e-02, 6.02688931e-01,-8.35558126e-02,-4.62139469e-02]
,[ -1.34306180e-01, 1.34593578e-02,-2.92967753e-01, 7.94008935e-01
, -3.83106824e-02,-4.82618844e-01,-4.80866897e-02,-4.33226728e-02]
,[ -3.37294852e-01,-7.45747760e-01,-1.06874538e+00, 2.23565565e+00
,1.26981475e-01,-1.31262112e+00, 2.69903365e-01, 7.78344146e-02]
,[2.04461155e-01,-3.34676861e-02, 4.19841412e-01,-5.63357669e-01
,7.66770103e-02, 3.32390012e-01, 2.52030279e-02,-5.54604252e-02]
,[ -2.53579120e-01, 1.78653268e-01,-3.83075279e-01, 5.89676138e-01
, -4.28175110e-03,-3.58996387e-01, 5.34379442e-02, 8.68467452e-02]
,[ -1.87078809e-01, 1.83647219e-02,-4.96025135e-01, 9.70139460e-01
,3.77531658e-02,-6.34890440e-01, 3.25267034e-02, 1.11052452e-01]
,[ -3.03034325e-01,-8.13465697e-01,-1.04615907e+00, 2.16732435e+00
,1.04377852e-01,-1.10715777e+00, 3.00386420e-01, 1.03154833e-01]
,[3.41427082e-01, 1.10499099e-01, 3.86679053e-01,-1.53370661e+00
, -2.99358941e-01, 1.23587063e+00,-8.42612365e-04,-4.56316434e-02]
,[ -1.71782623e-01,-1.40411476e+00,-1.19929011e+00, 2.96805457e+00
,1.88671323e-01,-1.65868122e+00, 4.74396048e-01, 6.99827902e-02]
,[ -2.54805242e-01,-9.29323201e-01,-9.97025202e-01, 2.41993413e+00
,1.19669423e-01,-1.28759714e+00, 3.17129346e-01, 1.01123767e-01]
,[2.37391616e-04, 3.42086250e-02,-2.86014519e-01, 3.23062186e-01
, -1.17703218e-01,-7.98576660e-02, 1.32812019e-02, 1.90666719e-01]
,[2.50798912e-01, 4.95532168e-01, 8.41781067e-01,-1.79160684e+00
, -1.33605951e-01, 1.00324077e+00,-1.88100963e-01,-7.68031079e-02]
,[2.32219311e-01, 6.41497468e-01, 8.55599388e-01,-2.05184632e+00
, -9.84776605e-02, 9.44331059e-01,-2.10771260e-01,-1.09559478e-01]
,[ -2.02236860e-01,-4.49482082e-01,-7.59721925e-01, 1.78840125e+00
,2.16292291e-01,-1.14098769e+00, 1.48944915e-01, 2.40171741e-02]
,[ -7.36925494e-02, 1.45934437e-01,-1.12976348e-01, 1.89458717e-01
,1.04799187e-01,-2.15790994e-01, 2.18954331e-01, 5.45174596e-02]
,[ -1.19499341e-01,-6.25751439e-01,-2.93438607e-01, 2.43861719e+00
,2.95423704e-01,-1.46331028e+00, 9.49515302e-02, 5.91275723e-03]
,[2.35405856e-01, 3.74058737e-01, 7.24448923e-01,-1.67665819e+00
, -1.13997955e-01, 9.31875633e-01,-1.58923543e-01,-5.27549729e-02]
,[5.16763200e-02,-5.79839917e-01,-7.44296134e-01, 2.41156503e+00
,1.68253800e-01,-5.69324434e-01, 2.42565104e+00, 2.32166896e-02]
,[ -2.93799929e-01,-2.83015671e-01,-3.81373585e-01,-6.22640431e-02
, -5.88684957e-03, 4.73316959e-02,-6.39187758e-03, 4.45030572e-02]
,[2.54029432e-01, 3.74365521e-01, 7.10361022e-01,-1.68714214e+00
, -9.32929869e-02, 7.00601663e-01,-1.00264096e-01,-7.72111920e-02]
,[ -7.85146667e-02, 3.45461034e-02,-2.46972774e-01, 2.71504674e-01
,6.13933857e-02,-2.05319787e-01,-1.24801131e-02,-4.32126359e-02]
,[2.34946384e-01, 7.77538104e-01, 6.90613090e-01,-2.25403111e+00
, -1.29924686e-01, 1.18751020e+00,-2.43592404e-01,-1.44155938e-01]
,[3.25670504e-02,-2.66143309e-01,-5.14183759e-01, 1.44945890e+00
,2.24861704e-01,-4.82809131e-01, 1.58609077e+00, 4.75966320e-02]
,[4.17018104e-01,-6.08063658e-02,-3.87892834e-02,-5.73269319e-01
,1.14146581e-02, 2.74160559e-01,-5.84783644e-01,-1.06836696e-01]
,[3.87562383e-02, 2.44602282e-01, 4.90723082e-01,-1.50621383e+00
, -1.75347482e-01, 3.75014305e-01,-1.47040983e+00, 3.38229481e-02]
,[ -8.81472344e-02, 6.29379826e-03,-2.10720134e-01, 2.98726776e-01
, -2.06519712e-01, 5.67631552e-03, 1.49210245e-02, 2.71120169e-01]
,[ -1.08386016e-01, 5.39537356e-01, 8.24936618e-01,-2.12773681e+00
, -2.66895007e-01, 5.73538064e-01,-2.55301070e+00,-1.64158116e-02]
,[2.56365675e-01, 1.31752873e-01, 2.58553279e-01,-8.13983170e-01
, -4.37185733e-03, 3.58684422e-01,-1.04622499e+00,-1.99652849e-01]
,[ -3.37944417e-01,-6.82120424e-01,-1.05350770e+00, 2.11040164e+00
,9.06747238e-02,-1.01479939e+00, 2.36512356e-01, 1.00239084e-01]
,[1.62081571e-01, 2.59181763e+00, 1.73574855e+00,-4.69140525e+00
, -2.87320894e-01, 2.08711457e+00,-7.43083957e-01,-1.85138118e-01]
,[2.70214015e-01, 1.50733632e-01, 6.04270744e-01,-1.06985343e+00
, -9.74478846e-02, 6.49956511e-01,-6.34980691e-02, 1.89956331e-02]
,[1.08497758e-01,-2.20686617e-01,-8.29191760e-02,-7.21376575e-03
, -7.05909392e-02, 1.33577870e-01,-1.47112657e-01, 9.67671678e-02]
,[ -2.43147851e-01,-6.99823425e-01,-9.48364556e-01, 2.12532750e+00
,1.24008957e-01,-1.12927769e+00, 2.57829417e-01, 7.14155716e-02]
,[ -4.37970466e-02, 7.53824429e-02, 4.83613084e-03,-2.69392533e-01
, -7.62309710e-02,-3.33256947e-02, 1.07912702e-01, 4.72232529e-02]
,[ -1.31235628e-01,-1.68244522e-01,-2.82688261e-01, 1.03580891e+00
,1.52662575e-01,-4.93712595e-01, 2.37808253e-01, 5.68194642e-02]
,[1.62087096e-01, 3.80115578e-01, 4.93934438e-01,-1.21762461e+00
, -2.11815650e-01, 4.22672012e-01,-7.94037715e-02,-1.37945927e-01]
,[1.70395961e-01,-8.75226368e-02, 1.63154344e-01,-5.17133251e-01
,6.37618672e-02, 3.62886235e-01, 5.47064418e-02, 1.41940119e-01]
,[9.68741454e-03, 8.25732519e-01, 9.53660860e-01,-2.64244817e+00
, -2.14481616e-01, 8.23654135e-01,-2.57526723e+00,-4.26209262e-02]
,[1.21986605e-01,-2.78649967e-01,-6.36752363e-02,-2.44618319e-01
, -2.27719933e-01, 1.32092384e-01,-1.64168078e-01,-5.08826067e-02]
,[1.58820598e-01, 8.86701581e-02, 2.76492325e-01,-8.88567416e-01
, -1.79629258e-01, 5.33067363e-01, 2.33486904e-02,-5.04859270e-02]])

        self.who = np.array([[2.19930175e-01,-1.14900576e+00, 7.70074408e-01,-6.83125143e-01
, -7.84349487e-01, 6.49719348e-01, 3.16943512e-01, 1.22109311e+00
,1.58250979e+00,-4.11974072e-01, 2.38638724e-01, 1.93178396e+00
,1.08295374e+00, 9.09399122e-01, 1.41503976e+00,-6.47088875e-01
,7.89248701e-01, 1.50133249e+00, 1.75518887e+00,-6.91060905e-01
, -1.91215143e-01, 3.87755449e-01,-2.18677799e-01,-3.51119487e-01
,7.94587237e-01,-2.08154381e-01,-1.65203247e+00, 3.93385349e-01
, -2.41934056e-01,-5.58694363e-01,-1.49773873e+00, 1.07606414e+00
, -2.22619254e+00,-1.64334689e+00,-1.35823332e-01, 1.34925699e+00
,1.46613275e+00,-1.06795054e+00,-5.74365781e-02,-1.50217327e+00
,1.13697996e+00,-1.56887839e+00,-3.34669494e-04, 1.15636887e+00
, -8.33920428e-02, 1.63907343e+00,-9.00251415e-01, 4.77599898e-01
,1.06997557e+00,-2.21615106e-04, 1.69975780e+00, 7.18329474e-01
, -1.52357335e+00, 4.23760131e+00, 7.25643367e-01, 1.85076743e-01
, -1.33633240e+00, 2.18413371e-01,-4.16495054e-01, 8.21425071e-01
,4.16765908e-01, 2.10138903e+00, 2.28111855e-01, 6.11093075e-01]])
        self.activation_function = lambda x: __import__('scipy').special.expit(x)
    def is_a_bot(self, name):
        tObj = User(name)
        if tObj.invalid_flag: return None 
        inpt_list = normalize_alone(list(tObj.__dict__.values())[1:])
        inputs = np.array(inpt_list, ndmin=2).T 
        hidden_outputs = self.activation_function(np.dot(self.wih, inputs))
        result = self.activation_function(np.dot(self.who, hidden_outputs))[0][0]
        # print('Returning {} with confidence {}'.format(result>=self.threshold, result))
        return (result >= self.threshold, result)



                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                