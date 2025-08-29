import streamlit as st
import math

# =============================
# 함수 정의
# =============================

# 1cm² 당 기공 밀도
stomatal_density = {
    "단풍잎": 72111.6,
    "테이블야자": 23041.5,
    "깻잎": 29387.2,
    "고무나무": 42760.7,
    "몬스테라": 12694.6,
    "스투키": 8675.1
}

# 면적 단위 변환 계수
unit_conversion_area = {
    "cm²": 1,
    "mm²": 0.01,
    "m²": 10000
}

# CO₂ 흡수량 단위 변환 계수
unit_conversion_co2 = {
    "µg": 1,
    "mg": 1e-3,
    "g": 1e-6,
    "kg": 1e-9
}

# 기공 1개당 하루 CO₂ 흡수량(µg)
co2_per_stomata_per_day = 0.05

# 성인 1명 하루 CO₂ 배출량 (kg)
co2_per_person_per_day_kg = 1.0

def calculate_stomata_airpurification_for_people(
    leaf_type, width, height, num_leaves, area_unit="cm²", co2_unit="µg", people_count=1
):
    try:
        width = float(width)
        height = float(height)
        num_leaves = int(num_leaves)
        people_count = int(people_count)
    except:
        return "숫자를 올바르게 입력해주세요."
    
    density = stomatal_density.get(leaf_type)
    if density is None:
        return "알 수 없는 잎 종류입니다."
    
    area_cm2 = width * height
    total_area_cm2 = area_cm2 * num_leaves
    total_stomata = total_area_cm2 * density
    co2_absorbed = total_stomata * co2_per_stomata_per_day  # µg/day
    
    # 스투키는 계산값 4배
    if leaf_type == "스투키":
        total_stomata *= 4
        co2_absorbed *= 4
    
    # 단위 변환
    area_converted = total_area_cm2 / unit_conversion_area.get(area_unit, 1)
    co2_absorbed_converted = co2_absorbed * unit_conversion_co2.get(co2_unit, 1)
    
    # 사람 수 기준 CO₂ 배출량 (kg → µg)
    total_people_co2_µg = people_count * co2_per_person_per_day_kg * 1e9
    
    # 필요한 잎 수 계산
    leaves_needed = math.ceil(total_people_co2_µg / co2_absorbed) if co2_absorbed > 0 else "계산 불가"
    
    result = {
        "leaf_type": leaf_type,
        "leaf_size": f"{width} x {height} cm",
        "num_leaves_input": num_leaves,
        "total_area": f"{area_converted:.2f} {area_unit}",
        "total_stomata": int(total_stomata),
        "co2_absorbed": f"{co2_absorbed_converted:,.4f} {co2_unit}/day",
        "people_count": people_count,
        "people_co2_kg_per_day": people_count * co2_per_person_per_day_kg,
        "leaves_needed_to_absorb": leaves_needed
    }
    
    return result

# =============================
# Streamlit UI
# =============================

st.title("🌿 잎의 CO₂ 흡수량 계산기 (사람 기준)")

st.markdown("입력한 잎 개수와 크기로, 선택한 사람 수의 하루 CO₂ 배출량을 흡수하려면 몇 장의 잎이 필요한지 계산합니다.")

# 사용자 입력
leaf_type = st.selectbox("잎 종류 선택", list(stomatal_density.keys()))
width = st.text_input("잎 가로 길이 (cm)", value="1")
height = st.text_input("잎 세로 길이 (cm)", value="1")
num_leaves = st.number_input("잎 개수", min_value=1, value=1, step=1)
area_unit = st.selectbox("면적 단위 선택", list(unit_conversion_area.keys()), index=0)
co2_unit = st.selectbox("CO₂ 흡수 단위 선택", list(unit_conversion_co2.keys()), index=0)
people_count = st.number_input("사람 수", min_value=1, value=1, step=1)

if st.button("계산하기"):
    result = calculate_stomata_airpurification_for_people(
        leaf_type, width, height, num_leaves, area_unit, co2_unit, people_count
    )
    
    st.subheader("계산 결과")
    for key, value in result.items():
        st.write(f"**{key}**: {value}")
