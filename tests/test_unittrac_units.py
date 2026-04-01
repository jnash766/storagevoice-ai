from providers.unittrac.units import filter_available_units, find_unit_by_identifier


def test_filter_available_units_applies_heuristics() -> None:
    facility = {
        "id": "facility_1",
        "name": "Main",
        "sizes": [
            {
                "id": "size_1",
                "name": "10x10",
                "units": [
                    {
                        "id": "unit_1",
                        "sizeId": "size_1",
                        "identifier": "101",
                        "unitPrice": 100.0,
                        "pricingPeriod": 1,
                        "isCurrentlyActive": True,
                        "isCurrentlyLeased": False,
                        "currentStatus": 1,
                        "displayOnWebsite": True,
                    },
                    {
                        "id": "unit_2",
                        "sizeId": "size_1",
                        "identifier": "102",
                        "unitPrice": 200.0,
                        "pricingPeriod": 1,
                        "isCurrentlyActive": True,
                        "isCurrentlyLeased": True,
                        "currentStatus": 1,
                        "displayOnWebsite": True,
                    },
                ],
            }
        ],
    }

    rows = filter_available_units(facility, facility_id="facility_1", max_price=150.0)
    assert len(rows) == 1
    assert rows[0]["identifier"] == "101"


def test_find_unit_by_identifier_case_insensitive() -> None:
    facility = {
        "sizes": [
            {
                "id": "size_1",
                "name": "10x10",
                "units": [
                    {
                        "id": "unit_1",
                        "sizeId": "size_1",
                        "identifier": "Unit 001",
                    }
                ],
            }
        ]
    }
    assert find_unit_by_identifier(facility, "unit 001") is not None
    assert find_unit_by_identifier(facility, "999") is None
