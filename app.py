import cv2
import streamlit as st
import numpy as np
import dark_channel_prior as dcp
import inference as inf

# 用于从图像中去除噪声的函数
def remove_noise(image):
    # 使用您自己的去噪代码替换此处
    processed_image, alpha_map = dcp.haze_removal(image, w_size=15, a_omega=0.95, gf_w_size=200, eps=1e-6)
    return processed_image

# 在图像上执行对象检测的函数
def detect_objects(image):
    # 使用您自己的对象检测代码替换此处
    # 确保输出图像周围有检测到的对象的边界框
    output_image, class_names = inf.detect(image)
    return output_image, class_names

# Streamlit 应用程序的主函数
def app():
    st.title("水下目标检测模型")
    st.text("上传一张图片以检测对象")

    # 允许用户上传图片或视频
    file = st.file_uploader("选择文件", type=["jpg", "jpeg", "png"])
    # 处理输入并显示输出
    if file is not None:
        st.text("正在上传图片...")
        input_image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        input_image = cv2.resize(input_image, (416, 416))
        st.text("输入图片:")
        st.image(input_image)

        # 处理输入
        st.text("正在从输入中去除噪声...")
        processed_image = remove_noise(input_image)
        st.image(processed_image, clamp=True)

        # 运行模型
        st.text("正在运行模型...")
        output_image, class_names = detect_objects(processed_image)

        # 显示输出
        st.text("输出图片:")
        # 显示 "输出图片"
        st.image(output_image)
        if len(class_names) == 0:
            st.success("水很清澈！！！")
        else:
            st.error(f"检测到杂物！！！\n图片中有 {class_names}")