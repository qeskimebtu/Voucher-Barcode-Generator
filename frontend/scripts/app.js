// თანხები ბრენდის მიხედვით
const brandAmounts = {
    english_home: [50, 100, 200, 250],
    penti: [50, 100, 150, 200],
    matalan: [50, 100, 200, 500],
    ovs: [50, 100, 200, 250, 500],
    principe: [100, 200, 500, 1000],
};

const brandNames = {
    english_home: "English Home",
    penti: "Penti",
    matalan: "Matalan",
    ovs: "OVS",
    principe: "Principe",
};

function loadAmounts() {
    const brand = document.getElementById("brand").value;
    const container = document.getElementById("amountRows");
    container.innerHTML = "";

    if (!brand || !brandAmounts[brand]) {
        return;
    }

    const amounts = brandAmounts[brand];

    const title = document.createElement("div");
    title.textContent = "Voucher amounts and quantities:";
    title.style.fontSize = "14px";
    title.style.fontWeight = "600";
    title.style.marginBottom = "4px";
    container.appendChild(title);

    amounts.forEach((amount) => {
        const row = document.createElement("div");
        row.className = "amount-row";

        const label = document.createElement("span");
        label.className = "amount-label";
        label.textContent = `${amount} ₾`;

        const input = document.createElement("input");
        input.type = "number";
        input.min = "0";
        input.value = "0";
        input.className = "amount-qty";
        input.dataset.amount = amount;

        row.appendChild(label);
        row.appendChild(input);
        container.appendChild(row);
    });
}

async function generateVouchers() {
    const brand = document.getElementById("brand").value;
    if (!brand) {
        alert("გთხოვ აირჩიო ბრენდი.");
        return;
    }

    const qtyInputs = document.querySelectorAll(".amount-qty");
    const vouchers = [];

    qtyInputs.forEach((input) => {
        const qty = parseInt(input.value);
        const amount = parseInt(input.dataset.amount);
        if (!isNaN(qty) && qty > 0) {
            vouchers.push({ amount, quantity: qty });
        }
    });

    if (vouchers.length === 0) {
        alert("უნდა მიუთითო მაინც ერთი თანხა და რაოდენობა (> 0).");
        return;
    }

    const width_cm = parseFloat(document.getElementById("widthCm").value);
    const height_cm = parseFloat(document.getElementById("heightCm").value);
    const text_size = parseInt(document.getElementById("textSize").value);

    const show_text =
        document.querySelector('input[name="showText"]:checked').value === "yes";
    const stretch =
        document.querySelector('input[name="stretch"]:checked').value === "yes";
    const bold =
        document.querySelector('input[name="bold"]:checked').value === "yes";

    const payload = {
        brand,
        vouchers,
        width_cm,
        height_cm,
        text_size,
        show_text,
        stretch,
        bold,
    };

    const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        alert("Server error: " + response.status);
        return;
    }

    // ZIP ჩამოტვირთვა
    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = `${brand}_vouchers.zip`;
    link.click();

    // წარმატების შეტყობინება
    const summary = vouchers
        .map((v) => `${v.amount}₾ x ${v.quantity}`)
        .join(", ");

    const brandLabel = brandNames[brand] || brand;
    alert(
        `წარმატებით დაგენერირდა ${brandLabel} ბრენდის ვაუჩერის ბარკოდები: ${summary}`
    );
}
