from datetime import datetime, timedelta

# 7 days delta outbound and incoming+5 days dela

# 30 days delta outgoing
#outgoing_v3_30_days_delta_base = datetime.today() + timedelta(days=30)
#outgoing_v3_30_days_delta = outgoing_v3_30_days_delta_base.strftime("%Y-%m-%d")
#incoming_v3_30_days_delta = (outgoing_v3_30_days_delta_base + timedelta(days=5)).strftime("%Y-%m-%d")

def make_day_params(outbound_delta, return_delta):
    outbound_base = datetime.today() + timedelta(days=outbound_delta)
    outbound = outbound_base.strftime("%Y-%m-%d")
    returning = (outbound_base + timedelta(days=return_delta)).strftime("%Y-%m-%d")
    return (outbound, returning)
