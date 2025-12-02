import qrcode
import base64
from io import BytesIO

def generate_qr_code(url: str)->str:
    """
    Generates a QR code for the given URL and returns it as a Base64 encoded PNG string.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save image to a memory buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    # Encode the image data to Base64
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Return the data URI string
    return f"data:image/png;base64,{qr_base64}"
