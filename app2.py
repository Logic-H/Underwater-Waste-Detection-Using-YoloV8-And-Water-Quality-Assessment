import streamlit as st
from pycaret.classification import *
import pandas as pd
# 读取测试数据
test_df = pd.read_csv('C:/Users/22596/Documents/AI/Underwater-Waste-Detection-Using-YoloV8-And-Water-Quality-Assessment/test_data/test_df')

# 定义特征及其类型
features = {
    'pH': float,
    'Iron': float,
    'Nitrate': float,
    'Chloride': float,
    'Lead': float,
    'Zinc': float,
    'Color': str,
    'Turbidity': float,
    'Fluoride': float,
    'Copper': float,
    'Odor': float,
    'Sulfate': float,
    'Chlorine': float,
    'Manganese': float,
    'Total Dissolved Solids': float,
}

# 定义目标变量
target_variable = 'Target'

# 定义颜色选项
color_options = ['无色', '淡黄色', '浅黄色', '近无色', '黄色', 'NaN']

quality = []
# 创建 Streamlit 应用程序
def app2():
    st.title('水的可饮用性测试模型')
    # 加载预训练模型
    model = load_model(
        'C:/Users/22596/Documents/AI/Underwater-Waste-Detection-Using-YoloV8-And-Water-Quality-Assessment/models/Water_Potability'
        '/xgboost_without_source_month')
    # 为每个特征创建输入控件
    inputs = {}
    col1, col2, col3 = st.columns(3)
    for i, feature in enumerate(features.items()):
        if feature[0] == 'Color':
            col = col1
        elif i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        with col:
            if feature[0] == 'Color':
                inputs[feature[0]] = st.selectbox(f'{feature[0]}', options=color_options)
            else:
                inputs[feature[0]] = st.number_input(f'{feature[0]}', value=0.0, step=0.1, format='%.1f',
                                                     key=feature[0])

    # 添加两个居中的按钮
    col1, col2 = st.columns([1,2])
    with col1:
        if st.button('预测'):
            data = pd.DataFrame(inputs, index=range(0, 1), columns=inputs.keys())
            target = predict_model(model, data=data)
            quality.append(target['prediction_label'][0])
            if target['prediction_label'][0] == 0:
                st.success('水适合饮用，也适合灌溉')
            else:
                st.error('水不适合饮用或灌溉')

    with col2:
        if st.button('随机输入预测'):
            data = test_df.sample(n=1)
            data.drop(['Target'], axis=1, inplace=True)
            st.write(data)
            target = predict_model(model, data=data)
            quality.append(target['prediction_label'][data.index[0]])
            if target['prediction_label'][data.index[0]] == 0:
                st.success('水适合饮用，也适合灌溉')
            else:
                st.error('水不适合饮用或灌溉')