import parties
from parties import *

from PIL import Image, ImageDraw, ImageFont

SP_X, SP_Y = (50,200)
PARTY_HEIGHT = 100
NUMBER_WIDTH = 50
LOGO_WIDTH = 100
FIELD_WIDTH = 100

bulwidth = 600
bulheight = 400+PARTY_HEIGHT*len(parties.PARTIES)

def new_bulleten():

    img = Image.new("RGB",(bulwidth,bulheight),(255,255,255))
    draw = ImageDraw.ImageDraw(img,"RGB")

    logo = Image.open("bulleten/general/KeslyLogo.png","r")
    img.paste(logo,(30,30),logo)
    draw.text((230,60),"ИЗБИРАТЕЛЬНЫЙ\nБЮЛЛЕТЕНЬ",(0,0,0),ImageFont.truetype("arialbd.ttf",35))
    draw.text((230,140),"для голосования\nпо партийным спискам\nна выборах в КэсДуму",(0,0,0),ImageFont.truetype("arial.ttf",25))
    part_idx = 0
    for party_name, party in parties.PARTIES.items():
        part_idx += 1
        draw.rectangle(((SP_X,SP_Y+PARTY_HEIGHT*part_idx),(SP_X+NUMBER_WIDTH,SP_Y+PARTY_HEIGHT*(part_idx+1))),outline=(0,0,0),width=4)
        draw.rectangle(((SP_X+NUMBER_WIDTH,SP_Y+PARTY_HEIGHT*part_idx),(SP_X+NUMBER_WIDTH+LOGO_WIDTH,SP_Y+PARTY_HEIGHT*(part_idx+1))),outline=(0,0,0),width=4)
        draw.rectangle(((SP_X+NUMBER_WIDTH+LOGO_WIDTH,SP_Y+PARTY_HEIGHT*part_idx),(bulwidth-SP_X-FIELD_WIDTH,SP_Y+PARTY_HEIGHT*(part_idx+1))),outline=(0,0,0),width=4)
        draw.rectangle(((bulwidth-SP_X-FIELD_WIDTH,SP_Y+PARTY_HEIGHT*part_idx),(bulwidth-SP_X,SP_Y+PARTY_HEIGHT*(part_idx+1))),outline=(0,0,0),width=4)
        draw.text((SP_X+NUMBER_WIDTH*1/5,SP_Y+PARTY_HEIGHT*part_idx+PARTY_HEIGHT*1/3.5),f"{party['number']}",(0,0,0),font=ImageFont.truetype("arialbd.ttf",30))
        img.paste(Image.open(party["logo"],"r"),(SP_X+NUMBER_WIDTH+10,SP_Y+PARTY_HEIGHT*part_idx+10))
        draw.text((SP_X+NUMBER_WIDTH+LOGO_WIDTH+12,SP_Y+PARTY_HEIGHT*part_idx+30),f"{party['print_name']}",(0,0,0),font=ImageFont.truetype("arialbd.ttf",18))
        draw.rectangle(((bulwidth-SP_X-FIELD_WIDTH+15,SP_Y+PARTY_HEIGHT*part_idx+15),(bulwidth-SP_X-15,SP_Y+PARTY_HEIGHT*(part_idx+1)-15)),fill=(191,191,191),outline=(0,0,0),width=4)

    img.save("bulleten.png")

def parsvote(id, votefile: str):
    global INVALID_BUL
    votesquare_color = (191,191,191)
    voteimg = Image.open(votefile)
    if voteimg.size != (bulwidth, bulheight):
        voteimg = voteimg.resize((bulwidth, bulheight))
    vote = []
    for i in range(len(parties.PARTIES)):
        votesquare_pos = (bulwidth-SP_X-FIELD_WIDTH+20,SP_Y+PARTY_HEIGHT*(i+1)+20)
        votesquare_size = (bulwidth-SP_X-20,SP_Y+PARTY_HEIGHT*(i+2)-20)
        for pix_y in range(votesquare_pos[1],votesquare_size[1]):
            for pix_x in range(votesquare_pos[0], votesquare_size[0]):
                pixel = voteimg.getpixel((pix_x, pix_y))
                if check_pixel(pixel):
                    vote.append(i)
                    break
            if i in vote:
                break
    votetext = "ГОЛОС НЕ ОПРЕДЕЛЁН"
    if len(vote) < 1:
        parties.INVALID_BUL += 1
        votetext = "Недействительный бюллетень (Пустой бланк)"
        users[id]["vote_id"] = -1
    elif len(vote) == 1:
        Results[list(PARTIES.keys())[vote[0]]] += 1
        votetext = f"Голос за партию {list(PARTIES.keys())[vote[0]]}"
        users[id]["vote_id"] = vote[0]
    elif len(vote) > 1:
        parties.INVALID_BUL += 1
        votetext = "Недействительный бюллетень (Несколько галочек)"
        users[id]["vote_id"] = -1
    users[id]["vote_option_name"] = votetext
    global_spectator_pict(votefile, f"☑ БЮЛЛЕТЕНЬ ИЗБИРАТЕЛЯ {users[id]['cryptokey']}\nГОЛОС ЗАСЧИТАН БОТОМ КАК\n{votetext}")
    users[id]["wait_bul"] = False
    upload_voters()
    return

def check_pixel(pixel):
    if (pixel[0] == pixel[1] == pixel[2]) and (pixel != (0,0,0)) and (pixel != (255,255,255)):
        return False
    return True

if __name__ == "__main__":
    new_bulleten()