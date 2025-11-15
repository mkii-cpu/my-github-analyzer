import json
import pandas as pd

def load_raw_json(path):
    """Load JSON GitHub data"""
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def json_to_dfs(raw):
    """Convert JSON → DataFrames"""
    profile = raw.get('profile', {})
    repos = raw.get('repos', [])

    profile_df = pd.DataFrame([{
        'login': profile.get('login'),
        'name': profile.get('name'),
        'followers': profile.get('followers'),
        'following': profile.get('following'),
        'public_repos': profile.get('public_repos'),
        'created_at': profile.get('created_at')
    }])

    repos_df = pd.DataFrame(repos)
    return profile_df, repos_df


def clean_repos_df(repos_df):
    """Clean repo data"""
    date_columns = ['created_at', 'updated_at', 'pushed_at']
    for col in date_columns:
        if col in repos_df:
            repos_df[col] = pd.to_datetime(repos_df[col], errors='coerce')

    repos_df['language'] = repos_df['language'].fillna('Unknown')

    numeric_cols = ['stargazers_count', 'forks_count', 'watchers_count', 'size']
    for col in numeric_cols:
        if col in repos_df.columns:
            repos_df[col] = repos_df[col].fillna(0).astype(int)

    return repos_df


def convert_timestamps_to_strings(df):
    """Convert all Timestamp columns to strings"""
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)
    return df


def build_summary(profile_df, repos_df):
    """Convert timestamps → strings before JSON save"""
    profile_df = convert_timestamps_to_strings(profile_df)
    repos_df = convert_timestamps_to_strings(repos_df)

    summary = {
        "profile": profile_df.to_dict(orient="records")[0],
        "repos": repos_df.to_dict(orient="records")
    }
    return summary


if __name__ == "__main__":
    print("Processing GitHub data...")

    raw_data = load_raw_json("sample_raw.json")
    profile_df, repos_df = json_to_dfs(raw_data)
    repos_df = clean_repos_df(repos_df)

    summary = build_summary(profile_df, repos_df)

    with open("processed_data.json", "w", encoding="utf-8") as output:
        json.dump(summary, output, indent=4)

    print("Processed data saved to processed_data.json 🎉")
