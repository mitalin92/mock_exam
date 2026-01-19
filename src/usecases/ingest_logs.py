from zipfile import ZipFile
import json
import pandas as pd


def main(zip_filename: str) -> None:
    log_lines = []
    malformed_lines = 0
    df = pd.DataFrame()
    with ZipFile(zip_filename) as myfile:
        for filename in myfile.namelist():
            if not filename.startswith("openai_log"):
                print("Skip the {filename}")
                continue
            with myfile.open(filename, "r") as f:
                for line in f.readlines():
                    try:
                        log_lines.append(json.loads(line))
                    except json.JSONDecodeError:
                        malformed_lines += 1

    df = pd.concat([df, pd.DataFrame(log_lines)])

    avg_latency = (
        df.groupby("api_method")["latency_ms"].mean().sort_values(ascending=False)
    )
    print(avg_latency)


if __name__ == "__main__":
    main("data/openai_logs.zip")
