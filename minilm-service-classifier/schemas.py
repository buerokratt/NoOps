# schemas.py
SERVICE_SCHEMAS = {
    "common_service_weather": {
        "params": {
            "location": {"required": True, "extract": "location_gazetteer"}
        }
    },
    "common_service_motor_vehicle_tax": {
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
    "common_service_electricity_price": {
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
    "common_service_holidays": {
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
    "common_service_exchange_rate": {
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
    "common_service_parliament_votes": {
        "params": {
            "plural": {
                "required": False,
                "extract": "extract_plural_votes"
            }
        }
    }
}
