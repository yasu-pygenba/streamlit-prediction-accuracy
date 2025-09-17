import streamlit as st
import pandas as pd
import altair as alt

def keiba_dashboard():
    # CSV読み込み
    df = pd.read_csv('sample.csv')

    st.title("🏇 競馬データ ダッシュボード")

    # サイドバーでフィルタ
    venue = st.sidebar.selectbox("開催場を選択", df["開催場"].unique())
    bet_type = st.sidebar.multiselect(
        "券種を選択", df["券種"].unique(), default=list(df["券種"].unique())
    )
    trackman = st.sidebar.multiselect(
        "トラックマンを選択", df["トラックマン"].unique(), default=list(df["トラックマン"].unique())
    )

    # フィルタリング
    df_filtered = df[
        (df["開催場"] == venue) &
        (df["券種"].isin(bet_type)) &
        (df["トラックマン"].isin(trackman))
    ]

    # データ表示
    st.write(f"### {venue} のデータ（{', '.join(bet_type)}）")
    st.dataframe(df_filtered)

    # 集計用データ
    chart_data = (
        df_filtered.groupby(["トラックマン", "券種"])["回収率(%)"]
        .mean()
        .reset_index()
    )

    # Altair グループ棒グラフ
    bar = (
        alt.Chart(chart_data)
        .mark_bar(size=15, cornerRadius=3)
        .encode(
            x=alt.X(
                "トラックマン:N",
                title="トラックマン",
                axis=alt.Axis(
                    labelAngle=0,
                    labelAlign="center", 
                    labelBaseline="top",
                    labelPadding=8
                )
            ),
            xOffset="券種:N",
            y=alt.Y("回収率(%):Q"),
            color=alt.Color("券種:N", scale=alt.Scale(scheme="set2")),
            tooltip=["トラックマン", "券種", "回収率(%)"]
        )
    )


    # 棒の上にラベル追加
    text = bar.mark_text(
        align="center",
        baseline="bottom",
        dy=-2,
        fontSize=11
    ).encode(text="回収率(%):Q")

    chart = (bar + text).properties(
        width=800,
        height=450
    ).configure_axisX(
        titleFontSize=14,
        titlePadding=30,
        labelFontSize=12
    ).configure_view(
        strokeWidth=0
    )



    st.write("トラックマン別 回収率(%)")
    st.altair_chart(chart, use_container_width=True) 

def main():
    keiba_dashboard()

if __name__ == "__main__":
    main()
