import os
import pandas as pd
import json
from openai import OpenAI  # We use the OpenAI library structure as it is fully compatible with Ollama's API route

# Configure to point to your remote Ollama GPU server over ZeroTier
REMOTE_OLLAMA_HOST = "http://10.22.39.192:11434/v1"
MODEL_NAME = "qwen2.5vl:latest" # Or your specific Qwen model tag (e.g., qwen2.5:7b, qwen2.5-coder)

client = OpenAI(
    base_url=REMOTE_OLLAMA_HOST,
    api_key="ollama",  # Ollama doesn't require a real key, but a placeholder string prevents library validation errors
    timeout=120.0      # Generous timeout for remote processing over the network
)

def analyze_marketing_campaigns_local_ai(csv_path: str):
    print("🔄 [STAGE 1] Reading and computing marketing KPIs...")
    if not os.path.exists(csv_path):
        print(f"❌ Error: Cannot find file at {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    
    # Calculate performance metrics
    df['CTR_percent'] = (df['clicks'] / df['impressions']) * 100
    df['CPC'] = df['spend'] / df['clicks']
    df['Conversion_Rate_percent'] = (df['conversions'] / df['clicks']) * 100
    df['ROAS'] = df['revenue'] / df['spend']
    df = df.round({'CTR_percent': 2, 'CPC': 2, 'Conversion_Rate_percent': 2, 'ROAS': 2})
    
    # Extract structural performance outliers
    top_performers = df.nlargest(2, 'ROAS')[['campaign_name', 'channel', 'spend', 'ROAS', 'Conversion_Rate_percent']].to_dict(orient='records')
    bottom_performers = df.nsmallest(2, 'ROAS')[['campaign_name', 'channel', 'spend', 'ROAS', 'Conversion_Rate_percent']].to_dict(orient='records')
    
    analysis_payload = {
        "overall_summary": {
            "total_budget_spent": float(df['spend'].sum()),
            "total_revenue_generated": float(df['revenue'].sum()),
            "blended_roas": round(float(df['revenue'].sum()) / float(df['spend'].sum()), 2)
        },
        "top_performing_campaigns": top_performers,
        "underperforming_campaigns": bottom_performers
    }
    
    print(f"📡 [STAGE 2] Streaming telemetry context to remote Qwen engine at {REMOTE_OLLAMA_HOST}...")
    
    # Precise operational prompt structure for Qwen models
    prompt = (
        "You are an expert Marketing Data Analyst. Analyze this campaign metrics JSON structure:\n"
        f"{json.dumps(analysis_payload, indent=2)}\n\n"
        "Generate a structured analytics response. Return ONLY a valid raw JSON object matching this exact schema "
        "with no markdown formatting or backticks: "
        "{\n"
        "  \"executive_summary\": \"string\",\n"
        "  \"success_factors\": \"string\",\n"
        "  \"corrective_actions\": \"string\",\n"
        "  \"budget_reallocation\": \"string\"\n"
        "}"
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precise data analysis tool that outputs strict, raw JSON objects matching the user's schema perfectly. Do not include markdown wraps like ```json or any conversational introductory text."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}  # Forces Ollama to enforce valid JSON generation syntax
        )
        
        model_output = response.choices[0].message.content.strip()
        
        # Parse the JSON string to ensure structural validity
        parsed_insights = json.loads(model_output)
        print("✅ [STAGE 3] Remote GPU Response Received and Parsed Cleanly!")
        
        final_report = {
            "performance_metrics": df.to_dict(orient='records'),
            "ai_insights": parsed_insights
        }
        
        # Save output into your workspace directory
        os.makedirs("Work on", exist_ok=True)
        output_json_path = os.path.join("Work on", "campaign_analysis_report.json")
        
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=2)
            
        print(f"📝 [STAGE 4] Success! Strategic insights exported safely to: {output_json_path}")
        
    except json.JSONDecodeError:
        print("❌ Error: Remote model did not return a clean JSON structure. Raw response was:")
        print(model_output)
    except Exception as e:
        print(f"❌ System Exception occurred during processing: {str(e)}")

if __name__ == "__main__":
    # Make sure 'campaign_data.csv' is generated in this folder before running!
    analyze_marketing_campaigns_local_ai("campaign_data.csv")