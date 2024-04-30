import pandas as pd

raw_path = "examples/qa_example.csv"
save_path = "data/know.csv"

df = pd.read_csv(raw_path, sep="\t")
df["Document"] = "Question\n" + df["Question"] + "\n\nAnswer\n" + df["Answer"]

df.to_csv(save_path, index=False)
