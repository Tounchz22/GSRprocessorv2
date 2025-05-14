#Import Libraries

import  streamlit as st
import pandas as pd
import plotly.express as px
import  seaborn as  sns
import  altair as  alt
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from io import BytesIO

from datetime import datetime

#config the page width
st.set_page_config(page_title="Home",page_icon="",layout="wide")
st.title(" :bar_chart: GSR Processor")

#load data set
#df=pd.read_excel("data.xlsx")
#st.dataframe(df,use_container_width=True)

#side bar
#st.sidebar.image("")

#sidebar date picker
with st.sidebar:
    st.title("Select Date Range")
    start_date=st.date_input(label="Start Date")

with st.sidebar:
    #st.title("Select Date Range")
    end_date=st.date_input(label="End Date")

st.error(" you have choosen analytics from: "+ str(start_date) +" to" + str(end_date))

#df2=df[(df["OrderDate"]>=str(start_date))& (df["OrderDate"]<= str(end_date))]


uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])


if uploaded_file:
    # Load file
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    df["Month"] = pd.to_datetime(df["Month"], errors='coerce', dayfirst=True)
    st.dataframe(df)

    # Prepare new rows
    new_rows = []

    for _, row in df.iterrows():
        shared_data = {
            "NEW TERRITORY CODE": row["NEW TERRITORY CODE"],
            "ID NO.": row["ID NO."],
            "FULL NAME": row["FULL NAME"],
            "ROLE": row["ROLE"],
            "SQUAD": row["SQUAD"],
            "TRIBE": row["TRIBE"],
            "Month": row["Month"]
        }

        # Ret Baseline row
        baseline_row = shared_data.copy()
        baseline_row["Target"] = row["BASE TARGET"]
        baseline_row["Metric"] = "Base"
        baseline_row["Actual"] = row["Ret Baseline"]
        new_rows.append(baseline_row)

        # RET IFRS row
        ifrs_row = shared_data.copy()
        ifrs_row["Target"] = row["IFRS BASELINE"]
        ifrs_row["Metric"] = "IFRS Baseline"
        ifrs_row["Actual"] = row["RET IFRS"]
        new_rows.append(ifrs_row)

         # ACQUI IFRS row
        Acqui_ifrs_row = shared_data.copy()
        Acqui_ifrs_row["Target"] = row["IFRS ACQUI"]
        Acqui_ifrs_row["Metric"] = "ACQUI IFRS"
        Acqui_ifrs_row["Actual"] = row["ACQUI IFRS"]
        new_rows.append(Acqui_ifrs_row)

        # ACQUI row  done
        Acqui_row = shared_data.copy()
        Acqui_row["Target"] = row["ACQUI TARGET"]
        Acqui_row["Metric"] = "Acqui"
        Acqui_row["Actual"] = row["Acqui"]
        new_rows.append(Acqui_row)

        # CHURN row
        Churn_row = shared_data.copy()
        Churn_row["Target"] = row["CHURN TARGET"]
        Churn_row["Metric"] = "Churn"
        Churn_row["Actual"] = row["CHURN"]
        new_rows.append(Churn_row)

        # Total GSR row
        TotalGSR_row = shared_data.copy()
        TotalGSR_row["Target"] = row["CHURN TARGET"]
        TotalGSR_row["Metric"] = "Total GSR"
        TotalGSR_row["Actual"] = row["TOTAL"]
        new_rows.append(TotalGSR_row)

    # Create new dataframe
    final_df = pd.DataFrame(new_rows)

    st.subheader("Processed Data")
    st.dataframe(final_df)

    # Download button
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Processed')
    st.download_button(
        label="📥 Download Excel",
        data=output.getvalue(),
        file_name="GSR_Processed.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
