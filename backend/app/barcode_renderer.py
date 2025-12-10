from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont


def generate_barcode_png(
    code: str,
    output_path_no_ext: str,
    width_cm: float = 4.0,
    height_cm: float = 1.3,  # პრინციპში აღარ ვიყენებთ, მაგრამ ვტოვებთ სიგნატურაში
    text_size: int = 26,
    show_text: bool = True,
    stretch: bool = True,
    bold: bool = False,
):
    """
    ქმნის ბარკოდის PNG-ს:
    - სიგანე: width_cm სმ (≈ 118 px თითო სმ-ზე)
    - სიმაღლე ბარკოდის ზოლებისთვის ფიქსირებული: 40 px
    - ტექსტი ბოლოში, ცენტრში
    """

    PX_PER_CM = 118
    target_width = int(width_cm * PX_PER_CM)
    barcode_height = 90  # შენი მოთხოვნა: ფიქსირებული სიმაღლე

    writer = ImageWriter()
    options = {
        "module_width": 0.2,
        "module_height": barcode_height,
        "quiet_zone": 1,
        "write_text": False,  # ტექსტს ჩვენ დავამატებთ ხელით
    }

    # შეიქმნას ბარკოდი დროებით ფაილად
    barcode = Code128(code, writer=writer)
    filename = barcode.save(output_path_no_ext, options)

    img = Image.open(filename)

    # ჰორიზონტალური გაწელვა მთელ სიგანეზე
    if stretch:
        img = img.resize((target_width, barcode_height), Image.Resampling.NEAREST)

    # ტექსტისთვის ადგილი
    text_area = int(text_size * 2)
    final_height = barcode_height + (text_area if show_text else 0)

    # საბოლოო თეთრი კენვასი
    final_img = Image.new("RGB", (target_width, final_height), "white")
    draw = ImageDraw.Draw(final_img)

    # ბარკოდი ზედა ნაწილში
    final_img.paste(img, (0, 0))

    if show_text:
        try:
            font = ImageFont.truetype("arial.ttf", text_size)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), code, font=font)
        w = bbox[2] - bbox[0]

        # ცენტრში, ბოლოში
        x = (target_width - w) // 2
        y = final_height - text_size - 6

        draw.text(
            (x, y),
            code,
            font=font,
            fill="black",
            stroke_width=2 if bold else 0,
            stroke_fill="black",
        )

    final_img.save(filename, format="PNG")
