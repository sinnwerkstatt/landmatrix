__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class OldData:

    URL_VALUES = {
        '/api/statistics.json':
            {"total": {"acquired_land": 0, "acquired_africa": 0, "deals": 0, "hectares": 0, "year": 0, "investor_account": "30"}},
        '/api/statistics.json?deal_scope=transnational&negotiation_status=failed&negotiation_status=intended&negotiation_status=concluded':
            {"concluded": {"deals": 1046, "hectares": 38243154.0, "deals_percentage": 79.0, "hectares_percentage": 62.0}, "failed": {"deals": 86, "hectares": 7443148.0, "deals_percentage": 6.0, "hectares_percentage": 12.0}, "total": {"acquired_land": 93, "acquired_africa": 260, "deals": 1328, "hectares": 62021259.0, "year": 2000, "investor_account": "30"}, "intended": {"deals": 196, "hectares": 16334957.0, "deals_percentage": 15.0, "hectares_percentage": 26.0}},
        '/api/latest_deals.json?limit=3&deal_scope=transnational&negotiation_status=failed&negotiation_status=intended&negotiation_status=concluded':
            [{"timestamp": "23 March 2015 12:01", "state": "overwritten", "deal_id": 3858, "target_country": "Sri Lanka"}, {"timestamp": "23 March 2015 11:26", "state": "overwritten", "deal_id": 404, "target_country": "Philippines"}, {"timestamp": "23 March 2015 09:57", "state": "overwritten", "deal_id": 4630, "target_country": "Nicaragua"}]
    }