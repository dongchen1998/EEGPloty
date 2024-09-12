
import streamlit as st
# from st_aggrid import AgGrid
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import os
# 导入自定义模块
from script.UniversalFunctions import load_and_read_data, create_download_button,\
                                    toggle_button, radio_toggle, update_layout_by_theme


# 生成默认数据集函数
def generate_default_data(workdir):
    """
    生成默认数据集
    """
    data_path = os.path.join(workdir, 'input_files', 'Pro_demo_3G_matrix_Scatter.csv')
    group_path = os.path.join(workdir, 'input_files', 'Pro_demo_3G_Group_Scatter.csv')

    if not os.path.exists(data_path):
        st.error('默认原始数据文件不存在，请检查！')
        return None, None

    if not os.path.exists(group_path):
        st.error('默认分组数据文件不存在，请检查！')
        return None, None

    df_data = pd.read_csv(data_path, sep=',', index_col=0, header=0)
    df_group = pd.read_csv(group_path, sep=',', index_col=0, header=0)
    return df_data, df_group


# 参数设置
def layout_interface(workdir=None):
    """
    创建一个用户界面用于Streamlit应用，允许用户上传数据文件和分组文件，并设置图像相关的参数。

    用户可以选择是否上传自己的数据，如果选择上传，可以通过文件上传器上传csv, tsv, txt, xlsx或xls文件。
    类似地，用户可以选择是否上传分组数据，并使用文件上传器上传相应的文件。

    除了文件上传，用户还可以通过左侧的控制面板设置图像的标题，X轴和Y轴的标题，输出格式，尺寸，
    主题，字体和其他可视化参数。

    该函数将所有用户的输入和配置作为一个字典返回，可以在其他程序中使用这些配置来进一步处理数据和图像。
    """
    # 初始化默认数据
    df_data, df_group = generate_default_data(workdir)
    if df_data is None or df_group is None:
        return  # 数据文件不存在时，不继续执行
    
    # 创建两列布局
    left_column, right_column = st.columns([1, 2])
    # try:
    # 在左边的列中放置复选框和文件上传器：导入数据集
    with left_column:
        checkbox_data = st.checkbox('是否要导入自己数据？')
        uploaded_data = None
        if checkbox_data:
            uploaded_data = st.file_uploader("上传你的数据文件（注意分隔符号）。", type=['csv', 'tsv', 'txt', 'xlsx', 'xls'])
        # checkbox_group = st.checkbox('是否要导入分组数据？')
        # uploaded_group = None
        # if checkbox_group:
        #     uploaded_group = st.file_uploader("上传你的分组文件（注意分隔符号）。", type=['csv', 'tsv', 'txt', 'xlsx', 'xls'])
        
    # 设置特殊参数
        st.markdown('***')
        st.subheader('特殊参数：')
        # 颜色集开关，使用函数创建和控制开关按钮
        show_colors = toggle_button('show_colors', '查看 / 隐藏颜色集')
        # 根据当前状态显示或隐藏颜色集
        if show_colors:
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
        toggle_state = radio_toggle("选择颜色集", ["离散颜色集", "连续颜色集", "自定义颜色集"])
        # st.write("Current State:", toggle_state)
        if toggle_state == '离散颜色集':
            # 获取 Plotly 的所有预设颜色集
            color_qualitative = dir(px.colors.qualitative)
            color_qualitative = [color for color in color_qualitative if not color.startswith("__") and color not in ['_swatches', 'swatches']]
            # 让用户选择一个颜色集
            selected_qualitative_scheme = st.selectbox('选择一个具体离散颜色集：', color_qualitative)
            selected_colors = getattr(px.colors.qualitative, selected_qualitative_scheme)
            # 创建一个下拉菜单让用户选择特定的颜色
            selected_color = st.multiselect('选择具体的颜色 (有几组数据就选择几组)：', selected_colors)  # 返回一个颜色列表
            # st.markdown(selected_color)
            # 展示用户选择的颜色
            st.write('您选择的颜色是:')
            # 使用一个容器来并排展示颜色
            color_container = ""
            for color in selected_color:
                color_container += f"<span style='display:inline-block; margin: 2px; width: 30px; height: 30px; background-color: {color};'></span>"
            st.markdown(color_container, unsafe_allow_html=True)
        elif toggle_state == '连续颜色集':
            color_sequential = dir(px.colors.sequential)
            color_sequential = [color for color in color_sequential if not color.startswith("__") and color not in ['_swatches', 'swatches', '_swatches_continuous', 'swatches_continuous']]
            selected_color = st.selectbox('选择一个具体连续颜色集：', color_sequential)  # 返回一个颜色代号
            # st.markdown(selected_color)
        elif toggle_state == '自定义颜色集':
            # 颜色盘参考
            color_reference = st.color_picker('颜色盘参考（可以复制颜色盘中的代号）：', '#FA7F6F')
            # 返回一个颜色列表
            selected_color = st.text_input('有几组就输入几组颜色（用英文逗号隔开）：', '#FA7F6F, #82B0D2, #8ECFC9, #FFBE7A, #BEB8DC, #E7DAD2, #A1A9D0, #B883D4, #9E9E9E, #CFEAF1')
            # 将字符串分割成列表，并去除每个元素两端的空格
            if selected_color.strip():
                selected_color = [color.strip() for color in selected_color.split(',')]
            else:
                selected_color = []
            # st.markdown(selected_color)

        group_names = st.text_input('输入组名（用英文逗号隔开，不输入则为列名）：')
        # 检查group_names是否为空
        if group_names.strip():
            # 如果不为空，则分割字符串并去除每个元素的空白
            group_names = [group.strip() for group in group_names.split(',')]
        else:
            # 如果为空，则返回一个空列表
            group_names = []
        # 指定显示文本
        selected_text = st.text_input('输入指定显示文本（用英文逗号隔开，不输入则为索引名）：')
        # 检查selected_text是否为空
        if selected_text.strip():
            # 如果不为空，则分割字符串并去除每个元素的空白
            selected_text = [text.strip().upper() for text in selected_text.split(',')]
        else:
            # 如果为空，则返回一个空列表
            selected_text = []        
        symbol_list = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 
                        'triangle-left', 'triangle-right', 'triangle-ne', 'triangle-se', 'triangle-sw', 
                        'triangle-nw', 'pentagon', 'hexagon', 'hexagon2', 'octagon', 'star', 'hexagram', 
                        'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide']
        marker_size = st.slider('点大小：', min_value=0, max_value=20, value=6) 
        symbol = st.multiselect('选择点的形状（有几组就选几组）：', symbol_list)
        sub_col1, sub_col2= st.columns(2) 
        with sub_col1:
            if_lg = st.radio('是否取对数？', ('yes', 'no'), horizontal=True, index=1)
            if_line = st.radio('是否显示连线？', ('yes', 'no'), horizontal=True, index=1)
        with sub_col2:
            if_text = st.radio('是否显示文本', ('yes', 'no'), horizontal=True, index=1)
            if_no_bg = st.radio('是否显示背景（下载为透明背景）？', ('yes', 'no'), horizontal=True, index=1)

    # 通用参数设置
        st.markdown('***')
        st.subheader('通用参数：')
        # 以下是根据图片中的界面创建的参数设置
        sub_col1, sub_col2= st.columns(2)    
        with sub_col1:
            # 图片标题
            title = st.text_input('图片标题（不显示则为空）):', )
                        # X轴标题
            x_title = st.text_input('X 轴标题（不显示则为空）:',)
                        # Y轴标题
            y_title = st.text_input('Y 轴标题（不显示则为空）:', )
            if_legend = st.radio('是否显示图例？', ('yes', 'no'), horizontal=True, index=0)
            legent_text = st.text_input('图例标题（不显示则为空）:', 'Conditions')
            legend_orientation = st.selectbox('图例方向:', ['v', 'h'])
            title_font_size = st.slider('标题字体大小:', min_value=0, max_value=100, value=20)
            x_title_font_size = st.slider('X轴标题字体大小:', min_value=0, max_value=100, value=18)
            y_title_font_size = st.slider('Y轴标题字体大小:', min_value=0, max_value=100, value=18)
        with sub_col2:
            plotly_template = st.selectbox('主题风格:', ['plotly_white', 'plotly_dark', 'plotly', 'simple_white', 'ggplot2', 'seaborn', 'gridon', 'none'])
            font_family = st.selectbox('字体:', ['Arial', 'Calibri', 'Times New Roman'])
            fig_formats = st.multiselect('图片输出格式:', ['jpeg', 'png', 'svg', 'pdf', 'html'])
            # 宽度设置，使用滑块选择
            width = float(st.slider('图片宽度:', min_value=0.0, max_value=30.0, value=0.0, step=0.1))
            # 高度设置，使用滑块选择
            height = float(st.slider('图片高度:', min_value=0.0, max_value=30.0, value=0.0, step=0.1))
            # 透明度
            opacity = float(st.slider('透明度:', min_value=0.0, max_value=1.0, value=0.8, step=0.1))
            font_size = st.slider('全局字体大小:', min_value=0, max_value=100, value=16)
            legend_font_size = st.slider('图例字体大小:', min_value=0, max_value=100, value=14)


# 在右边的列中放置表格视图
    with right_column:
        # 在页面顶部创建一个占位符
        error_placeholder = st.empty()
        if checkbox_data and uploaded_data is not None:
            # df_data = load_and_read_data(uploaded_data)
            # 询问用户首行和首列是否为名称
            user_first_column = st.checkbox('首行为列名？', value=True)
            user_first_index = st.checkbox('首列为索引？', value=True)
            # 根据用户的选择调整数据读取方式
            if user_first_column and user_first_index:
                # 首行为列名，首列为索引
                df_data = load_and_read_data(uploaded_data, index_col=0, header=0)
            elif user_first_column:
                # 仅首行为列名
                df_data = load_and_read_data(uploaded_data, index_col=None, header=0)
            elif user_first_index:
                # 仅首列为索引
                df_data = load_and_read_data(uploaded_data, index_col=0, header=None)
            else:
                # 首行首列均不作为名称
                df_data = load_and_read_data(uploaded_data, index_col=None, header=None)
            # 如果DataFrame不是None，显示数据表
            if df_data is not None:
                st.subheader('数据预览：')
                st.dataframe(df_data)  # 使用st.dataframe显示数据
        else:
            st.subheader('原始数据')
            st.dataframe(df_data)  # 使用 st.dataframe 显示数据

# 绘图
        st.markdown('***')            
        if 'show_plot' not in st.session_state:
            st.session_state['show_plot'] = False
        if st.button('运行结果'):
            st.session_state['show_plot'] = True
        else:
            st.session_state['show_plot'] = False
        if st.session_state.get('show_plot', False):
        # st.subheader('Result：')
            scatter_plot = Scatter_Plot(df_data,
                                        df_group=df_group,
                                        group_names=group_names,
                                        selected_text=selected_text,
                                        if_selected_color=toggle_state,   
                                        group_color=selected_color,
                                        marker_size=marker_size,
                                        symbol=symbol,
                                        if_lg=if_lg,
                                        if_line=if_line,
                                        if_text=if_text,
                                        if_no_bg=if_no_bg,

                                        title=title,
                                        x_title=x_title,
                                        y_title=y_title,
                                        if_legend=if_legend,
                                        legent_text=legent_text,
                                        legend_orientation=legend_orientation,
                                        font_family=font_family,
                                        font_size=font_size,
                                        plotly_template=plotly_template,
                                        fig_formats=fig_formats,
                                        workdir=workdir,
                                        
                                        width=width,
                                        height=height,
                                        opacity=opacity,
                                        title_font_size=title_font_size,
                                        legend_font_size=legend_font_size,
                                        x_title_font_size=x_title_font_size,
                                        y_title_font_size=y_title_font_size,
                                        )
            st.plotly_chart(scatter_plot, use_container_width=False, theme=None)
    # except Exception as e:
    #     error_placeholder.error(f'参数设置错误，请检查：{e}')

def Scatter_Plot(df_data, df_group=None, if_selected_color='离散颜色集', group_names=None, selected_text=None,
             group_color=None, marker_size=6, symbol='circle', if_lg='no', if_line='no', if_text='yes', if_no_bg='no',
             title=None, x_title=None, y_title=None, if_legend='yes', legent_text=None,
             legend_orientation=None, font_family=None, font_size=None, 
             plotly_template=None, fig_formats=None, workdir=None,
             width=None, height=None, opacity=None, title_font_size=None,
             legend_font_size=None, x_title_font_size=None, y_title_font_size=None):
    # 参数验证
    if not isinstance(df_data, pd.DataFrame):
        raise ValueError("df_data 应该是一个 pandas DataFrame")
    
    # 初始化变量
    y_columns = df_data.columns[1:] # 默认y轴数据
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

    if_legend = True if if_legend == 'yes' else False
    print(if_legend)

    # 设置主题
    plot_bgcolor, paper_bgcolor, font_color = update_layout_by_theme(plotly_template)
    plotly_template = None if plotly_template == 'none' else plotly_template
    # 模式选择
    mode = 'markers'
    if if_text == 'yes' and if_line == 'yes':
        mode = 'markers+text+lines'
    elif if_text == 'yes':
        mode = 'markers+text'
    elif if_line == 'yes':
        mode = 'markers+lines'

    # 制定显示文本
    if selected_text:
        text = [text if text.upper() in selected_text else None for text in df_data.index]
    else:
        text = df_data.index
    
    # 构建图形
    fig = go.Figure()
    for i, column in enumerate(y_columns):
        x = np.log10(df_data.iloc[:, 0]) if if_lg == 'yes' else df_data.iloc[:, 0]
        y = np.log10(df_data[column]) if if_lg == 'yes' else df_data[column]
        fig.add_trace(go.Scatter(
            x=x,  # 对于柱状图，x 是类别名称
            y=y,  
            name=group_names[i],
            marker=dict(size=marker_size, 
                        symbol=symbol[i % len(symbol)] if symbol else 'circle', 
                        color=colors[i % len(colors)], 
                        ),
            mode=mode,
            line=dict(color='#404040', width=2),
            # textposition='top right',
            hovertext=df_data.index,
            text=text if if_text == 'yes' else None,
            textposition='top center',
            opacity=opacity,
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
    #         plot_path = os.path.join(workdir, 'output_files', f"Bar_Plot.{fmt}")
    #         fig.write_html(plot_path) if fmt == 'html' else fig.write_image(plot_path, width=width, height=height, scale=2, engine='orca')
     # 创建图表下载按钮
    sub_col1, sub_col2 = st.columns(2)
    for i, file_format in enumerate(fig_formats):
        with sub_col1 if i % 2 == 0 else sub_col2:
            filename = f"Violin_Plot"
            create_download_button(fig, file_format, width=width, height=height, scale=2, filename=filename)

    return fig