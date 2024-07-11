import sys
from imp import reload

import streamlit as st
import app
import app2
import rule_based_classifier as rbc
from inference import garbage
import seaborn as sns
import matplotlib.pyplot as plt


# 定义标签列表
labels = ['口罩', '罐头', '手机', '电子产品', '玻璃瓶', '手套', '金属', '其他', '网', '塑料袋', 'PET瓶',
          '塑料', '杆', '太阳镜', '轮胎']

# 主函数
def main():
    # 设置侧边栏标题
    st.sidebar.title('导航')
    # 选择模型
    selected_model = st.sidebar.selectbox('', ['首页', '水下目标检测模型',
                                               '水质评估模型',
                                               '水的可饮用性测试模型', '生成报告'])
    # 根据选择的模型显示相应内容
    if selected_model == '首页':
        st.title('深海慧眼')
        st.image('./assets/yacht.jpg')
        st.success('深海慧眼 项目针对水下目标，围绕水下环境复杂多变、声学图像纹理特征模糊、数据集缺少等问题，提出基于深度学习的方法，采用视觉传感器，利用水下光学图像分辨率较高、对小尺寸物体检测优势，通过YOLO-World等新型神经网络模型融合注意力机制，构建由光学图像处理模块、神经网络决策模块、传感器及其控制模块、物联网信息协同模块四大模块组成的“深海慧眼”水下目标视觉识别系统，用以改善目前人工水下目标捕捞高成本、低效率、低安全性，人工操纵的水下潜水器无法进行大规模水下目标清除，已有的水下机器人普遍呈现检测精度差的现实情况，以解决水下目标监测定位难、海洋生态评估改善难等社会热点问题')
    elif selected_model == '水下目标检测模型':
        app.app()
    elif selected_model == '水质评估模型':
        rbc.rbc()
    elif selected_model == '水的可饮用性测试模型':
        app2.app2()
    elif selected_model == '生成报告':
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # 显示所有目标标签的频率
        st.header('所有物体标签的频率')
        occurrences = [garbage.count(labels[i]) for i in range(len(labels))]
        sns.barplot(y=labels, x=occurrences)
        plt.xlabel("出现次数")
        plt.ylabel("标签")
        plt.title("出现次数的直方图")
        st.pyplot()

        # 水质对水生生物栖息地的影响
        st.header('水生生物栖息地的水质')
        quality_aquatic = rbc.quality_aquatic
        counts = [quality_aquatic.count(0), quality_aquatic.count(1)]
        if len(quality_aquatic) == 0:
            st.error("请先对水生生物栖息地的水质进行一些推理")
        else:
            ans = max(set(quality_aquatic), key=quality_aquatic.count)
            labels_h = ['适宜', '不适宜']
            habitual = labels_h[ans]
            colors = ['#cfaca4', '#623337']
            sns.set_style("whitegrid")
            plt.figure(figsize=(6, 6))
            plt.pie(counts, labels=labels_h, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('水质比例')
            st.pyplot()

        # 水的可饮用性质量
        st.header('水的可饮用性质量')
        data = app2.quality
        counts = [data.count(0), data.count(1)]
        if len(data) == 0:
            st.error("请先对水质进行一些推理")
        else:
            ans = max(set(data), key=data.count)
            labels_wqa = ['适合使用', '污染']
            qwa = labels_wqa[ans]
            colors = ['#1f77b4', '#ff7f0e']
            sns.set_style("whitegrid")
            plt.figure(figsize=(6, 6))
            plt.pie(counts, labels=labels_wqa, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('水质比例')
            st.pyplot()
            st.header("结论: ")
            st.success(
                f'在最近的图片中，最常看到的物体类型是'
                f' {labels[occurrences.index(max(occurrences))]}，出现了 {max(occurrences)} 次。'
                f' 此外，水的水质已经分析，水被标记为对水生生物{habitual}'
                f' 和对人类{qwa}。'
            )
    else:
        st.warning('请从侧边栏选择一个模型。')

# 运行主函数
main()