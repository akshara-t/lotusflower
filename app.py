import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from rembg import remove, new_session
import io

session = new_session()

def draw_rotated_text(base, text, position, angle, font, fill="black"):
    # Step 1: create a transparent image to hold the text
    txt_img = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_img)

    # Step 2: draw text at desired position
    draw.text(position, text, font=font, fill=fill)

    # Step 3: rotate the text image
    rotated = txt_img.rotate(angle, resample=Image.BICUBIC)

    # Step 4: paste it back onto the base image
    base.alpha_composite(rotated)
    return base

def generate_meme(face_img, name, action):
    base = Image.open("template.jpg").convert("RGBA")

    face_img = face_img.resize((500, 500))
    base.paste(face_img, (400, 200), face_img)

    draw = ImageDraw.Draw(base)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 60)
    except OSError:
        font = ImageFont.load_default()

    draw.text((875, 115), name, font=font, fill="black")

    base = draw_rotated_text(base.copy(), action, (50, 860), 7, font = font, fill="black")
    return base

st.title("lotus flower meme generator")
st.caption("i love hinduism. and also python inbuilt remove background library. ts is sick. also did i mention streamlit. streamlit is sick")
name = st.text_input("Enter a name (max 12ish characters! first name only prob works)")
action = st.text_input("Enter an action")
uploaded = st.file_uploader("Upload a face image (square images only unforch)", type=["png", "jpg", "jpeg"])

if uploaded and name and action:
    input_img = Image.open(uploaded)
    face_only = remove(input_img, session = session)

    meme = generate_meme(face_only, name, action)
    st.image(meme, caption="lmao here u go", use_container_width=True)

    # Download button
    buf = io.BytesIO()
    meme.save(buf, format="PNG")
    st.download_button("download image", buf.getvalue(), "lotus_meme.png", "image/png")