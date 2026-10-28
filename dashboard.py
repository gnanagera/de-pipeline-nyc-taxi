import os
import pandas as pd
import streamlit as st
from databricks import sql

st.set_page_config(page_title="NYC Taxi Dashboard", layout="wide")


@st.cache_data(ttl=600)
def load_data() -> pd.DataFrame:
    with sql.connect(
        server_hostname=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM workspace.analytics.fct_daily_revenue ORDER BY pickup_date"
            )
            return cur.fetchall_arrow().to_pandas()


df = load_data()
df["pickup_date"] = pd.to_datetime(df["pickup_date"])

st.title("NYC Yellow Taxi: Daily Revenue")
c1, c2, c3 = st.columns(3)
c1.metric("Total trips", f"{int(df['trips'].sum()):,}")
c2.metric("Total revenue", f"${df['revenue'].sum():,.0f}")
c3.metric("Avg trip distance (mi)", f"{df['avg_distance'].mean():.2f}")

st.subheader("Revenue by day")
st.line_chart(df, x="pickup_date", y="revenue")
st.subheader("Trips by day")
st.bar_chart(df, x="pickup_date", y="trips")
st.dataframe(df, use_container_width=True)
