import pandas as pd

# Mock marketing campaign metrics dataset
data = {
    'campaign_id': [f'CMP_{i:03d}' for i in range(1, 11)],
    'campaign_name': ['Summer Sale Meta', 'Google Search Brand', 'LinkedIn B2B Outreach', 
                     'Retargeting Display', 'Newsletter Blast Q2', 'Influencer Pack Tech', 
                     'Google Shopping Apparel', 'Meta Lookalike Audience', 'YouTube Pre-Roll Tech', 'X Promo Devs'],
    'channel': ['Meta', 'Google Search', 'LinkedIn', 'Display', 'Email', 'Influencer', 'Google Shopping', 'Meta', 'YouTube', 'X'],
    'spend': [5000, 12000, 8500, 3100, 450, 15000, 9200, 6000, 11000, 2500],
    'impressions': [250000, 450000, 80000, 190000, 35000, 600000, 310000, 280000, 850000, 120000],
    'clicks': [7500, 22000, 1200, 2100, 1800, 18000, 14000, 8900, 9500, 3100],
    'conversions': [180, 850, 32, 45, 95, 210, 410, 290, 110, 65],
    'revenue': [9000, 42500, 4800, 2100, 5700, 16800, 24600, 17400, 8800, 3900]
}

df = pd.DataFrame(data)
df.to_csv('campaign_data.csv', index=False)
print("📊 Generated 'campaign_data.csv' cleanly in your directory!")