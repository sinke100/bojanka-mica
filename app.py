from flask import Flask, request, render_template
from io import BytesIO as by
import PIL.Image as im
from base64 import b64encode as enc

app = Flask(__name__)
app.static_folder = '.'
app.template_folder = '.'
#poredak_p = ['pozadina','obrub','šare','krzno','uši','oči','zjenice','krzno2','nos']
img = im.open('mica_p.png')
w,h = img.size
img_list = list(img.getdata())
prefix = 'data:image/png;base64,'

def uri(x):
    x = enc(x).decode()
    return prefix+x

def png(x):
    with by() as output:
        x.save(output, 'PNG')
        slika = output.getvalue()
    return slika

def return_palette(info):
    palette = [[int(i[j:j+2],16) for j in range(1,len(i),2)] for i in info.values()]
    palette = [i for t in palette for i in t]
    return bytes(palette)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post-colors', methods=['POST'])
def post_colors():
    colors = dict(request.form)
    colors_list = list(colors.keys())
    transparency = True if 'transparency' in colors_list else False
    if transparency: colors.pop('transparency')
    palette = return_palette(colors)
    img_new = im.new('P',(w,h))
    img_new.putpalette(palette)
    img_new.putdata(img_list)
    if transparency: img_new.info['transparency'] = bytes([0])
    slika = png(img_new)
    slika_uri = uri(slika)
    return slika_uri

if __name__ == '__main__':
    app.run(host='0.0.0.0')
