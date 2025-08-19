# schemas.py
SERVICE_SCHEMAS = {
    "weather_query": {
        "params": {
            "location": {"required": True, "extract": "location_gazetteer"}
        }
    },
    "vehicle_tax_check": {
        "params": {
            "registration_number": {"required": True, "extract": "regex_plate"}
        }
    },
    "document_request": {
        "params": {
            "id_code": {"required": False, "extract": "regex_id_code"},
            "full_name": {"required": False, "extract": "regex_name"}
        }
    },
    "electricity_info": {
        "params": {
            "query_type": {  # "praegu" või "kõrge/madal"
                "required": True,
                "extract": "extract_electricity_query_type"
            },
            "direction": {  # "kõrgem", "madalam" (vaja ainult kui query_type on "kõrge/madal")
                "required": False,
                "extract": "extract_price_direction"
            }
        }
    },
    "holiday_info": {
        "params": {
            "query_time": {  # "täna", "järgmine", "eelmine", "spetsiifiline"
                "required": True,
                "extract": "extract_holiday_query_type"
            },
            "holiday_name": {
                "required": False,
                "extract": "extract_holiday_name"
            }
        }
    },
    "currency_conversion": {
        "params": {
            "source_currency": {
                "required": True,
                "extract": "extract_currency_pair"
            },
            "amount": {
                "required": False,
                "extract": "extract_amount"
            },
            "target_currency": {
                "required": True,
                "extract": "extract_currency_pair"
            }
        }
    },
    "recent_votes": {
        "params": {
            "plural": {
                "required": False,
                "extract": "extract_plural_votes"
            }
        }
    }
}
