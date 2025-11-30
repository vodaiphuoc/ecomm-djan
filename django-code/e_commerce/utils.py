import hashlib
import qrcode
import base64
from io import BytesIO

AVATAR_COLORS = [
    '#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', 
    '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', 
    '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107', '#FF9800', 
    '#FF5722', '#795548', '#9E9E9E', '#607D8B'
]

def get_avatar_color(identifier)->str:
    """
    Takes a unique identifier (like user ID or username) and returns 
    a stable background color from the AVATAR_COLORS list.
    """
    identifier_str = str(identifier)
    
    hash_object = hashlib.sha256(identifier_str.encode())
    hex_digest = hash_object.hexdigest()
    
    hash_int = int(hex_digest[:6], 16)
    
    color_index = hash_int % len(AVATAR_COLORS)
    
    return AVATAR_COLORS[color_index]


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
