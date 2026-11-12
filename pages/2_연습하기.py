from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="펭귄 탐구 대시보드", page_icon="🐧", layout="wide")


# 원본은 보존하고, 선택한 자료만 별도로 분석합니다.
@st.cache_data
def load_penguins():
    return pd.read_csv(Path(__file__).resolve().parents[1] / "penguins.csv")


pg = load_penguins()
labels = {
    "bill_length_mm": "부리 길이 (mm)",
    "bill_depth_mm": "부리 깊이 (mm)",
    "flipper_length_mm": "날개 길이 (mm)",
    "body_mass_g": "체중 (g)",
}
english = {
    "bill_length_mm": "Bill length (mm)",
    "bill_depth_mm": "Bill depth (mm)",
    "flipper_length_mm": "Flipper length (mm)",
    "body_mass_g": "Body mass (g)",
}
palette = {"Adelie": "#3288bd", "Chinstrap": "#e88a40", "Gentoo": "#36a393"}
sex_labels = {"MALE": "수컷", "FEMALE": "암컷", "미기록": "미기록"}

st.title("🐧 펭귄 탐구 대시보드")
st.caption("Palmer Penguins · 종과 서식지에 따라 펭귄의 몸 크기는 어떻게 다를까요?")

with st.sidebar:
    st.header("분석할 펭귄 선택")
    species = st.multiselect("종", list(palette), default=list(palette))
    islands = st.multiselect("섬", sorted(pg["island"].unique()), default=sorted(pg["island"].unique()))
    sexes = st.multiselect("성별", list(sex_labels), default=list(sex_labels), format_func=sex_labels.get)
    st.caption("선택을 모두 해제하면 해당 조건의 자료가 0개가 됩니다.")
    st.divider()
    st.markdown("**단위 안내**\n\n길이: mm · 체중: g")
    st.caption("성별이 없는 자료는 ‘미기록’으로 선택할 수 있습니다.")

selected = pg.loc[
    pg["species"].isin(species)
    & pg["island"].isin(islands)
    & pg["sex"].fillna("미기록").isin(sexes)
].copy()
st.caption(f"전체 {len(pg):,}마리 중 {len(selected):,}마리 선택")
if selected.empty:
    st.info("조건에 맞는 펭귄이 없습니다. 왼쪽에서 종·섬·성별을 다시 선택해 주세요.")
    st.stop()


def mean_text(column, unit):
    value = selected[column].mean()
    return "자료 없음" if pd.isna(value) else f"{value:,.1f} {unit}"


cards = st.columns(4)
cards[0].metric("선택한 펭귄", f"{len(selected):,}마리")
cards[1].metric("펭귄 종", f"{selected['species'].nunique()}종")
cards[2].metric("평균 체중", mean_text("body_mass_g", "g"))
cards[3].metric("평균 날개 길이", mean_text("flipper_length_mm", "mm"))
st.caption("평균은 해당 측정값이 있는 개체로 계산합니다. 원본의 누락값을 채우거나 삭제하지 않습니다.")

overview, relation, distribution, data_tab = st.tabs(["종별 비교", "변수의 관계", "분포 살펴보기", "자료와 요약"])

with overview:
    st.subheader("어떤 종이 얼마나 있을까요?")
    counts = selected["species"].value_counts().reindex(list(palette), fill_value=0)
    st.bar_chart(counts.rename("개체 수"), color="#3288bd")
    st.subheader("종별 몸 크기 비교")
    summary = selected.groupby("species")[list(labels)].mean().rename(columns=labels)
    st.dataframe(summary.round(1), width="stretch")
    st.caption("표의 값은 종별 평균입니다. 평균과 종별 개체 수를 함께 비교하세요.")
    st.info("탐구 질문: 섬을 하나씩 골랐을 때 나타나는 종의 구성이 어떻게 달라지나요?")

with relation:
    st.subheader("두 측정값 사이의 관계")
    controls = st.columns(2)
    x = controls[0].selectbox("가로축", list(labels), index=2, format_func=labels.get)
    y_options = [key for key in labels if key != x]
    y = controls[1].selectbox("세로축", y_options,
                              index=y_options.index("body_mass_g") if "body_mass_g" in y_options else 0,
                              format_func=labels.get)
    plot_data = selected.dropna(subset=[x, y])
    if plot_data.empty:
        st.info("선택한 두 변수의 측정값이 모두 있는 개체가 없습니다.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4.8))
        sns.scatterplot(data=plot_data, x=x, y=y, hue="species", palette=palette,
                        s=65, alpha=0.8, ax=ax)
        ax.set(xlabel=english[x], ylabel=english[y])
        ax.legend(title="Species")
        sns.despine(ax=ax)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"산점도: {len(plot_data)}마리 사용 · 두 측정값 중 누락이 있는 {len(selected) - len(plot_data)}마리 제외")
        if len(plot_data) >= 3 and plot_data[x].nunique() > 1 and plot_data[y].nunique() > 1:
            st.metric("선택 자료 전체의 피어슨 상관계수", f"{plot_data[x].corr(plot_data[y]):.3f}")
        st.caption("상관관계는 인과관계를 뜻하지 않습니다. 종을 섞었을 때와 한 종만 선택했을 때의 관계를 비교해 보세요.")

with distribution:
    st.subheader("측정값은 어떻게 퍼져 있을까요?")
    variable = st.selectbox("비교할 측정값", list(labels), index=3, format_func=labels.get)
    chart_type = st.radio("그래프 종류", ["히스토그램", "상자그림"], horizontal=True)
    plot_data = selected.dropna(subset=[variable])
    if plot_data.empty:
        st.info("이 측정값에 사용할 수 있는 자료가 없습니다.")
    else:
        fig, ax = plt.subplots(figsize=(8, 4.8))
        if chart_type == "히스토그램":
            bins = st.slider("구간 수", 5, 30, 15)
            sns.histplot(data=plot_data, x=variable, hue="species", bins=bins,
                         palette=palette, element="step", alpha=0.35, ax=ax)
            ax.set(xlabel=english[variable], ylabel="Count")
        else:
            sns.boxplot(data=plot_data, x="species", y=variable, color="#b8dce9", ax=ax)
            sns.stripplot(data=plot_data, x="species", y=variable, color="#24516a",
                          alpha=0.4, size=3, jitter=0.15, ax=ax)
            ax.set(xlabel="Species", ylabel=english[variable])
        sns.despine(ax=ax)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption(f"{len(plot_data)}마리 사용 · 측정값이 없는 {len(selected) - len(plot_data)}마리 제외")
        st.info("탐구 질문: 평균이 비슷한 종도 분포의 퍼짐이나 극단적인 값은 다를까요?")

with data_tab:
    st.subheader("선택한 자료")
    display_data = selected.rename(columns={"species": "종", "island": "섬", "sex": "성별", **labels})
    st.dataframe(display_data, width="stretch")
    st.download_button("선택 자료 CSV 내려받기", selected.to_csv(index=False).encode("utf-8-sig"),
                       file_name="selected_penguins.csv", mime="text/csv")
    st.subheader("기초 통계량")
    st.dataframe(selected[list(labels)].describe().rename(columns=labels).round(2), width="stretch")
    st.caption("count: 측정 개수 · mean: 평균 · std: 표본 표준편차 · 50%: 중앙값")
    with st.expander("누락값 확인"):
        st.dataframe(selected.isna().sum().rename("누락 개수").to_frame(), width="stretch")

st.divider()
st.caption("출처: Palmer Penguins / Seaborn 예제 데이터. 관측된 펭귄의 특성을 탐색하는 자료입니다.")
st.markdown("[데이터 설명](https://allisonhorst.github.io/palmerpenguins/) · [Seaborn 원본 자료](https://github.com/mwaskom/seaborn-data/blob/master/penguins.csv)")
