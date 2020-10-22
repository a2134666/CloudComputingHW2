from flask import Flask, render_template, request, send_file, make_response
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/hw2', methods=['GET', 'POST'])
def hw2():
    print(request.method)
    if request.method == "POST":
        if request.files:
            image1 = Image.open(request.files["image1"])
            image2 = Image.open(request.files["image2"])

            if request.form["option"] == "left":
                new_image = Image.new('RGB',(image1.size[0]+image2.size[0], max(image1.size[1],image2.size[1])), (250,250,250))
                new_image.paste(image1,(0,0))
                new_image.paste(image2,(image1.size[0],0))
            elif request.form["option"] == "right":
                new_image = Image.new('RGB',(image1.size[0]+image2.size[0], max(image1.size[1],image2.size[1])), (250,250,250))
                new_image.paste(image2,(0,0))
                new_image.paste(image1,(image2.size[0],0))
            elif request.form["option"] == "top":
                new_image = Image.new('RGB',(max(image1.size[0],image2.size[0]), image1.size[1]+image2.size[1]), (250,250,250))
                new_image.paste(image1,(0,0))
                new_image.paste(image2,(0,image1.size[1]))
            elif request.form["option"] == "bottom":
                new_image = Image.new('RGB',(max(image1.size[0],image2.size[0]), image1.size[1]+image2.size[1]), (250,250,250))
                new_image.paste(image2,(0,0))
                new_image.paste(image1,(0,image2.size[1]))

            buffered = BytesIO()
            new_image.save(buffered, format="jpeg")
            result = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return {"state":True, "result":result}
        else:
            return {"state":False, "msg":"unsupport"}
    else:
        return render_template('call_function.html')

if __name__ == '__main__':
    app.debug = True
    app.run()