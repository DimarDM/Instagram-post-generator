from PIL import Image,ImageDraw,ImageFont,ImageFilter
import requests
from io import BytesIO
import json

#handle inputs
slogan =input('Slogan: ') 
page= input('Page : ')
#how much percent of the image the logo will be
logo_percentage=1.3


def handle_pexels_request(search):
    url = 'https://api.pexels.com/v1/search?page='+page+'&query='+search+'&per_page=1'
    headers = {'Authorization': '563492ad6f917000010000014159e93d4ac4460c9389a5e07f083867'}
    r = requests.get(url, headers=headers)
    response = json.loads(r.text)
    original_photo = response['photos'][0]['src']['original']
    return original_photo

#get pexels images
response = requests.get(handle_pexels_request('software'))
#create a new image
img =Image.open(BytesIO(response.content))
img_w,img_h = img.size

# Paste blurred region and save result
#handling bottom right logo
logo = Image.open('./woodevia1.jpg','r')
logo = logo.resize((int(logo.size[0]*logo_percentage),int(logo.size[1]*logo_percentage)),Image.ANTIALIAS)
logo_w,logo_h = logo.size

#handle text
draw = ImageDraw.Draw(img)

#rect dimensions
rect_wstart=0.1*img_w
rect_w = img_w-(2*0.1*img_w)
rect_hstart=0.45*img_h
rect_h = img_h-(2*0.45*img_h)


#rectangle.rectangle([rect_wstart,rect_hstart,0.9*img_w,img_h-rect_hstart],fill="black")
# Blur image-----------------------------------------------
# Create rectangle mask

mask = Image.new('L', img.size, 0)
draw2 = ImageDraw.Draw(mask)

draw2.rectangle([rect_wstart,rect_hstart,0.9*img_w,img_h-rect_hstart], fill=255)
mask.save('mask.png')
# Blur image
blurred = img.filter(ImageFilter.GaussianBlur(20))

# Paste blurred region and save result
img.paste(blurred, mask=mask)
# -----------------------------------------------------------

# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("Jaapokki-Regular.otf", img_w//18)
font_w, font_h = draw.textsize(slogan)
font_w = font.getsize(slogan)[0]
font_h = font.getsize(slogan)[1]

draw.text((rect_wstart+(rect_w-font_w)/2,rect_hstart),slogan,(255,255,255),font=font)

#positioning my logo
offset = (img_w-logo_w,img_h-logo_h)
#mergin logo
img.paste(logo,offset)
#saving image and show it
img.save('dimar.png')
img.show()
print('Done')
