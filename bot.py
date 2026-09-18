# -*- coding: utf-8 -*-
import os, io, time, math, requests
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
FOOTBALL_API_TOKEN = os.getenv('FOOTBALL_API_TOKEN')
API_URL = 'https://api.football-data.org/v4/competitions/{}/matches'
TEHRAN = ZoneInfo('Asia/Tehran')
WIDTH, MARGIN, GAP = 1600, 70, 28

COMPETITIONS = {
    'PL':'لیگ برتر انگلیس','PD':'لالیگا','SA':'سری آ ایتالیا','BL1':'بوندسلیگا',
    'FL1':'لیگ ۱ فرانسه','DED':'اردیویسه','PPL':'لیگ پرتغال','BSA':'سری آ برزیل','CL':'لیگ قهرمانان اروپا'
}
LEAGUE_COLORS = {
    'PL':(132,82,246),'PD':(236,70,91),'SA':(42,132,238),'BL1':(232,66,72),
    'FL1':(50,120,236),'DED':(242,145,42),'PPL':(38,170,118),'BSA':(38,158,103),'CL':(92,103,238)
}
LEAGUE_ICONS = {'PL':'PL','PD':'LaLiga','SA':'Serie A','BL1':'BL','FL1':'L1','DED':'NL','PPL':'PT','BSA':'BR','CL':'UCL'}

TEAM_NAMES = {
'Brentford FC':'برنتفورد','Chelsea FC':'چلسی','Arsenal FC':'آرسنال','Liverpool FC':'لیورپول','Manchester City FC':'منچسترسیتی','Manchester United FC':'منچستریونایتد','Tottenham Hotspur FC':'تاتنهام','Newcastle United FC':'نیوکاسل','Aston Villa FC':'استون ویلا','Everton FC':'اورتون','West Ham United FC':'وستهم','Fulham FC':'فولام','Crystal Palace FC':'کریستال پالاس','Brighton & Hove Albion FC':'برایتون','Wolverhampton Wanderers FC':'ولورهمپتون','Nottingham Forest FC':'ناتینگهام فارست','AFC Bournemouth':'بورنموث','Burnley FC':'برنلی','Leeds United FC':'لیدز','Sunderland AFC':'ساندرلند',
'Real Madrid CF':'رئال مادرید','FC Barcelona':'بارسلونا','RCD Espanyol de Barcelona':'اسپانیول','Elche CF':'الچه','Club Atlético de Madrid':'اتلتیکو مادرید','Club Atlأ©tico de Madrid':'اتلتیکو مادرید','Sevilla FC':'سویا','Valencia CF':'والنسیا','Villarreal CF':'ویارئال','Athletic Club':'اتلتیک بیلبائو','Real Betis Balompié':'رئال بتیس','Real Betis Balompiأ©':'رئال بتیس','Getafe CF':'ختافه','Girona FC':'ژیرونا','RC Celta de Vigo':'سلتاویگو','CA Osasuna':'اوساسونا','Rayo Vallecano de Madrid':'رایو وایکانو','RCD Mallorca':'مایورکا','Deportivo Alavés':'آلاوس','Deportivo Alavأ©s':'آلاوس','Real Sociedad de Fútbol':'رئال سوسیداد','Real Sociedad de Fأ؛tbol':'رئال سوسیداد',
'FC Internazionale Milano':'اینتر','Inter Milan':'اینتر','AC Milan':'آث میلان','Juventus FC':'یوونتوس','SSC Napoli':'ناپولی','AS Roma':'رم','SS Lazio':'لاتزیو','Atalanta BC':'آتالانتا','ACF Fiorentina':'فیورنتینا','Torino FC':'تورینو','Bologna FC 1909':'بولونیا','Genoa CFC':'جنوا','Udinese Calcio':'اودینزه','Parma Calcio 1913':'پارما','US Lecce':'لچه','Cagliari Calcio':'کالیاری','Como 1907':'کومو','US Sassuolo Calcio':'ساسولو','Sassuolo Calcio':'ساسولو',
'FC Bayern München':'بایرن مونیخ','FC Bayern Mأ¼nchen':'بایرن مونیخ','Borussia Dortmund':'دورتموند','RB Leipzig':'لایپزیگ','Bayer 04 Leverkusen':'بایرلورکوزن','Eintracht Frankfurt':'آینتراخت فرانکفورت','VfB Stuttgart':'اشتوتگارت','VfL Wolfsburg':'ولفسبورگ','Borussia Mönchengladbach':'مونشن گلادباخ','Borussia Mأ¶nchengladbach':'مونشن گلادباخ','SV Werder Bremen':'وردربرمن','1. FSV Mainz 05':'ماینتس','TSG 1899 Hoffenheim':'هوفنهایم','Sport-Club Freiburg':'فرایبورگ','FC Augsburg':'آگسبورگ','1. FC Union Berlin':'یونیون برلین','1. FC Köln':'کلن','1. FC Kأ¶ln':'کلن','Hamburger SV':'هامبورگ',
'Paris Saint-Germain FC':'پاری سن ژرمن','Olympique de Marseille':'مارسی','AS Monaco FC':'موناکو','Olympique Lyonnais':'لیون','Lille OSC':'لیل','OGC Nice':'نیس','Stade Rennais FC 1901':'رن','FC Nantes':'نانت','Toulouse FC':'تولوز','RC Lens':'لانس','Racing Club de Lens':'لانس','RC Strasbourg Alsace':'استراسبورگ',
'AFC Ajax':'آژاکس','PSV':'آیندهوون','Feyenoord Rotterdam':'فاینورد','AZ':'آلکمار',"FC Twente '65":'توئنته','FC Utrecht':'اوترخت','PEC Zwolle':'زوله','FC Groningen':'خرونینگن',
'SL Benfica':'بنفیکا','FC Porto':'پورتو','Sporting Clube de Portugal':'اسپورتینگ','SC Braga':'براگا','Vitória SC':'ویتوریا گیمارش','Vitأ³ria SC':'ویتوریا گیمارش',
'CR Flamengo':'فلامینگو','SE Palmeiras':'پالمیراس','Botafogo FR':'بوتافوگو','Fluminense FC':'فلومیننزه','Corinthians':'کورینتیانس','São Paulo FC':'سائوپائولو','Sأ£o Paulo FC':'سائوپائولو'
}

FONT_PATHS = {
    'bold': ['/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf','/usr/share/fonts/opentype/noto/NotoKufiArabic-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
    'regular': ['/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf','/usr/share/fonts/opentype/noto/NotoKufiArabic-Regular.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
    'english': ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
}
def get_font(size,bold=False,english=False):
    custom=os.getenv('FONT_PATH')
    if custom and os.path.exists(custom): return ImageFont.truetype(custom,size)
    for p in FONT_PATHS['english' if english else ('bold' if bold else 'regular')]:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def rtl_args(font,fill,anchor='ra',align='right'):
    return {'font':font,'fill':fill,'anchor':anchor,'align':align,'direction':'rtl','language':'fa'}

def repair_text(text):
    if text is None:return ''
    text=str(text)
    try:
        r=text.encode('cp1256').decode('utf-8')
        if r != text and ('�' not in r): return r
    except Exception: pass
    return text

def persian_digits(text):
    return str(text).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))

def draw_rtl(draw,xy,text,font,fill,anchor='ra'):
    draw.text(xy,repair_text(text),**rtl_args(font,fill,anchor))

def bbox(draw,text,font,rtl=True):
    if rtl:
        return draw.textbbox((0,0),repair_text(text),font=font,direction='rtl',language='fa')
    return draw.textbbox((0,0),str(text),font=font)

def centered(draw,cx,y,text,font,fill,rtl=True):
    b=bbox(draw,text,font,rtl); w=b[2]-b[0]
    if rtl:
        draw.text((cx+w/2,y),repair_text(text),**rtl_args(font,fill,'ra','center'))
    else:
        draw.text((cx-w/2,y),str(text),font=font,fill=fill,anchor='la')

def fit_font(draw,text,max_width,max_size,min_size=18,bold=True):
    for s in range(max_size,min_size-1,-2):
        f=get_font(s,bold=bold)
        if bbox(draw,text,f)[2]-bbox(draw,text,f)[0] <= max_width:return f
    return get_font(min_size,bold=bold)

def get_today(): return datetime.now(TEHRAN).strftime('%Y-%m-%d')
def format_date(s):
    try:
        d=datetime.strptime(s,'%Y-%m-%d'); return persian_digits(f'{d.year}/{d.month:02d}/{d.day:02d}')
    except Exception:return persian_digits(s)
def match_time(s):
    try:return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TEHRAN).strftime('%H:%M')
    except Exception:return '--:--'

LOGO_CACHE={}
def download_logo(url):
    if not url:return None
    if url in LOGO_CACHE:return LOGO_CACHE[url]
    try:
        r=requests.get(url,timeout=15); r.raise_for_status()
        im=Image.open(io.BytesIO(r.content)).convert('RGBA'); im.thumbnail((250,250),Image.Resampling.LANCZOS)
        LOGO_CACHE[url]=im; return im
    except Exception as e:
        print('Logo download failed:',e); LOGO_CACHE[url]=None; return None

def get_matches(code,date_string):
    headers={'X-Auth-Token':FOOTBALL_API_TOKEN}; params={'dateFrom':date_string,'dateTo':date_string}
    for attempt in range(3):
        try:
            r=requests.get(API_URL.format(code),headers=headers,params=params,timeout=30)
            if r.status_code==429: time.sleep(45); continue
            r.raise_for_status(); return r.json().get('matches',[])
        except Exception as e:
            print(f'Error {code}: {e}')
            if attempt<2: time.sleep(5)
    return []

def background(w,h):
    im=Image.new('RGBA',(w,h)); px=im.load()
    for y in range(h):
        t=y/max(1,h-1)
        base=(7+int(5*t),10+int(5*t),24+int(12*t))
        for x in range(w):
            dx=(x-w*.5)/w; dy=(y-h*.18)/h; glow=max(0,1-math.sqrt(dx*dx+dy*dy)*3)
            px[x,y]=(min(255,int(base[0]+glow*8)),min(255,int(base[1]+glow*8)),min(255,int(base[2]+glow*18)),255)
    ov=Image.new('RGBA',(w,h)); d=ImageDraw.Draw(ov)
    d.ellipse((-350,-250,500,650),fill=(91,70,245,24)); d.ellipse((w-550,0,w+300,800),fill=(35,110,240,20))
    for x in range(-h,w+h,260): d.line((x,h,x+h,0),fill=(255,255,255,5),width=2)
    ov=ov.filter(ImageFilter.GaussianBlur(16)); im.alpha_composite(ov); return im

def shadow(im,box,r=30):
    sh=Image.new('RGBA',im.size); d=ImageDraw.Draw(sh); x1,y1,x2,y2=box
    d.rounded_rectangle((x1,y1+12,x2,y2+12),radius=r,fill=(0,0,0,125)); sh=sh.filter(ImageFilter.GaussianBlur(24)); im.alpha_composite(sh)

def draw_logo(im,logo,cx,cy,size=150,accent=(120,100,240)):
    s=size+42; plate=Image.new('RGBA',(s,s)); d=ImageDraw.Draw(plate)
    d.ellipse((7,11,s-3,s+2),fill=(0,0,0,90)); d.ellipse((0,0,s-9,s-9),fill=(247,249,253,255),outline=accent,width=4)
    d.ellipse((10,10,s-19,s-19),outline=(220,224,235,255),width=2)
    if logo:
        lg=logo.copy(); lg.thumbnail((size-5,size-5),Image.Resampling.LANCZOS)
        plate.alpha_composite(lg,((s-lg.width)//2,(s-lg.height)//2))
    else:
        d.ellipse((38,38,s-47,s-47),outline=(185,190,205,255),width=4)
    im.alpha_composite(plate,(int(cx-s/2),int(cy-s/2)))

def league_badge(draw,x,y,code,accent):
    r=27; draw.ellipse((x-r,y-r,x+r,y+r),fill=accent); f=get_font(14,bold=True,english=True)
    label=LEAGUE_ICONS.get(code,code); b=draw.textbbox((0,0),label,font=f); draw.text((x-(b[2]-b[0])/2,y-(b[3]-b[1])/2-2),label,font=f,fill='white')

def draw_match_card(im,m,x,y,w,h,num):
    d=ImageDraw.Draw(im); accent=LEAGUE_COLORS.get(m['competition_code'],(100,110,235)); shadow(im,(x,y,x+w,y+h))
    d.rounded_rectangle((x,y,x+w,y+h),radius=30,fill=(17,22,41,255),outline=(255,255,255,10),width=1)
    d.rounded_rectangle((x,y,x+w,y+8),radius=5,fill=accent)
    # subtle inner glow
    d.rounded_rectangle((x+3,y+3,x+w-3,y+h-3),radius=27,outline=(*accent,38),width=2)
    league_badge(d,x+49,y+48,m['competition_code'],accent)
    lf=fit_font(d,m['league_name'],w-170,29,18)
    draw_rtl(d,(x+w-30,y+30),m['league_name'],lf,(242,244,249),'ra')
    d.line((x+30,y+92,x+w-30,y+92),fill=(255,255,255,35),width=2)
    # match number pill
    nf=get_font(18,bold=True); n=persian_digits(num); nb=bbox(d,n,nf); nw=nb[2]-nb[0]
    d.rounded_rectangle((x+24,y+112,x+24+max(54,nw+26),y+150),radius=18,fill=(255,255,255,12),outline=(255,255,255,22),width=1)
    d.text((x+24+max(54,nw+26)/2,y+131),n,**rtl_args(nf,(220,224,235),'mm','center'))
    home_x=x+w*.27; away_x=x+w*.73; logo_y=y+185
    draw_logo(im,m['home_logo'],home_x,logo_y,138,accent); draw_logo(im,m['away_logo'],away_x,logo_y,138,accent)
    # central VS / clock motif
    vf=get_font(18,bold=True,english=True); d.text((x+w/2,y+165),'VS',font=vf,fill=(113,123,151),anchor='mm')
    tw,th=170,68; tx=x+w/2-tw/2; ty=y+220
    d.rounded_rectangle((tx+2,ty+5,tx+tw+2,ty+th+5),radius=20,fill=(0,0,0,65)); d.rounded_rectangle((tx,ty,tx+tw,ty+th),radius=20,fill=accent)
    tf=get_font(34,bold=True); tt=persian_digits(m['time']); d.text((x+w/2,ty+th/2-2),tt,**rtl_args(tf,(255,255,255),'mm','center'))
    hf=fit_font(d,m['home'],w*.36,31,18); af=fit_font(d,m['away'],w*.36,31,18)
    centered(d,home_x,y+301,m['home'],hf,(249,250,253)); centered(d,away_x,y+301,m['away'],af,(249,250,253))
    sf=get_font(16); centered(d,home_x,y+350,'میزبان',sf,(113,122,149)); centered(d,away_x,y+350,'مهمان',sf,(113,122,149))

def create_poster(matches):
    cols=2; card_w=int((WIDTH-MARGIN*2-GAP)/2); card_h=395; rows=math.ceil(len(matches)/2); header=385; footer=105
    H=header+rows*card_h+max(0,rows-1)*GAP+footer+60; im=background(WIDTH,H); d=ImageDraw.Draw(im)
    d.rectangle((0,0,WIDTH,8),fill=(132,82,246)); d.rectangle((0,8,WIDTH,11),fill=(65,125,240,120))
    # left brand
    ef=get_font(24,bold=True,english=True); d.text((MARGIN,50),'FOOTBALL DAILY',font=ef,fill=(151,139,255))
    d.text((MARGIN,86),'MATCH CENTER',font=get_font(14,bold=True,english=True),fill=(93,101,130))
    # right title
    title='بازی‌های امروز'; tf=get_font(72,bold=True); draw_rtl(d,(WIDTH-MARGIN,92),title,tf,(250,251,255),'ra')
    sub='برنامه مسابقات فوتبال امروز'; draw_rtl(d,(WIDTH-MARGIN,181),sub,get_font(25),(145,153,180),'ra')
    # date glass panel
    date='تاریخ '+format_date(get_today()); df=get_font(24,bold=True); dw=bbox(d,date,df)[2]-bbox(d,date,df)[0]; pw=max(300,dw+60)
    d.rounded_rectangle((MARGIN,145,MARGIN+pw,211),radius=20,fill=(255,255,255,14),outline=(255,255,255,30),width=2)
    draw_rtl(d,(MARGIN+pw-28,160),date,df,(236,239,247),'ra')
    d.line((MARGIN,285,WIDTH-MARGIN,285),fill=(255,255,255,35),width=2)
    # count label + mini sports icon
    count=persian_digits(len(matches))+' مسابقه امروز'; draw_rtl(d,(WIDTH-MARGIN,326),count,get_font(23,bold=True),(143,151,178),'ra')
    d.ellipse((MARGIN,316,MARGIN+20,336),fill=(132,82,246)); d.arc((MARGIN+4,320,MARGIN+16,332),0,270,fill=(255,255,255),width=2)
    start=header
    for i,m in enumerate(matches):
        row,col=i//2,i%2; x=MARGIN+col*(card_w+GAP); y=start+row*(card_h+GAP); draw_match_card(im,m,x,y,card_w,card_h,i+1)
    fy=start+rows*card_h+max(0,rows-1)*GAP+30; d.line((MARGIN,fy,WIDTH-MARGIN,fy),fill=(255,255,255,30),width=2)
    draw_rtl(d,(WIDTH-MARGIN,fy+29),'تمامی ساعت‌ها به وقت تهران',get_font(20),(112,121,148),'ra')
    d.ellipse((MARGIN,fy+30,MARGIN+16,fy+46),fill=(132,82,246))
    out=io.BytesIO(); im.convert('RGB').save(out,'JPEG',quality=97,optimize=True); out.seek(0); return out

def send_photo(photo,caption):
    url=f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'; files={'photo':('football_today.jpg',photo,'image/jpeg')}; data={'chat_id':CHAT_ID,'caption':caption}
    r=requests.post(url,files=files,data=data,timeout=60); r.raise_for_status(); print('Telegram message sent.')

def main():
    print('='*60); print('FOOTBALL DAILY BOT'); print('='*60)
    for name,val in [('BOT_TOKEN',BOT_TOKEN),('CHAT_ID',CHAT_ID),('FOOTBALL_API_TOKEN',FOOTBALL_API_TOKEN)]:
        if not val: raise ValueError(f'{name} is missing')
    today=get_today(); print('Today in Tehran:',today); all_matches=[]
    for code,league_name in COMPETITIONS.items():
        print('Checking',code); matches=get_matches(code,today); print(code,len(matches),'matches')
        for match in matches:
            if match.get('status') in ('CANCELLED','POSTPONED'): continue
            utc=match.get('utcDate');
            if not utc: continue
            home=repair_text(match.get('homeTeam',{}).get('name','تیم میزبان')); away=repair_text(match.get('awayTeam',{}).get('name','تیم مهمان'))
            all_matches.append({'competition_code':code,'league_name':league_name,'home':TEAM_NAMES.get(home,home),'away':TEAM_NAMES.get(away,away),'home_logo':download_logo(match.get('homeTeam',{}).get('crest')),'away_logo':download_logo(match.get('awayTeam',{}).get('crest')),'time':match_time(utc),'utc':utc})
    all_matches.sort(key=lambda z:z['utc']); print('TOTAL MATCHES:',len(all_matches))
    if not all_matches:
        url=f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'; msg='⚽ بازی‌های امروز\n\n📅 تاریخ: '+format_date(today)+'\n\nدر ۹ لیگ منتخب امروز مسابقه‌ای پیدا نشد.'; r=requests.post(url,data={'chat_id':CHAT_ID,'text':msg},timeout=30); r.raise_for_status(); return
    poster=create_poster(all_matches); caption='⚽ بازی‌های امروز\n📅 '+format_date(today)+'\n🎯 '+persian_digits(len(all_matches))+' مسابقه\n🕐 تمامی ساعت‌ها به وقت تهران'; send_photo(poster,caption); print('DONE')

if __name__=='__main__': main()
