from app.database import SessionLocal
from app.models import VoucherSequence

db = SessionLocal()

seeds = [
    # English Home
    ("english_home", 50, 300540),
    ("english_home", 100, 310460),
    ("english_home", 200, 320260),
    ("english_home", 250, 330175),

    # Penti
    ("penti", 50, 100534),
    ("penti", 100, 110515),
    ("penti", 150, 120185),
    ("penti", 200, 130164),

    # Matalan
    ("matalan", 50, 400015),
    ("matalan", 100, 410015),
    ("matalan", 200, 420015),
    ("matalan", 500, 450015),

    # OVS
    ("ovs", 50, 200105),
    ("ovs", 100, 210105),
    ("ovs", 200, 220105),
    ("ovs", 250, 230105),
    ("ovs", 500, 250002),

    # Principe
    ("principe", 100, 500020),
    ("principe", 200, 510020),
    ("principe", 500, 520020),
    ("principe", 1000, 530020),
]

for brand, amount, last in seeds:
    row = VoucherSequence(brand=brand, amount=amount, last_code=last)
    db.add(row)

db.commit()
db.close()

print("Voucher sequences were initialized successfully.")
