import re
from dataclasses import dataclass
from typing import List, Optional, Tuple
from google.cloud import vision
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product
from models.receipts import Receipt
from schemas.receipt import ReceiptBaseModel, ProductBaseModel


@dataclass
class Item:
    quantity: float
    unit: str
    name: str
    price: float
    sale: float


_QTY_LINE_RE = re.compile(
    r"""
    ^\s*
    (?P<qty>\d+(?:[.,]\d+)?)
    \s+
    (?P<unit>BUC\.?|KG|G|L)\b
    \s*
    (?:[xX]\s*(?P<unit_price>\d+(?:[.,]\d{1,2})?))?
    """,
    re.VERBOSE | re.IGNORECASE,
)

_DISCOUNT_LINE_RE = re.compile(
    r"\b(?:REDUCERE|DISCOUNT)\b.*(?P<amount>[-+]?\d+(?:[.,]\d{1,2}))\s*(?:LEI)?\s*$",
    re.IGNORECASE,
)

_SALE_PERCENTAGE_RE = re.compile(
    r"(?P<percent>\d+(?:[.,]\d+)?)\s*%",
    re.IGNORECASE,
)

_STOP_RE = re.compile(
    r"""
    ^\s*(
        SUBTOTAL|TOTAL|TVA\b|CARD\b|CASH\b|BON\b|FISCAL\b|DATA\b|ORA\b|
        EXCEPTATE|VAN\.?|POS:|OP:|TR:|
        C\.I\.F\.|COD\b|IDENTIFICARE|FISCALA|MUNICIPIUL|SECTOR\b|
        S\.?C\.?\s
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

_IGNORE_NAME_LINE_RE = re.compile(
    r"^\s*[-+]\s*\d+(?:[.,]\d+)?\s*LEI\b",
    re.IGNORECASE,
)
_END_OF_LINE_PRICE_RE = re.compile(
    r"\s+(?P<price>\d+(?:[.,]\d{2}))\s*[A-Z]?\s*$",
    re.IGNORECASE
)

def _norm_decimal(s: str) -> float:
    s = s.strip().replace(" ", "")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    else:
        s = s.replace(",", ".")
    return float(s)


def _clean_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+\d+(?:[.,]\d{2})\s*[A-Z]?\s*$", "", name).strip()
    name = re.sub(r"\s{2,}", " ", name)
    return name


def _extract_lines_from_vision(full_text: str) -> List[str]:
    lines = [ln.strip() for ln in full_text.splitlines()]
    return [ln for ln in lines if ln]


def _extract_prices(line: str, qty: float, unit_price_raw: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    unit_price = _norm_decimal(unit_price_raw) if unit_price_raw else None

    numbers = re.findall(r"-?\d+(?:[.,]\d{1,2})", line)
    prices: List[float] = []
    for num in numbers:
        val = _norm_decimal(num)
        if abs(val - qty) < 1e-6:
            continue
        prices.append(val)

    line_price = prices[-1] if prices else None
    if line_price is None and unit_price is not None:
        line_price = round(unit_price * qty, 2)

    return unit_price, line_price


def _parse_items_from_lines(lines: List[str]) -> List[Item]:
    items: List[Item] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _STOP_RE.search(line):
            i += 1
            continue
        discount_match = _DISCOUNT_LINE_RE.search(line)
        if discount_match and items:
            raw_amount = discount_match.group("amount")
            discount_val = _norm_decimal(raw_amount)
            if "-" not in raw_amount and discount_val > 0:
                discount_val = -discount_val
            items[-1].price = round(max(items[-1].price + discount_val, 0.0), 2)
            sale_match = _SALE_PERCENTAGE_RE.search(line)
            if sale_match:
                pct_value = _norm_decimal(sale_match.group("percent"))
                items[-1].sale = pct_value / 100.0

            i += 1
            continue
        m = _QTY_LINE_RE.match(line)
        if not m:
            i += 1
            continue

        qty = _norm_decimal(m.group("qty"))
        unit = m.group("unit").upper().rstrip(".")
        _, current_line_price = _extract_prices(line, qty, m.group("unit_price"))
        if current_line_price is None:
            current_line_price = 0.0

        i += 1
        name_parts: List[str] = []
        while i < len(lines):
            nxt = lines[i].strip()

            if _STOP_RE.search(nxt):
                break
            if _DISCOUNT_LINE_RE.search(nxt):
                break
            if _QTY_LINE_RE.match(nxt):
                break
            price_on_name_match = _END_OF_LINE_PRICE_RE.search(nxt)
            if price_on_name_match:
                found_price = _norm_decimal(price_on_name_match.group("price"))
                if found_price > 0.0:
                    current_line_price = found_price
                nxt = _END_OF_LINE_PRICE_RE.sub("", nxt)
                name_parts.append(nxt)
                i += 1
                break
            if re.match(r"^\s*-\d", nxt):
                break

            name_parts.append(nxt)
            i += 1
            if len(name_parts) >= 2:
                break

        name = _clean_name(" ".join(name_parts))
        sale_pct = 0.0
        full_item_text = line + " " + " ".join(name_parts)
        sale_match_name = _SALE_PERCENTAGE_RE.search(full_item_text)
        if sale_match_name:
            pct_value = _norm_decimal(sale_match_name.group("percent"))
            sale_pct = pct_value / 100.0

        if name:
            items.append(Item(quantity=qty, unit=unit, name=name, price=current_line_price, sale=sale_pct))

    return items


def google_ocr_full_text(image_path: str) -> str:
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)

    resp = client.document_text_detection(
        image=image,
        image_context=vision.ImageContext(language_hints=["ro", "en"]),
    )

    if resp.error.message:
        raise RuntimeError(f"Google Vision API error: {resp.error.message}")

    if not resp.full_text_annotation or not resp.full_text_annotation.text:
        return ""

    return resp.full_text_annotation.text


def extract_receipt_items(image_path: str) -> List[Item]:
    full_text = google_ocr_full_text(image_path)
    lines = _extract_lines_from_vision(full_text)
    return _parse_items_from_lines(lines)



def extract_receipt_payload(image_path: str,db:AsyncSession,transaction_id:int) -> ReceiptBaseModel:
    items = extract_receipt_items(image_path)
    total = (
        round(
            sum(
                it.price * it.quantity if it.unit == "BUC" else it.price
                for it in items
            ),
            2,
        )
        if items
        else 0.0
    )
    receipt = Receipt(
        total=total,
        transaction_id=transaction_id,
        products=[Product(
            name=it.name,
            price=it.price,
            quantity=it.quantity,
            unit=it.unit,
            sale=it.sale
        ) for it in items]
    )
    db.add(receipt)
    return ReceiptBaseModel(
        total=total,
        product=[
            ProductBaseModel(
                name=it.name,
                price=it.price,
                quantity=it.quantity,
                unit=it.unit,
                sale=it.sale,
            )
            for it in items
        ],
    )


