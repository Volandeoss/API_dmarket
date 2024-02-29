from tkinter import *
from bs4 import BeautifulSoup as bs
import requests as req
import json
from datetime import datetime
from nacl.bindings import crypto_sign
import time
import steammarket as sm
#from testing_url_image import WebImage
import urllib.request
#import base64
import io
from PIL import ImageTk, Image
from environs import Env

env = Env()
env.read_env()

# root = tk.Tk()
# root.title("Weather")

#link = "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09G3h5SOhe7LO77QgHIf7pJ0iLGS94_2jAOx_BdvZGr2I9eVegVvNV3Q_gW8lbrsgZC875TPnWwj5HcWwWbOUQ"
private_key = env.str("PRIVATE_KEY")
key = env.str("API_KEY")

class WebImage:
    def __init__(self, url, width=None, height=None):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)
        if width and height:
            image = image.resize((width, height),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image
    
    def resize(self, width, height):
        resized_image = self.image.resize((width, height))
        self.image = ImageTk.PhotoImage(resized_image)




#imageUrl="https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09G3h5SOhe7LO77QgHIf7pJ0iLGS94_2jAOx_BdvZGr2I9eVegVvNV3Q_gW8lbrsgZC875TPnWwj5HcWwWbOUQ"


private_key='4c69f17c0dfb8d0bba2d3156647828d620da75e4364b5a88ebcf68a67a12b17a53123e7ad06d9bbdbaeea354a2919b8774ab72e11bccb963881457e7f050e3a7'
key=

rootApiUrl = "https://api.dmarket.com"

def get_offer_from_market():
    market_response = req.get(rootApiUrl + "/exchange/v1/market/items?gameId=a8db&limit=1&currency=USD")
    offers = json.loads(market_response.text)["objects"]
    return offers[0]


def build_target_body_from_offer(offer):
    return {"targets": [
        {"amount": 1, "gameId": offer["gameId"], "price": {"amount": "2", "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"],
                        "ownerGets": {"amount": "1", "currency": "USD"}}}
    ]}


def get_dmarket_lowest_offer(name:str,Only_Dmarket:bool):
    nonce = str(round(datetime.now().timestamp()))
    api_url_path = "/exchange/v1/offers-by-title"
    method = "GET"
    offer_from_market = get_offer_from_market()
    body = build_target_body_from_offer(offer_from_market)
    string_to_sign = method + api_url_path + json.dumps(body) + nonce
    signature_prefix = "dmar ed25519 "
    encoded = string_to_sign.encode('utf-8')
    secret_bytes = bytes.fromhex(private_key)
    signature_bytes = crypto_sign(encoded, bytes.fromhex(private_key))
    signature = signature_bytes[:64].hex()
    headers = {
        "X-Api-Key": key,
        "X-Request-Sign": signature_prefix + signature,
        "X-Sign-Date": nonce
    }
  
    curs=""
    all_skins=[]
    y=1
    steam_lowest=sm.get_csgo_item(name,currency="USD")
    print(steam_lowest)
    
    if type(steam_lowest) is not dict:
        steam="couldn`t be retrieved (wait 100 seconds)"
        amount="couldn`t be retrieved (wait 100 seconds)"
    else:
        steam=steam_lowest.get("lowest_price","No key")
        amount=steam_lowest.get("volume","No key")
    while True:
        
        params={
            "Title":name,
            "limit":100,
            "cursor":curs
        }
        resp= req.get(rootApiUrl + "/exchange/v1/offers-by-title",headers=headers,params=params)
        #print(resp.url)
        ending=json.loads(resp.text)["total"]["offers"]
        if ending == 0:
            return None
        offers=json.loads(resp.text)["objects"]
        
        
            
        try:
            curs=json.loads(resp.text)["cursor"]
        except:
            #у випадку якщо ми беремо офери які тільки знаходяться на дм, то буде спрацьовувати ця умова
            return (min(all_skins),offers[0]["image"]),ending,steam,amount
        for offer in offers:
            if Only_Dmarket==True:
                if offer['inMarket'] is True:
                    print(f"{y}. {int(offer['price']['USD'])/100} - {offer['inMarket']}")
                    all_skins.append(int(offer['price']['USD'])/100)
                    if y == ending:
                        
                        return min(all_skins),offers[0]["image"],ending,steam,amount
                    y+=1
            else:
                print(f"{y}. {int(offer['price']['USD'])/100} - {offer['inMarket']}")
                all_skins.append(int(offer['price']['USD'])/100)
                if y == ending:
                    return min(all_skins),offers[0]["image"],ending,steam,amount
                y+=1

root = Tk()
root.title("Skinи")
root.geometry("700x500")
root.resizable(width=False,height=False)
canvas = Canvas(root, width=300, height=225,bg="lightgrey")
canvas_for_dot=Canvas(root,width=20,height=20)
#global red_dot,no_dot
#red_dot=PhotoImage(file="red_dot.png")
#no_dot=PhotoImage(file="no_dot.png")
#dot_image=canvas_for_dot.create_image(0,0, image=no_dot)
canvas_for_dot.place(x=342,y=10)


x1, y1 = 2,226
x2, y2 = 302,2

canvas.create_line(2,226,302,226,fill="black")#знизу
canvas.create_line(2,226,2,2,fill="black")#зліва
canvas.create_line(2,2,302,2,fill="black")#зверху
canvas.create_line(301,2,301,226,fill="black")#з права

canvas.create_line(3,225,300,225,fill="grey",width=2)#знизу
canvas.create_line(4,224,4,3,fill="grey",width=2)#зліва
canvas.create_line(3,4,301,4,fill="grey",width=2)#зверху
canvas.create_line(300,3,300,226,fill="grey",width=2)#з права
# Calculate the center coordinates for the image
center_x = (x1 + x2) // 2
center_y = (y1 + y2) // 2

def entry_on_enter(event):
    
    #canvas_for_dot.itemconfig(dot_image,image=red_dot)
    #print("shit goes") 
    text=entry.get()
    global img2
    #red_dot=PhotoImage(file="red_dot.png")
    #no_dot=PhotoImage(file="no_dot.png")
    main_func=get_dmarket_lowest_offer(text,False)
    if main_func is not None:
        minim,image_link,total,steamprice,amount_steam=main_func
        img2=WebImage(image_link,256,192).get()
        canvas.itemconfig(image_1,image=img2)
    
        dmarket_lowest.config(text=f"${minim}")
        offers_dmarket.config(text=str(total))
        try:
            steam_lowest.config(text=f"{float(steamprice[1:])}-13% = {float(steamprice[1:]) - 13*float(steamprice[1:])/100}")
        except:
            steam_lowest.config(text=str(steamprice))
        try:
            offers_steam.config(text=f"Максимум - {int(amount_steam)*9}")
        except:
            offers_steam.config(text=amount_steam)

        #canvas_for_dot.itemconfig(dot_image,image=no_dot)
    else:
        dmarket_lowest.config(text="Хуйню написав")
        offers_dmarket.config(text="Хуйню написав")
        steam_lowest.config(text="Хуйню написав")
        offers_steam.config(text="Хуйню написав")
        #canvas_for_dot.itemconfig(dot_image,image=no_dot)
    
    
def add_the_lowest_diff():
    text=entry.get()
    with open("lowest_difference.txt","a") as fil:
        fil.write(text+"\n")        

# Create an image item on the canvas
#initial= PhotoImage(file="initial.png")
image_1=canvas.create_image(center_x, center_y)

canvas.place(x=40,y=10)

entry = Entry(root)
entry.config(width=40)
entry.place(x=400,y=100)

label_dmarket=Label(root,text="Найнижчий офер на дмаркеті:")
dmarket_lowest=Label(root,text="#")
label_offers_dmarket=Label(root,text="Кількість оферів на дмаркеті:")
offers_dmarket=Label(root,text="#")
label_steam=Label(root,text="Найнижчий офер на стімі:")
steam_lowest=Label(root,text="#")
label_offers_steam=Label(root,text="Кількість оферів на стімі:")
offers_steam=Label(root,text="#")

label_dmarket.place(y=240,x=40)
dmarket_lowest.place(y=260,x=40)
label_offers_dmarket.place(y=280,x=40)
offers_dmarket.place(y=300,x=40)
label_steam.place(y=320,x=40)
steam_lowest.place(y=340,x=40)
label_offers_steam.place(y=360,x=40)
offers_steam.place(y=380,x=40)

button1=Button(root,text="додати скін",command=add_the_lowest_diff)
button1.place(x=400,y=120)


entry.bind("<Return>", entry_on_enter)
root.mainloop()