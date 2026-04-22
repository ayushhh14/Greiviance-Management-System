import pandas as pd

def create_dataframe(data):
    if len(data) == 0:
        return pd.DataFrame()

    if len(data[0]) == 9:
        return pd.DataFrame(data, columns=[
            "ID","Name","Email","Account",
            "Complaint","Department","Priority","Status","Created"
        ])
    else:
        return pd.DataFrame(data, columns=[
            "ID","Name","Email","Account",
            "Complaint","Department","Priority","Status"
        ])