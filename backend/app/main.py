from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from .database import SessionLocal, Base, engine
from .models import Voucher, VoucherSequence
from .barcode_renderer import generate_barcode_png

import os
import zipfile
import time

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB schema ensure
Base.metadata.create_all(bind=engine)

GENERATED_DIR = "./app/generated"
os.makedirs(GENERATED_DIR, exist_ok=True)


class VoucherItem(BaseModel):
    amount: int
    quantity: int


class GenerateRequest(BaseModel):
    brand: str
    vouchers: List[VoucherItem]
    width_cm: float
    height_cm: float
    text_size: int
    show_text: bool
    stretch: bool
    bold: bool


@app.post("/generate")
async def generate_vouchers(payload: GenerateRequest):
    db = SessionLocal()

    brand = payload.brand
    vouchers = [v for v in payload.vouchers if v.quantity > 0]

    if not vouchers:
        db.close()
        raise HTTPException(status_code=400, detail="No vouchers requested")

    folder_name = f"{brand}_{int(time.time())}"
    target_folder = os.path.join(GENERATED_DIR, folder_name)
    os.makedirs(target_folder, exist_ok=True)

    filepaths: List[str] = []

    try:
        for item in vouchers:
            seq = (
                db.query(VoucherSequence)
                .filter_by(brand=brand, amount=item.amount)
                .first()
            )
            if not seq:
                raise HTTPException(
                    status_code=400,
                    detail=f"No sequence configured for {brand} {item.amount}₾",
                )

            for _ in range(item.quantity):
                seq.last_code += 1
                code_int = seq.last_code
                code_str = str(code_int)

                png_path = os.path.join(target_folder, f"{code_str}.png")
                png_no_ext = png_path[:-4]

                generate_barcode_png(
                    code_str,
                    png_no_ext,
                    width_cm=payload.width_cm,
                    height_cm=payload.height_cm,
                    text_size=payload.text_size,
                    show_text=payload.show_text,
                    stretch=payload.stretch,
                    bold=payload.bold,
                )

                voucher_row = Voucher(
                    code=code_int,
                    brand=brand,
                    amount=item.amount,
                )
                db.add(voucher_row)

                filepaths.append(png_path)

        db.commit()

    finally:
        db.close()

    # ZIP
    zip_name = f"{folder_name}.zip"
    zip_path = os.path.join(GENERATED_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w") as z:
        for f in filepaths:
            z.write(f, arcname=os.path.basename(f))

    return FileResponse(zip_path, filename=zip_name, media_type="application/zip")
