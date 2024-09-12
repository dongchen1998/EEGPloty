
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import os
# 导入自定义模块
from script.UniversalFunctions import load_and_read_data, create_download_button,\
                                    toggle_button, radio_toggle, update_layout_by_theme, init_session_state



# 生成默认数据集函数
def generate_default_data(workdir):
    """
    生成默认数据集
    """
    data_path = os.path.join(workdir, 'input_files', 'Pro_demo_12S_matrix.csv')
    group_path = os.path.join(workdir, 'input_files', 'Pro_demo_12S_Group.csv')
    if not os.path.exists(data_path):
        st.error('默认原始数据文件不存在，请检查！')
        return None, None

    if not os.path.exists(group_path):
        st.error('默认分组数据文件不存在，请检查！')
        return None, None

    df_data = pd.read_csv(data_path, sep=',', index_col=0, header=0)
    df_group = pd.read_csv(group_path, sep=',', index_col=0, header=0)
    return df_data, df_group

def handle_left_column():
    st.session_state.checkbox_data = st.checkbox('是否要导入自己数据？', key='checkbox_data')
    st.session_state.uploaded_data = None
    if st.session_state.checkbox_data:
        st.session_state.uploaded_data = st.file_uploader("上传你的数据文件（注意分隔符号）。", type=['csv', 'tsv', 'txt', 'xlsx', 'xls'])
    # st.session_state.checkbox_group = st.checkbox('是否要导入分组数据？')
    # st.session_state.uploaded_group = None
    # if st.session_state.checkbox_group:
    #     st.session_state.uploaded_group = st.file_uploader("上传你的分组文件（注意分隔符号）。", type=['csv', 'tsv', 'txt', 'xlsx', 'xls'])
    
# 设置特殊参数
    st.markdown('***')
    st.subheader('特殊参数：')
    # 在页面顶部创建一个占位符
    try: 
        st.session_state.error_placeholder = st.empty()
        # 颜色集开关，使用函数创建和控制开关按钮
        st.session_state.show_colors = toggle_button('show_colors', '查看 / 隐藏颜色集')
        # 根据当前状态显示或隐藏颜色集
        if st.session_state.show_colors:
            # 创建离散和连续颜色集的样本图
            fig_qualitative = px.colors.qualitative.swatches()
            fig_sequential = px.colors.sequential.swatches()
            # 调整图表大小
            fig_qualitative.update_layout(width=300, height=1000, margin=dict(l=2, r=2, t=30, b=0))  # 根据需要调整大小
            fig_sequential.update_layout(width=300, height=1000, margin=dict(l=2, r=2, t=30, b=0))   # 根据需要调整大小
            # 使用 Streamlit 的列功能并列显示两个图表
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.write("离散颜色集：")
                st.plotly_chart(fig_qualitative, use_container_width=True)
            with sub_col2:
                st.write("连续颜色集：")
                st.plotly_chart(fig_sequential, use_container_width=True)
                
        # 判断用户是选择离散颜色集还是连续颜色集
        st.session_state.toggle_state = radio_toggle("选择颜色集", ["离散颜色集", "连续颜色集", "自定义颜色集"])
        # st.write("Current State:", toggle_state)
        if st.session_state.toggle_state == '离散颜色集':
            # 获取 Plotly 的所有预设颜色集
            color_qualitative = dir(px.colors.qualitative)
            color_qualitative = [color for color in color_qualitative if not color.startswith("__") and color not in ['_swatches', 'swatches']]
            # 让用户选择一个颜色集
            st.session_state.selected_qualitative_scheme = st.selectbox('选择一个具体离散颜色集：', color_qualitative)
            selected_colors = getattr(px.colors.qualitative, st.session_state.selected_qualitative_scheme)
            # 创建一个下拉菜单让用户选择特定的颜色
            st.session_state.selected_color = st.multiselect('选择具体的颜色 (有几组数据就选择几组)：', selected_colors)  # 返回一个颜色列表
            # st.markdown(selected_color)
            # 展示用户选择的颜色
            st.write('您选择的颜色是:')
            # 使用一个容器来并排展示颜色
            color_container = ""
            for color in st.session_state.selected_color:
                color_container += f"<span style='display:inline-block; margin: 2px; width: 30px; height: 30px; background-color: {color};'></span>"
            st.markdown(color_container, unsafe_allow_html=True)
        elif st.session_state.toggle_state == '连续颜色集':
            color_sequential = dir(px.colors.sequential)
            color_sequential = [color for color in color_sequential if not color.startswith("__") and color not in ['_swatches', 'swatches', '_swatches_continuous', 'swatches_continuous']]
            st.session_state.selected_color = st.selectbox('选择一个具体连续颜色集：', color_sequential)  # 返回一个颜色代号
            # st.markdown(selected_color)
        elif st.session_state.toggle_state == '自定义颜色集':
            # 颜色盘参考
            color_reference = st.color_picker('颜色盘参考（可以复制颜色盘中的代号）：', '#FA7F6F')
            # 返回一个颜色列表
            st.session_state.selected_color = st.text_input('有几组就输入几组颜色（用英文逗号隔开）：', '#FA7F6F, #82B0D2, #8ECFC9, #FFBE7A, #BEB8DC, #E7DAD2, #A1A9D0, #B883D4, #9E9E9E, #CFEAF1')
            # 将字符串分割成列表，并去除每个元素两端的空格
            if st.session_state.selected_color.strip():
                st.session_state.selected_color = [color.strip() for color in st.session_state.selected_color.split(',')]
            else:
                st.session_state.selected_color = []
            # st.markdown(selected_color)

        st.session_state.group_names = st.text_input('输入组名（用英文逗号隔开，不输入则为列名）：')
        # 检查group_names是否为空
        if st.session_state.group_names.strip():
            # 如果不为空，则分割字符串并去除每个元素的空白
            st.session_state.group_names = [group.strip() for group in st.session_state.group_names.split(',')]
        else:
            # 如果为空，则返回一个空列表
            st.session_state.group_names = []
            
        # yaxis_tickvals = st.text_input('输入y轴刻度值（用英文逗号隔开，与y轴范围同用）：')
        # yaxis_range = st.text_input('输入y轴范围（用英文逗号隔开，与y轴刻度值同用）：')
        st.session_state.if_lg = st.radio('是否取对数？', ('yes', 'no'), horizontal=True, index=1)
        st.session_state.if_yaxis = st.radio('Y 轴图', ('yes', 'no'), horizontal=True, index=0)
        st.session_state.if_points = st.radio('是否显示数据点？', ('all', 'outliers', 'suspectedoutliers', 'False'), horizontal=True, index=3)
        st.session_state.if_no_bg = st.radio('是否显示背景（下载为透明背景）？', ('yes', 'no'), horizontal=True, index=1)

    # 通用参数设置
        st.markdown('***')
        st.subheader('通用参数：')
        # 以下是根据图片中的界面创建的参数设置
        # 图片标题
        st.session_state.title = st.text_input('图片标题（不显示则为空）):',)
        # X轴标题
        st.session_state.x_title = st.text_input('X 轴标题（不显示则为空）:',)
        # Y轴标题
        st.session_state.y_title = st.text_input('Y 轴标题（不显示则为空）:',)
        st.session_state.if_legend = st.radio('是否显示图例？', ('yes', 'no'), horizontal=True, index=0)
        st.session_state.legent_text = st.text_input('图例标题（不显示则为空）:')
        st.session_state.legend_orientation = st.selectbox('图例方向:', ['v', 'h'])
        st.session_state.font_family = st.selectbox('字体:', ['Arial', 'Calibri', 'Times New Roman'])
        st.session_state.font_size = st.slider('全局字体大小:', min_value=0, max_value=100, value=16)
        # st.markdown(type(font_size))
        st.session_state.plotly_template = st.selectbox('主题风格:', ['plotly_white', 'plotly_dark', 'plotly', 'simple_white', 'ggplot2', 'seaborn', 'gridon', 'none'])
        st.markdown(st.session_state.plotly_template)
        st.session_state.fig_formats = st.multiselect('图片输出格式:', ['jpeg', 'png', 'svg', 'pdf', 'html'])

        # 宽度设置，使用滑块选择
        st.session_state.width = float(st.slider('图片宽度:', min_value=0.0, max_value=30.0, value=0.0, step=0.1))
        # 高度设置，使用滑块选择
        st.session_state.height = float(st.slider('图片高度:', min_value=0.0, max_value=30.0, value=0.0, step=0.1))
        # 透明度
        st.session_state.opacity = float(st.slider('透明度:', min_value=0.0, max_value=1.0, value=1.0, step=0.1))
        st.session_state.title_font_size = st.slider('标题字体大小:', min_value=0, max_value=100, value=20)
        st.session_state.legend_font_size = st.slider('图例字体大小:', min_value=0, max_value=100, value=14)
        st.session_state.x_title_font_size = st.slider('X轴标题字体大小:', min_value=0, max_value=100, value=18)
        st.session_state.y_title_font_size = st.slider('Y轴标题字体大小:', min_value=0, max_value=100, value=18)
        # x_title_font_angle = st.slider('X轴字体角度:', min_value=0, max_value=360, value=0)
    except Exception as e:
        st.session_state.error_placeholder.error(f'参数设置时出错：{e}')



def handle_right_column(df_data=None, df_group=None, workdir=None):
    try:
        # 在页面顶部创建一个占位符
        st.session_state.error_placeholder = st.empty()
        if st.session_state.checkbox_data and st.session_state.uploaded_data is not None:
            # 询问用户首行和首列是否为名称
            user_first_column = st.checkbox('首行为列名？', value=True)
            user_first_index = st.checkbox('首列为索引？', value=True)
        # 根据用户的选择调整数据读取方式
            if user_first_column and user_first_index:
                # 首行为列名，首列为索引
                df_data = load_and_read_data(st.session_state.uploaded_data, index_col=0, header=0)
            elif user_first_column:
                # 仅首行为列名
                df_data = load_and_read_data(st.session_state.uploaded_data, index_col=None, header=0)
            elif user_first_index:
                # 仅首列为索引
                df_data = load_and_read_data(st.session_state.uploaded_data, index_col=0, header=None)
            else:
                # 首行首列均不作为名称
                df_data = load_and_read_data(st.session_state.uploaded_data, index_col=None, header=None)
            # 如果DataFrame不是None，显示数据表
            if df_data is not None:
                st.subheader('数据预览：')
                st.dataframe(df_data)  # 使用st.dataframe显示数据
        else:
            st.subheader('原始数据')
            st.dataframe(df_data)  # 使用 st.dataframe 显示数据

    # 绘图
        st.markdown('***')
        # 初始化绘图按钮状态
        if 'show_plot' not in st.session_state:
            st.session_state['show_plot'] = False
        if st.button('运行结果'):
            st.session_state['show_plot'] = True
        else:
            st.session_state['show_plot'] = False
        if st.session_state.get('show_plot', False):
            # init_session_state()
        # st.subheader('Result：')
            box_plot = Box_Plot(df_data,
                                df_group=df_group,
                                group_names=st.session_state.group_names,
                                if_selected_color=st.session_state.toggle_state,   
                                group_color=st.session_state.selected_color,
                                if_lg=st.session_state.if_lg,
                                if_yaxis=st.session_state.if_yaxis,
                                if_points=st.session_state.if_points,
                                if_no_bg=st.session_state.if_no_bg,

                                title=st.session_state.title,
                                x_title=st.session_state.x_title,
                                y_title=st.session_state.y_title,
                                if_legend=st.session_state.if_legend,
                                legent_text=st.session_state.legent_text,
                                legend_orientation=st.session_state.legend_orientation,
                                font_family=st.session_state.font_family,
                                font_size=st.session_state.font_size,
                                plotly_template=st.session_state.plotly_template,
                                fig_formats=st.session_state.fig_formats,
                                workdir=workdir,
                                
                                width=st.session_state.width,
                                height=st.session_state.height,
                                opacity=st.session_state.opacity,
                                title_font_size=st.session_state.title_font_size,
                                legend_font_size=st.session_state.legend_font_size,
                                x_title_font_size=st.session_state.x_title_font_size,
                                y_title_font_size=st.session_state.y_title_font_size,
                                )
            st.plotly_chart(box_plot, use_container_width=False, theme=None)
    except Exception as e:
        st.session_state.error_placeholder.error(f'绘图时出错：{e}')

def Box_Plot(df_data, df_group=None, if_selected_color='离散颜色集', group_names=None, 
             group_color=None, if_lg='no', if_yaxis='yes', if_points='no', if_no_bg='no',
             title=None, x_title=None, y_title=None, if_legend='yes', legent_text=None,
             legend_orientation=None, font_family='Arial', font_size=16, 
             plotly_template='plotly_white', fig_formats=None, workdir=None,
             width=None, height=None, opacity=1, title_font_size=20,
             legend_font_size=14, x_title_font_size=18, y_title_font_size=18):
    
    # 参数验证
    if not isinstance(df_data, pd.DataFrame):
        raise ValueError("df_data 应该是一个 pandas DataFrame")
    
    # 初始化变量
    y_columns = df_data.columns.tolist()
    group_names = group_names or y_columns

    # 处理宽度和高度参数
    width = width * 100 if width else None
    height = height * 100 if height else None

    # 设置颜色方案
    if if_selected_color == '离散颜色集':
        colors = group_color or px.colors.qualitative.Plotly
    elif if_selected_color == '连续颜色集':
        colors = getattr(px.colors.sequential, group_color)
    elif if_selected_color == '自定义颜色集':
        if not group_color:
            st.error("自定义颜色集为空，请准备颜色代号！")
            return
        colors = group_color

    pointpos = None
    if if_points =='False':
        if_points = False
    elif if_points == 'all':
        if_points = if_points
        pointpos = -1.8
    # st.markdown(if_points)  
    if_legend = True if if_legend == 'yes' else False
         
    # 设置主题
    plot_bgcolor, paper_bgcolor, font_color = update_layout_by_theme(plotly_template)
    plotly_template = None if plotly_template == 'none' else plotly_template

    # 构建图形
    fig = go.Figure()
    for i, column in enumerate(y_columns):
        y = np.log10(df_data[column]) if if_lg == 'yes' else df_data[column]
        axis = 'y' if if_yaxis == 'yes' else 'x'

        fig.add_trace(go.Box(  # 修改为 Box
                    x=y if axis == 'x' else None,
                    y=y if axis == 'y' else None,
                    name=group_names[i],
                    marker_color=colors[i % len(colors)],  # 修改颜色设置
                    opacity=opacity,
                    boxpoints=if_points,  # 显示所有数据点
                    # jitter=0.3,  # 调整数据点的显示方式
                    pointpos=pointpos,  # 数据点的位置
                    boxmean=True,  # 显示均值和标准差
                    showlegend=if_legend,
        ))

    # 更新布局
    fig.update_layout(
        title=dict(text=title, font=dict(size=title_font_size)),
        xaxis=dict(title=x_title, titlefont=dict(size=x_title_font_size)),
        yaxis=dict(title=y_title, titlefont=dict(size=y_title_font_size)),
        legend=dict(title=legent_text, orientation=legend_orientation, font=dict(size=legend_font_size)),
        width=width, height=height, template=plotly_template,
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor,
        font=dict(family=font_family, size=font_size, color=font_color)
    )

    if if_no_bg == 'yes':
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # # 导出图表
    # if fig_formats: 
    #     for fmt in fig_formats:
    #         plot_path = os.path.join(workdir, 'output_files', f"Violin_Plot.{fmt}")
    #         fig.write_html(plot_path) if fmt == 'html' else fig.write_image(plot_path, width=width, height=height, scale=2, engine='orca')
    # 创建图表下载按钮
    sub_col1, sub_col2 = st.columns(2)
    for i, file_format in enumerate(fig_formats):
        with sub_col1 if i % 2 == 0 else sub_col2:
            filename = f"Violin_Plot"
            create_download_button(fig, file_format, width=width, height=height, scale=2, filename=filename)

    return fig


# 参数设置
def layout_interface(workdir=None, function_name=None):
    # 初始化默认数据
    df_data, df_group = generate_default_data(workdir)
    if df_data is None or df_group is None:
        return  # 数据文件不存在时，不继续执行
    # 初始化st.session_state
    # st.markdown(st.session_state.toggle_state)
    # init_session_state()
    # st.markdown(st.session_state.toggle_state)
    # st.session_state.clear()
    # st.markdown(st.session_state.toggle_state)
    # 创建两列布局
    left_column, right_column = st.columns([1, 2])
    with left_column:
        handle_left_column()
    with right_column:
        handle_right_column(df_data, df_group, workdir)