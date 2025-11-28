#!/usr/bin/env python3
"""Create PDF-compatible versions by removing emojis and converting to HTML"""

import re
from pathlib import Path

def remove_emojis(text):
    """Remove emoji characters for PDF compatibility"""
    # Remove common emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F525"  # fire emoji
        u"\U0001F4A1"  # lightbulb
        u"\U0001F4CD"  # location pin
        u"\U0001F4CA"  # chart
        u"\U0001F4E7"  # email
        u"\U0001F4F1"  # mobile phone
        u"\U0001F4DD"  # memo
        u"\U0001F4C8"  # chart increasing
        u"\U0001F680"  # rocket
        u"\U000023F0"  # alarm clock
        u"\U000026A0"  # warning
        u"\U00002705"  # checkmark
        u"\U0000274C"  # cross mark
        u"\U0001F3AF"  # dart
        u"\U0001F4A5"  # explosion
        u"\U0001F4E2"  # megaphone
        u"\U0001F4E3"  # postal horn
        u"\U0001F4E9"  # envelope with arrow
        u"\U0001F4E8"  # incoming envelope
        u"\U0001F4EB"  # closed mailbox
        u"\U0001F4EA"  # closed mailbox with lowered flag
        u"\U0001F4EC"  # open mailbox with raised flag
        u"\U0001F4ED"  # open mailbox with lowered flag
        u"\U0001F4EE"  # postbox
        u"\U0001F4EF"  # postal horn
        u"\U0001F4F0"  # newspaper
        u"\U0001F4F2"  # mobile phone with arrow
        u"\U0001F4F3"  # vibration mode
        u"\U0001F4F4"  # mobile phone off
        u"\U0001F4F5"  # no mobile phones
        u"\U0001F4F6"  # antenna bars
        u"\U0001F4F7"  # camera
        u"\U0001F4F8"  # camera with flash
        u"\U0001F4F9"  # video camera
        u"\U0001F4FA"  # television
        u"\U0001F4FB"  # radio
        u"\U0001F4FC"  # videocassette
        u"\U0001F4FD"  # film projector
        u"\U0001F4FE"  # film frames
        u"\U0001F4FF"  # prayer beads
        u"\U0001F500"  # twisted rightwards arrows
        u"\U0001F501"  # clockwise rightwards and leftwards open circle arrows
        u"\U0001F502"  # clockwise rightwards and leftwards open circle arrows with circled one overlay
        u"\U0001F503"  # clockwise downwards and upwards open circle arrows
        u"\U0001F504"  # anticlockwise arrows button
        u"\U0001F505"  # low brightness symbol
        u"\U0001F506"  # high brightness symbol
        u"\U0001F507"  # speaker with cancellation stroke
        u"\U0001F508"  # speaker
        u"\U0001F509"  # speaker with one sound wave
        u"\U0001F50A"  # speaker with three sound waves
        u"\U0001F50B"  # battery
        u"\U0001F50C"  # electric plug
        u"\U0001F50D"  # left-pointing magnifying glass
        u"\U0001F50E"  # right-pointing magnifying glass
        u"\U0001F50F"  # locked with ink
        u"\U0001F510"  # closed lock with key
        u"\U0001F511"  # key
        u"\U0001F512"  # lock
        u"\U0001F513"  # open lock
        u"\U0001F514"  # bell
        u"\U0001F515"  # bell with cancellation stroke
        u"\U0001F516"  # bookmark
        u"\U0001F517"  # link symbol
        u"\U0001F518"  # radio button
        u"\U0001F519"  # back with leftwards arrow above
        u"\U0001F51A"  # end with leftwards arrow above
        u"\U0001F51B"  # on with exclamation mark with left right arrow above
        u"\U0001F51C"  # soon with rightwards arrow above
        u"\U0001F51D"  # top with upwards arrow above
        u"\U0001F51E"  # no one under eighteen symbol
        u"\U0001F51F"  # keycap ten
        u"\U0001F520"  # input symbol for latin capital letters
        u"\U0001F521"  # input symbol for latin small letters
        u"\U0001F522"  # input symbol for numbers
        u"\U0001F523"  # input symbol for symbols
        u"\U0001F524"  # input symbol for latin letters
        u"\U0001F525"  # fire
        u"\U0001F526"  # electric torch
        u"\U0001F527"  # wrench
        u"\U0001F528"  # hammer
        u"\U0001F529"  # nut and bolt
        u"\U0001F52A"  # hocho
        u"\U0001F52B"  # pistol
        u"\U0001F52C"  # microscope
        u"\U0001F52D"  # telescope
        u"\U0001F52E"  # crystal ball
        u"\U0001F52F"  # six pointed star with middle dot
        u"\U0001F530"  # japanese symbol for beginner
        u"\U0001F531"  # trident emblem
        u"\U0001F532"  # black square button
        u"\U0001F533"  # white square button
        u"\U0001F534"  # large red circle
        u"\U0001F535"  # large blue circle
        u"\U0001F536"  # large orange diamond
        u"\U0001F537"  # large blue diamond
        u"\U0001F538"  # small orange diamond
        u"\U0001F539"  # small blue diamond
        u"\U0001F53A"  # up-pointing red triangle
        u"\U0001F53B"  # down-pointing red triangle
        u"\U0001F53C"  # up-pointing small red triangle
        u"\U0001F53D"  # down-pointing small red triangle
        u"\U0001F549"  # om symbol
        u"\U0001F54A"  # dove of peace
        u"\U0001F54B"  # kaaba
        u"\U0001F54C"  # mosque
        u"\U0001F54D"  # synagogue
        u"\U0001F54E"  # shinto shrine
        u"\U0001F550"  # clock face one oclock
        u"\U0001F551"  # clock face two oclock
        u"\U0001F552"  # clock face three oclock
        u"\U0001F553"  # clock face four oclock
        u"\U0001F554"  # clock face five oclock
        u"\U0001F555"  # clock face six oclock
        u"\U0001F556"  # clock face seven oclock
        u"\U0001F557"  # clock face eight oclock
        u"\U0001F558"  # clock face nine oclock
        u"\U0001F559"  # clock face ten oclock
        u"\U0001F55A"  # clock face eleven oclock
        u"\U0001F55B"  # clock face twelve oclock
        u"\U0001F55C"  # clock face one-thirty
        u"\U0001F55D"  # clock face two-thirty
        u"\U0001F55E"  # clock face three-thirty
        u"\U0001F55F"  # clock face four-thirty
        u"\U0001F560"  # clock face five-thirty
        u"\U0001F561"  # clock face six-thirty
        u"\U0001F562"  # clock face seven-thirty
        u"\U0001F563"  # clock face eight-thirty
        u"\U0001F564"  # clock face nine-thirty
        u"\U0001F565"  # clock face ten-thirty
        u"\U0001F566"  # clock face eleven-thirty
        u"\U0001F567"  # clock face twelve-thirty
        u"\U0001F5FB"  # mount fuji
        u"\U0001F5FC"  # tokyo tower
        u"\U0001F5FD"  # statue of liberty
        u"\U0001F5FE"  # silhouette of japan
        u"\U0001F5FF"  # moyai
        u"\U0001F600"  # grinning face
        u"\U0001F601"  # grinning face with smiling eyes
        u"\U0001F602"  # face with tears of joy
        u"\U0001F603"  # smiling face with open mouth
        u"\U0001F604"  # smiling face with open mouth and smiling eyes
        u"\U0001F605"  # smiling face with open mouth and cold sweat
        u"\U0001F606"  # smiling face with open mouth and tightly-closed eyes
        u"\U0001F607"  # smiling face with halo
        u"\U0001F608"  # smiling face with horns
        u"\U0001F609"  # winking face
        u"\U0001F60A"  # smiling face with smiling eyes
        u"\U0001F60B"  # face savouring delicious food
        u"\U0001F60C"  # relieved face
        u"\U0001F60D"  # smiling face with heart-shaped eyes
        u"\U0001F60E"  # smiling face with sunglasses
        u"\U0001F60F"  # smirking face
        u"\U0001F610"  # neutral face
        u"\U0001F611"  # expressionless face
        u"\U0001F612"  # unamused face
        u"\U0001F613"  # face with cold sweat
        u"\U0001F614"  # pensive face
        u"\U0001F615"  # confused face
        u"\U0001F616"  # confounded face
        u"\U0001F617"  # kissing face
        u"\U0001F618"  # face throwing a kiss
        u"\U0001F619"  # kissing face with smiling eyes
        u"\U0001F61A"  # kissing face with closed eyes
        u"\U0001F61B"  # face with stuck-out tongue
        u"\U0001F61C"  # face with stuck-out tongue and winking eye
        u"\U0001F61D"  # face with stuck-out tongue and tightly-closed eyes
        u"\U0001F61E"  # disappointed face
        u"\U0001F61F"  # worried face
        u"\U0001F620"  # angry face
        u"\U0001F621"  # pouting face
        u"\U0001F622"  # crying face
        u"\U0001F623"  # persevering face
        u"\U0001F624"  # face with look of triumph
        u"\U0001F625"  # disappointed but relieved face
        u"\U0001F626"  # frowning face with open mouth
        u"\U0001F627"  # anguished face
        u"\U0001F628"  # fearful face
        u"\U0001F629"  # weary face
        u"\U0001F62A"  # sleepy face
        u"\U0001F62B"  # tired face
        u"\U0001F62C"  # grimacing face
        u"\U0001F62D"  # loudly crying face
        u"\U0001F62E"  # face with open mouth
        u"\U0001F62F"  # hushed face
        u"\U0001F630"  # face with open mouth and cold sweat
        u"\U0001F631"  # face screaming in fear
        u"\U0001F632"  # astonished face
        u"\U0001F633"  # flushed face
        u"\U0001F634"  # sleeping face
        u"\U0001F635"  # dizzy face
        u"\U0001F636"  # face without mouth
        u"\U0001F637"  # face with medical mask
        u"\U0001F638"  # grinning cat face with smiling eyes
        u"\U0001F639"  # cat face with tears of joy
        u"\U0001F63A"  # smiling cat face with open mouth
        u"\U0001F63B"  # smiling cat face with heart-shaped eyes
        u"\U0001F63C"  # cat face with wry smile
        u"\U0001F63D"  # kissing cat face with closed eyes
        u"\U0001F63E"  # pouting cat face
        u"\U0001F63F"  # crying cat face
        u"\U0001F640"  # weary cat face
        u"\U0001F641"  # slightly frowning face
        u"\U0001F642"  # slightly smiling face
        u"\U0001F643"  # upside-down face
        u"\U0001F644"  # face with rolling eyes
        u"\U0001F645"  # face with no good gesture
        u"\U0001F646"  # face with ok gesture
        u"\U0001F647"  # person bowing deeply
        u"\U0001F648"  # see-no-evil monkey
        u"\U0001F649"  # hear-no-evil monkey
        u"\U0001F64A"  # speak-no-evil monkey
        u"\U0001F64B"  # happy person raising one hand
        u"\U0001F64C"  # person raising both hands in celebration
        u"\U0001F64D"  # person frowning
        u"\U0001F64E"  # person with pouting face
        u"\U0001F64F"  # person with folded hands
        u"\U0001F680"  # rocket
        u"\U0001F681"  # helicopter
        u"\U0001F682"  # steam locomotive
        u"\U0001F683"  # railway car
        u"\U0001F684"  # high-speed train
        u"\U0001F685"  # high-speed train with bullet nose
        u"\U0001F686"  # train
        u"\U0001F687"  # metro
        u"\U0001F688"  # light rail
        u"\U0001F689"  # station
        u"\U0001F68A"  # tram
        u"\U0001F68B"  # tram car
        u"\U0001F68C"  # bus
        u"\U0001F68D"  # oncoming bus
        u"\U0001F68E"  # trolleybus
        u"\U0001F68F"  # bus stop
        u"\U0001F690"  # minibus
        u"\U0001F691"  # ambulance
        u"\U0001F692"  # fire engine
        u"\U0001F693"  # police car
        u"\U0001F694"  # oncoming police car
        u"\U0001F695"  # taxi
        u"\U0001F696"  # oncoming taxi
        u"\U0001F697"  # automobile
        u"\U0001F698"  # oncoming automobile
        u"\U0001F699"  # recreational vehicle
        u"\U0001F69A"  # delivery truck
        u"\U0001F69B"  # articulated lorry
        u"\U0001F69C"  # tractor
        u"\U0001F69D"  # monorail
        u"\U0001F69E"  # mountain railway
        u"\U0001F69F"  # suspension railway
        u"\U0001F6A0"  # mountain cableway
        u"\U0001F6A1"  # aerial tramway
        u"\U0001F6A2"  # ship
        u"\U0001F6A3"  # rowboat
        u"\U0001F6A4"  # speedboat
        u"\U0001F6A5"  # horizontal traffic light
        u"\U0001F6A6"  # vertical traffic light
        u"\U0001F6A7"  # construction sign
        u"\U0001F6A8"  # police cars revolving light
        u"\U0001F6A9"  # triangular flag on post
        u"\U0001F6AA"  # door
        u"\U0001F6AB"  # no entry sign
        u"\U0001F6AC"  # smoking symbol
        u"\U0001F6AD"  # no smoking symbol
        u"\U0001F6AE"  # put litter in its place symbol
        u"\U0001F6AF"  # do not litter symbol
        u"\U0001F6B0"  # potable water symbol
        u"\U0001F6B1"  # non-potable water symbol
        u"\U0001F6B2"  # bicycle
        u"\U0001F6B3"  # no bicycles
        u"\U0001F6B4"  # bicyclist
        u"\U0001F6B5"  # mountain bicyclist
        u"\U0001F6B6"  # pedestrian
        u"\U0001F6B7"  # no pedestrians
        u"\U0001F6B8"  # children crossing
        u"\U0001F6B9"  # mens symbol
        u"\U0001F6BA"  # womens symbol
        u"\U0001F6BB"  # restroom
        u"\U0001F6BC"  # baby symbol
        u"\U0001F6BD"  # toilet
        u"\U0001F6BE"  # wc
        u"\U0001F6BF"  # shower
        u"\U0001F6C0"  # bath
        u"\U0001F6C1"  # bathtub
        u"\U0001F6C2"  # passport control
        u"\U0001F6C3"  # customs
        u"\U0001F6C4"  # baggage claim
        u"\U0001F6C5"  # left luggage
        u"\U0001F6CB"  # couch and lamp
        u"\U0001F6CC"  # sleeping accommodation
        u"\U0001F6CD"  # shopping bags
        u"\U0001F6CE"  # bellhop bell
        u"\U0001F6CF"  # bed
        u"\U0001F6D0"  # place of worship
        u"\U0001F6D1"  # octagonal sign
        u"\U0001F6D2"  # shopping trolley
        u"\U0001F6D5"  # hindu temple
        u"\U0001F6D6"  # hut
        u"\U0001F6D7"  # elevator
        u"\U0001F6DD"  # playground slide
        u"\U0001F6DE"  # wheel
        u"\U0001F6DF"  # ring buoy
        u"\U0001F6E0"  # hammer and wrench
        u"\U0001F6E1"  # shield
        u"\U0001F6E2"  # oil drum
        u"\U0001F6E3"  # motorway
        u"\U0001F6E4"  # railway track
        u"\U0001F6E5"  # motor boat
        u"\U0001F6E9"  # small airplane
        u"\U0001F6EB"  # airplane departure
        u"\U0001F6EC"  # airplane arriving
        u"\U0001F6F0"  # satellite
        u"\U0001F6F3"  # passenger ship
        u"\U0001F6F4"  # scooter
        u"\U0001F6F5"  # motor scooter
        u"\U0001F6F6"  # canoe
        u"\U0001F6F7"  # sled
        u"\U0001F6F8"  # flying saucer
        u"\U0001F6F9"  # skateboard
        u"\U0001F6FA"  # auto rickshaw
        u"\U0001F6FB"  # pickup truck
        u"\U0001F6FC"  # roller skate
        u"\U0001F7E0"  # large orange circle
        u"\U0001F7E1"  # large yellow circle
        u"\U0001F7E2"  # large green circle
        # Add more emoji ranges as needed
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def create_html_for_pdf(md_content, title):
    """Create HTML version for PDF printing"""
    import markdown
    
    html_body = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
        }}
        h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 30px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #6b7280;
            margin-top: 25px;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
        }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #667eea;
        }}
        blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin-left: 0;
            color: #6b7280;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #f9fafb;
            font-weight: 600;
        }}
        @media print {{
            body {{
                padding: 20px;
            }}
            h1, h2 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""
    return html

def main():
    export_dir = Path("webinar-export")
    pdf_dir = export_dir / "pdf"
    
    print("Creating PDF-compatible versions...")
    
    for md_file in pdf_dir.glob("*.md"):
        print(f"Processing {md_file.name}...")
        
        # Read original
        content = md_file.read_text(encoding='utf-8')
        
        # Create clean version without emojis
        clean_content = remove_emojis(content)
        clean_md = pdf_dir / f"{md_file.stem}-clean.md"
        clean_md.write_text(clean_content, encoding='utf-8')
        
        # Create HTML version
        try:
            import markdown
            html_content = create_html_for_pdf(clean_content, md_file.stem.replace('-', ' ').title())
            html_file = pdf_dir / f"{md_file.stem}.html"
            html_file.write_text(html_content, encoding='utf-8')
            print(f"   Created HTML: {html_file.name}")
        except ImportError:
            print(f"    markdown library not available, skipping HTML")
        
        # Try PDF conversion with clean version
        try:
            import subprocess
            pdf_file = pdf_dir / f"{md_file.stem}.pdf"
            result = subprocess.run(
                ['pandoc', str(clean_md), '-o', str(pdf_file), '-f', 'markdown', '-t', 'pdf'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if pdf_file.exists():
                print(f"   Created PDF: {pdf_file.name}")
            else:
                print(f"    PDF creation failed, HTML available for printing")
        except Exception as e:
            print(f"    PDF conversion skipped: {e}")
    
    print("\n PDF-compatible versions created!")
    print(" HTML files can be opened in browser and printed to PDF")

if __name__ == "__main__":
    main()

