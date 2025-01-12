import qrcode
import time
import os
import requests # type: ignore
from PIL import Image, ImageShow # type: ignore

def is_site_reachable(url):
    try:
        # send a GET request
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
    
def is_valid_color(color):
    # List of valid color
    valid_colors = [
        "black", "white", "red", "blue", "green", "yellow", "cyan", "magenta", "gray",
        "#FF5733", "#C70039", "#900C3F", "#581845",  
        (255, 0, 0), (0, 255, 0), (0, 0, 255)  
    ]
    return color in valid_colors 

def is_valid_format(format):
    # List of valid format
    valid_formats = ["PNG", "JPEG", "JPG", "BMP", "GIF", "TIFF", "WEBP", "PDF", "EPS"]
    return format.upper() in valid_formats


while True:
    data = input("Enter the text or URL: ").strip()
    if not data.startswith(('http://', 'https://')):
        data = 'http://' + data

    if is_site_reachable(data):
        break
    else:
        print("Invalid URL! Please retry.")

filename =  input("Enter the filename (without extension): ").strip()


while True: 
    resp = input("Do you want save the QR_Code in the default path C:/Users/Salvatore/Desktop/QrCodeGenerati (y/n)? : ").strip().upper()
    if resp == 'Y':
        path = "C:/Users/Salvatore/Desktop/QrCodeGenerati"
        break
    elif resp =='N':
        correct_path=True 
        while correct_path is True:
            path = input("Write the path (e.g.  C:/path/to/folder): ").strip()
            if not os.path.isdir(path):
                print("The provided directory does not exist. Retry.")
            else: 
                correct_path=False    
        break
    else:
        print("Please write a correct answer (y/n) \n")


while True:
    fill_color = input("Enter the fill color (default black): ").strip() or "black"
    if is_valid_color(fill_color):
        break
    else:
        print("Invalid color! Please Enter a valid color.")

while True:
    back_color = input("Enter the background color (default white): ").strip() or "white"
    if is_valid_color(back_color):
        break
    else:
        print("Invalid color! Please Enter a valid color.")

while True:
    box_size = input("Enter box size (default 10): ").strip() or "10"
    try:
        box_size = int(box_size)
        break
    except ValueError:
        print("Invalid input! Please enter a valid number,")


add_logo = False
logo = None
while True:
    resp2 = input("Do you want add a logo to the center of the QR Code (y/n)? : ").strip().upper()
    if resp2 == "Y":
        add_logo = True
        while add_logo is True:
            logo_path = input("Enter the path of the logo image: ").strip()
            if logo_path and os.path.exists(logo_path):
                logo = Image.open(logo_path)
                add_logo = False
            else:
                print("The provided directory does not exist. Retry.")        
        break
    elif resp2 == "N":
        break
    else: 
        print("Please enter a valid response!")


qr = qrcode.QRCode(box_size=box_size, border=4)
qr.add_data(data)
image = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

if logo:
    qr_width, qr_height = image.size
    logo_size = int(qr_width * 0.15) 
    logo = logo.convert("RGBA")
     
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_alpha = logo.split()[3]

    x_offset = (qr_width - logo_size) // 2
    y_offset = (qr_height - logo_size) // 2
    image.paste(logo, (x_offset, y_offset), mask=logo_alpha)


while True:
    format = input("Enter image format (default PNG): ").strip() or "PNG"
    if is_valid_format(format):
        break
    else:
        print("Invalid format! Please enter a valid format.")


name_with_format = filename+"."+format
file_path = os.path.join(path,name_with_format)


image.save(file_path, format=format)

print(f"QR code saved as {filename}.{format} !")
time.sleep(2)

while True:
    view_image = input("Do you want to view the QR code preview? (y/n): ").strip().upper()
    if view_image == 'Y':
        ImageShow.show(image)
        print("It was a pleasure to serve you")
        time.sleep(2)
        break
    elif view_image == 'N':
        print("Ok, you will find the QR Code in the indicated directory! ")
        time.sleep(2)
        break
    else:
        print("Please enter a valid response")



