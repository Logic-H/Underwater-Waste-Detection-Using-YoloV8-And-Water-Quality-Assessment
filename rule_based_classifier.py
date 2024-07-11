import streamlit as st
import pandas as pd

# 定义一个函数，根据水质参数判断是否适宜水生生物生存
def is_habitable(pH, Iron, Nitrate, Chloride, Lead, Zinc, Turbidity, Fluoride, Copper, Sulfate, Chlorine, Manganese,
                 Total_Dissolved_Solids):
    # 设置水质参数的适宜范围
    if (pH >= 6.5 and pH <= 9.0 and Iron < 0.3 and Nitrate < 10 and Chloride < 250 and
        Lead < 0.015 and Zinc < 5 and Turbidity < 5 and Fluoride >= 0.7 and
        Fluoride <= 1.5 and Copper < 1.3 and Sulfate < 250 and Chlorine < 4.0 and
        Manganese < 0.05 and Total_Dissolved_Solids < 500):
        return 0  # 返回0表示水质适宜
    else:
        return 1  # 返回1表示水质不适宜

# 读取测试数据
test_df = pd.read_csv('C:/Users/22596/Documents/AI/Underwater-Waste-Detection-Using-YoloV8-And-Water-Quality-Assessment/test_data/test_df')

# 定义特征及其数据类型
features = {
    'pH': float,
    'Iron': float,
    'Nitrate': float,
    'Chloride': float,
    'Lead': float,
    'Zinc': float,
    'Turbidity': float,
    'Fluoride': float,
    'Copper': float,
    'Sulfate': float,
    'Chlorine': float,
    'Manganese': float,
    'Total Dissolved Solids': float,
}

# 初始化一个列表来存储水质评估结果
quality_aquatic = []

# 定义一个函数，用于创建Streamlit界面
def rbc():
    st.title('水质评估测试')
    inputs = {}
    col1, col2, col3 = st.columns(3)  # 创建三个列
    # 遍历特征，为每个特征创建输入框
    for i, feature in enumerate(features.items()):
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        with col:
            inputs[feature[0]] = st.number_input(f'{feature[0]}', value=0.0, step=0.1, format='%.1f',
                                                 key=feature[0])

    # 创建两个按钮，居中对齐
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button('预测'):
            inputs_list = list(inputs.values())
            is_good = is_habitable(*inputs_list)
            if is_good == 0:
                st.success("水质适宜水生生物生存")
            else:
                st.error("水质不适宜水生生物生存")
            quality_aquatic.append(is_good)

    with col2:
        if st.button('随机输入预测'):
            data = test_df.sample(n=1)
            data.drop(['Target', 'Color', 'Odor'], axis=1, inplace=True)
            st.write(data)
            is_good = is_habitable(*data.values.tolist()[0])
            if is_good == 0:
                st.success("水质适宜水生生物生存")
            else:
                st.error("水质不适宜水生生物生存")
            quality_aquatic.append(is_good)