import pandas as pd

def calculate_and_update_ratios(filepath="data/processed/financial_summary.csv"):
    df = pd.read_csv(filepath)

    # 필요한 열이 모두 존재하는지 확인
    required_cols = ["당기순이익", "자본총계", "자산총계", "영업이익", "매출액", "부채총계"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"❌ Column '{col}' is missing in the CSV.")

    # 재무 비율 계산
    df["ROE"] = df["당기순이익"] / df["자본총계"]
    df["ROA"] = df["당기순이익"] / df["자산총계"]
    df["영업이익률"] = df["영업이익"] / df["매출액"]
    df["부채비율"] = df["부채총계"] / df["자본총계"]
    df["자기자본비율"] = df["자본총계"] / df["자산총계"]

    # 매출액 증가율은 전년도 대비 변화량 계산
    df = df.sort_values(by=["corp_name", "year"])
    df["매출액증가율"] = df.groupby("corp_name")["매출액"].pct_change()

    # 저장 (덮어쓰기)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"✅ 재무비율이 '{filepath}'에 저장되었습니다.")

if __name__ == "__main__":
    calculate_and_update_ratios()
