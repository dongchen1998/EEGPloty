

import streamlit as st
import pandas as pd
import numpy as np
import plotly.io as pio
from io import BytesIO
import base64
import os



# 文件上传器
def load_and_read_data(uploaded_data, index_col=0, header=0):
    """
    Load and display data from an uploaded file.

    Parameters:
    uploaded_data (UploadedFile): The file uploaded by the user.
    """
    # 检查文件是否已上传
    if uploaded_data is not None:
        # 根据文件格式读取数据
        try:
            if uploaded_data.name.endswith('.csv'):
                # 假设CSV文件分隔符为逗号
                df = pd.read_csv(uploaded_data, sep=',', index_col=index_col, header=header)
            elif uploaded_data.name.endswith('.tsv'):
                # 假设TSV文件分隔符为'\t'
                df = pd.read_csv(uploaded_data, sep='\t', index_col=index_col, header=header)
            elif uploaded_data.name.endswith('.txt'):
                # 假设TXT文件分隔符为制表符'\t'
                df = pd.read_csv(uploaded_data, delimiter='\t', index_col=index_col, header=header)
            elif uploaded_data.name.endswith(('.xlsx', '.xls')):
                # 读取第一个sheet的内容
                df = pd.read_excel(uploaded_data, sheet_name=0, index_col=index_col, header=header)
            else:
                st.error('不支持的文件格式！')
                return None
            return df
        except Exception as e:
            st.error(f'读取文件时出错：{e}')

# 定义button切换按钮
def toggle_button(state_key, button_label=None):
    # 初始化 session_state 变量
    if state_key not in st.session_state:
        st.session_state[state_key] = False
    # 创建一个可以切换状态的按钮
    if st.button(button_label):  
        st.session_state[state_key] = not st.session_state[state_key]
    # 返回当前状态
    return st.session_state[state_key]

def radio_toggle(state_key, options, default_index=0):
    # 初始化 session_state 变量
    if state_key not in st.session_state:
        st.session_state[state_key] = options[default_index]
    # 创建一个 radio 选择器
    chosen_option = st.radio(state_key + '：', options, index=default_index, horizontal=True)
    # 更新 session_state
    st.session_state[state_key] = chosen_option
    # 返回当前选中的选项
    return st.session_state[state_key]

# 图表转换为不同格式的下载按钮函数
def create_download_button(fig, format, width=None, height=None, scale=None, filename=None):
    mime_type = f"image/{format}"
    if format in ["png", "jpeg", "svg", "pdf"]:
        img_bytes = pio.to_image(fig, format=format, width=width, height=height, scale=scale, engine="orca")
        st.download_button(label=f"下载{format.upper()}格式图片", data=img_bytes, file_name=f"{filename}.{format}", mime=mime_type)
    elif format == "html":
        html_bytes = pio.to_html(fig, include_plotlyjs="cdn", full_html=False, config={'responsive': False})
        st.download_button(label=f"下载{format.upper()}格式图片", data=html_bytes, file_name=f"{filename}.{format}", mime=mime_type)


def update_layout_by_theme(theme):
    theme_colors = {
        'plotly_white': {'plot_bgcolor': 'white', 'paper_bgcolor': 'white', 'font_color': 'black'},
        'plotly_dark': {'plot_bgcolor': 'black', 'paper_bgcolor': 'black', 'font_color': 'white'},
        'plotly': {'plot_bgcolor': '#e5ecf6', 'paper_bgcolor': 'white', 'font_color': 'black'},
        'simple_white': {'plot_bgcolor': 'white', 'paper_bgcolor': 'white', 'font_color': 'black'},
        'ggplot2': {'plot_bgcolor': '#ededed', 'paper_bgcolor': 'white', 'font_color': 'black'},
        'seaborn': {'plot_bgcolor': '#eaeaf2', 'paper_bgcolor': 'white', 'font_color': 'black'},
        'gridon': {'plot_bgcolor': 'white', 'paper_bgcolor': 'white', 'font_color': 'black'},
        'none': {'plot_bgcolor': 'white', 'paper_bgcolor': 'white', 'font_color': 'black'}
    }

    colors = theme_colors.get(theme, {})
    plot_bgcolor = colors.get('plot_bgcolor', None)
    paper_bgcolor = colors.get('paper_bgcolor', None)
    font_color = colors.get('font_color', 'black')
    return plot_bgcolor, paper_bgcolor, font_color

# 创建一个初始化st.session_state的函数
def init_session_state():
    st.session_state['function_name'] = []

    st.session_state['checkbox_data'] = False
    st.session_state.uploaded_data = None

    st.session_state['show_colors'] = False
    st.session_state['toggle_state'] = '离散颜色集'
    st.session_state['selected_qualitative_scheme'] = 'Plotly'
    st.session_state['selected_color'] = []

    st.session_state['group_names'] = []
    st.session_state['if_lg'] = 'no'
    st.session_state['if_yaxis'] = 'yes'
    st.session_state['if_points'] = 'False'
    st.session_state['if_no_bg'] = 'no'

    st.session_state['title'] = None
    st.session_state['x_title'] = None
    st.session_state['y_title'] = None
    st.session_state['if_legend'] = 'yes'
    st.session_state['legent_text'] = None
    st.session_state['legend_orientation'] = 'v'
    st.session_state['font_family'] = 'Arial'
    st.session_state['font_size'] = 16
    st.session_state['plotly_template'] = 'plotly_white'
    st.session_state['fig_formats'] = []
    st.session_state['width'] = None
    st.session_state['height'] = None
    st.session_state['opacity'] = 1
    st.session_state['title_font_size'] = 20
    st.session_state['legend_font_size'] = 14
    st.session_state['x_title_font_size'] = 18
    st.session_state['y_title_font_size'] = 18
