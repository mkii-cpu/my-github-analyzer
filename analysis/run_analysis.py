import json
from data_processing import load_raw_json, json_to_dfs, clean_repos_df, build_summary

def run_analysis():
    print("Loading raw GitHub data...")
    raw_data = load_raw_json("sample_raw.json")

    print("Converting JSON → DataFrames...")
    profile_df, repos_df = json_to_dfs(raw_data)

    print("Cleaning repository data...")
    repos_df = clean_repos_df(repos_df)

    print("Building summary...")
    summary = build_summary(profile_df, repos_df)

    print("Saving processed data...")
    with open("processed_data.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    print("✔ Analysis complete! processed_data.json generated successfully.")

if __name__ == "__main__":
    run_analysis()
