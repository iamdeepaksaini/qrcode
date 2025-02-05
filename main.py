from flask import Flask, request, send_file
import qrcode
from PIL import Image
import io

app = Flask(__name__)

@app.route('/create-qr-code/', methods=['GET'])
def create_qr_code():
    # Step 1: Get user parameters from GET request
    logo_url = request.args.get('logo', '')  # Logo URL
    size = request.args.get('size', '300x300')  # Size of QR Code (default 300x300)
    colour = request.args.get('colour', 'black')  # Colour of QR Code (default black)
    data = request.args.get('data', '')  # Data to encode in QR Code

    # Step 2: Parse the size parameter (width, height)
    width, height = map(int, size.split('×'))

    # Step 3: Generate the QR code using qrcode library
    qr = qrcode.QRCode(
        version=1,  # Size of the QR Code (1 is smallest, 40 is largest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction level
        box_size=10,  # Box size of each QR block
        border=4,  # Border thickness
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Step 4: Create the QR Code image with the given colour
    qr_img = qr.make_image(fill=colour, back_color='white')

    # Step 5: Add logo if provided
    if logo_url:
        logo = Image.open(logo_url)  # Open the logo image from URL or local path
        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 5  # Resize the logo to 1/5th of QR code size
        logo = logo.resize((logo_size, logo_size))
        logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, logo_position, mask=logo.convert("RGBA").split()[3])  # Use alpha channel as mask

    # Step 6: Save the image to a bytes buffer
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Step 7: Return the image as response
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
