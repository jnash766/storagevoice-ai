"""Derive availability from UnitTrac facility details (sizes -> units)."""

from __future__ import annotations

from typing import Any


def _as_bool(value: Any) -> bool:
    return bool(value)


def _as_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def iter_units_from_facility(facility: dict[str, Any]) -> list[dict[str, Any]]:
    sizes = facility.get("sizes") or []
    if not isinstance(sizes, list):
        return []
    out: list[dict[str, Any]] = []
    for size in sizes:
        if not isinstance(size, dict):
            continue
        size_id = size.get("id")
        size_name = size.get("name")
        units = size.get("units") or []
        if not isinstance(units, list):
            continue
        for unit in units:
            if not isinstance(unit, dict):
                continue
            out.append(
                {
                    "unit": unit,
                    "size_id": size_id,
                    "size_name": size_name,
                    "size": size,
                }
            )
    return out


def is_unit_available(unit: dict[str, Any]) -> bool:
    """Heuristic: active, rentable, not leased."""
    if not _as_bool(unit.get("isCurrentlyActive", True)):
        return False
    if _as_bool(unit.get("isCurrentlyLeased")):
        return False
    status = _as_int(unit.get("currentStatus"))
    if status is not None and status != 1:
        return False
    return True


def normalize_unit_row(
    *,
    facility_id: str,
    facility_name: str | None,
    size_id: Any,
    size_name: Any,
    unit: dict[str, Any],
) -> dict[str, Any]:
    return {
        "facility_id": facility_id,
        "facility_name": facility_name,
        "unit_id": unit.get("id"),
        "size_id": size_id,
        "size_name": size_name,
        "identifier": unit.get("identifier"),
        "unit_price": _as_float(unit.get("unitPrice")),
        "pricing_period": _as_int(unit.get("pricingPeriod")),
        "is_currently_active": _as_bool(unit.get("isCurrentlyActive")),
        "is_currently_leased": _as_bool(unit.get("isCurrentlyLeased")),
        "current_status": _as_int(unit.get("currentStatus")),
        "display_on_website": _as_bool(unit.get("displayOnWebsite")),
    }


def filter_available_units(
    facility: dict[str, Any],
    *,
    facility_id: str,
    max_price: float | None = None,
    size_name_substring: str | None = None,
) -> list[dict[str, Any]]:
    facility_name = facility.get("name") if isinstance(facility, dict) else None
    rows: list[dict[str, Any]] = []
    for item in iter_units_from_facility(facility if isinstance(facility, dict) else {}):
        unit = item["unit"]
        if not is_unit_available(unit):
            continue
        price = _as_float(unit.get("unitPrice"))
        if max_price is not None and price is not None and price > max_price:
            continue
        sname = item.get("size_name")
        if size_name_substring and isinstance(sname, str):
            if size_name_substring.lower() not in sname.lower():
                continue
        rows.append(
            normalize_unit_row(
                facility_id=facility_id,
                facility_name=facility_name if isinstance(facility_name, str) else None,
                size_id=item.get("size_id"),
                size_name=item.get("size_name"),
                unit=unit,
            )
        )
    return rows


def find_unit_by_identifier(facility: dict[str, Any], unit_identifier: str) -> dict[str, Any] | None:
    target = unit_identifier.strip().lower()
    if not target:
        return None
    for item in iter_units_from_facility(facility if isinstance(facility, dict) else {}):
        unit = item["unit"]
        ident = unit.get("identifier")
        if isinstance(ident, str) and ident.strip().lower() == target:
            return unit
    return None
