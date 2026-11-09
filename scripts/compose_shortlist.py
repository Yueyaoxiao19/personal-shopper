from PIL import Image, ImageDraw, ImageFont
import textwrap

F="/System/Library/Fonts/Supplemental/"
def f(name,size): return ImageFont.truetype(F+name,size)
bold=lambda s: f("Arial Bold.ttf",s); reg=lambda s: f("Arial.ttf",s)

BG=(243,241,240); CARD=(255,255,255); INK=(26,22,24); MUT=(96,90,92)
FAINT=(140,133,136); HAIR=(221,216,215)
GO=(31,107,74); GOBG=(220,239,229); NO=(163,58,43); NOBG=(247,225,221)
WINE=(110,31,53); WINEBG=(242,227,231)

rows=[
 dict(img="img/marnie.jpg", n="1. Marnie", price="CA$300", chip=("ARRIVES",GO,GOBG),
      blurb="Strapless pleated column, long sheer scarf, high slit. Closest to the Stephanie.",
      facts=[("SHIPS","Rush, 3-9 days, +CA$11. Comfortably before the 20th"),
             ("SIZE 8","In stock now"),
             ("WATCH","3D floral hem, edges toward the fluffiness you ruled out")]),
 dict(img="img/adrianna.jpg", n="2. Adrianna", price="CA$120", chip=("ARRIVES",GO,GOBG),
      blurb="One-shoulder satin, sculptural cascade, pockets. No lace, velvet, sparkle or tulle.",
      facts=[("SHIPS","Rush, 3-9 days, +CA$11. Safest delivery of the three"),
             ("SIZE 8","In stock now"),
             ("WATCH","No sheer element, so less drama than the scarf dresses")]),
 dict(img="img/sorrel.jpg", n="3. Sorrel", price="CA$84.50", chip=("FINAL SALE ONLY",WINE,WINEBG),
      blurb="Two-piece. Cowl corset with long scarf, fitted column skirt. Most architectural.",
      facts=[("SHIPS","Only clearance makes it: 3-7 days. Normal rush is 1.5-3 weeks"),
             ("SIZE 8","Available, but not a stocked rush size"),
             ("WATCH","Final sale. No returns on a dress nobody has tried on")]),
 dict(img="img/stephanie.jpg", n="Stephanie", price="CA$209", chip=("TOO LATE",NO,NOBG),
      blurb="The one you picked. Square neck, draped shoulder panels, knife-pleated skirt.",
      facts=[("SHIPS","Standard only, 2.5-4 weeks. Arrives Nov 27 - Dec 6"),
             ("WHY","Made to order. No rush option at any price"),
             ("IF","Worth it anyway if she has another formal event after the 20th")]),
]

W=1040; PAD=26; IW=200; IH=272; GAP=18
HEAD=108
H=HEAD + len(rows)*(IH+GAP) + PAD
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)

d.text((PAD,26),"BURGUNDY · FORMAL · SIZE 8 · MUST ARRIVE BEFORE 20 NOV",font=bold(13),fill=FAINT)
d.text((PAD,50),"Three that actually arrive",font=bold(34),fill=INK)

y=HEAD
for r in rows:
    d.rectangle([PAD,y,W-PAD,y+IH],fill=CARD,outline=HAIR)
    accent = r["chip"][1]
    d.rectangle([PAD,y,PAD+5,y+IH],fill=accent)
    ph=Image.open(r["img"]).convert("RGB")
    sc=max(IW/ph.width, IH/ph.height)
    ph=ph.resize((int(ph.width*sc),int(ph.height*sc)),Image.LANCZOS)
    l=(ph.width-IW)//2; t=(ph.height-IH)//2
    im.paste(ph.crop((l,t,l+IW,t+IH)),(PAD+6,y))
    x=PAD+6+IW+22; ty=y+20
    d.text((x,ty),r["n"],font=bold(27),fill=INK)
    pw=d.textlength(r["price"],font=bold(19))
    d.text((W-PAD-22-pw,ty+6),r["price"],font=bold(19),fill=INK)
    ty+=38
    label,fg,bgc=r["chip"]
    cw=d.textlength(label,font=bold(12))
    d.rounded_rectangle([x,ty,x+cw+18,ty+21],4,fill=bgc)
    d.text((x+9,ty+5),label,font=bold(12),fill=fg)
    ty+=33
    for line in textwrap.wrap(r["blurb"],74):
        d.text((x,ty),line,font=reg(15),fill=MUT); ty+=20
    ty+=8
    # label column is as wide as the widest label in THIS row, never a fixed guess
    labw=max(d.textlength(k,font=bold(11)) for k,_ in r["facts"])
    for k,v in r["facts"]:
        d.text((x,ty+2),k,font=bold(11),fill=FAINT)
        vx=x+int(labw)+14
        for i,line in enumerate(textwrap.wrap(v,max(34,int((W-PAD-22-vx)/7.4)))):
            d.text((vx,ty),line,font=reg(14),fill=INK if i==0 else MUT); ty+=18
        ty+=4
    y+=IH+GAP

im.save("shortlist.png")
print("shortlist.png", im.size)
