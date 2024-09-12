
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
    data_path = os.path.join(workdir, 'input_files', 'demo_Volcano.csv')
    # group_path = os.path.join(workdir, 'input_files', 'Pro_demo_3G_Group_Scatter.csv')

    if not os.path.exists(data_path):
        st.error('默认原始数据文件不存在，请检查！')
        return None, None

    # if not os.path.exists(group_path):
    #     st.error('默认分组数据文件不存在，请检查！')
    #     return None, None

    df_data = pd.read_csv(data_path, sep=',', index_col=0, header=0)
    return df_data


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
    df_data = generate_default_data(workdir)
    if df_data is None:
        return  # 数据文件不存在时，不继续执行
    
    # 创建两列布局
    left_column, right_column = st.columns([1, 2])
    try:
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
                # show_colors = toggle_button('show_colors', '查看 / 隐藏颜色集')
                # # 根据当前状态显示或隐藏颜色集
                # if show_colors:
                #     # 创建离散和连续颜色集的样本图
                #     fig_qualitative = px.colors.qualitative.swatches()
                #     fig_sequential = px.colors.sequential.swatches()
                #     # 调整图表大小
                #     fig_qualitative.update_layout(width=300, height=1000, margin=dict(l=2, r=2, t=30, b=0))  # 根据需要调整大小
                #     fig_sequential.update_layout(width=300, height=1000, margin=dict(l=2, r=2, t=30, b=0))   # 根据需要调整大小
                #     # 使用 Streamlit 的列功能并列显示两个图表
                #     sub_col1, sub_col2 = st.columns(2)
                #     with sub_col1:
                #         st.write("离散颜色集：")
                #         st.plotly_chart(fig_qualitative, use_container_width=True)
                #     with sub_col2:
                #         st.write("连续颜色集：")
                #         st.plotly_chart(fig_sequential, use_container_width=True)
                    
            # 判断用户是选择离散颜色集还是连续颜色集
            toggle_state = radio_toggle("选择颜色集", ["已有颜色集", "自定义颜色集"])
                # st.write("Current State:", toggle_state)
            if toggle_state == '已有颜色集':
                # 获取 Plotly 的所有预设颜色集
                color_qualitative = dir(px.colors.qualitative)
                color_qualitative = [color for color in color_qualitative if not color.startswith("__") and color not in ['_swatches', 'swatches']]
                # 让用户选择一个颜色集
                selected_qualitative_scheme = st.selectbox('选择一个具体离散颜色集：', color_qualitative)
                selected_colors = getattr(px.colors.qualitative, selected_qualitative_scheme)
                # 创建一个下拉菜单让用户选择特定的颜色
                selected_color = st.multiselect('选择 3 个具体的颜色 (顺序为 Down，Nonsignificant，Up)：', selected_colors)  # 返回一个颜色列表
                # st.markdown(selected_color)
                # 展示用户选择的颜色
                st.write('您选择的颜色是:')
                # 使用一个容器来并排展示颜色
                color_container = ""
                for color in selected_color:
                    color_container += f"<span style='display:inline-block; margin: 2px; width: 30px; height: 30px; background-color: {color};'></span>"
                st.markdown(color_container, unsafe_allow_html=True)
            elif toggle_state == '自定义颜色集':
                # 颜色盘参考
                color_reference = st.color_picker('颜色盘参考（可以复制颜色盘中的代号）：', '#FA7F6F')
                # 返回一个颜色列表
                selected_color = st.text_input('有几组就输入几组颜色（用英文逗号隔开）：', '#99CC99, #A9A9A9, #FA7F6F',)
                # 将字符串分割成列表，并去除每个元素两端的空格
                if selected_color.strip():
                    selected_color = [color.strip() for color in selected_color.split(',')]
                else:
                    selected_color = []
                # st.markdown(selected_color)
                    
            # 设置点的大小
            marker_size = st.slider('设置点大小：', min_value=0, max_value=30, value=8)
            
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            # 设置点的形状
            symbol_list = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 
                'triangle-left', 'triangle-right', 'triangle-ne', 'triangle-se', 'triangle-sw', 
                'triangle-nw', 'pentagon', 'hexagon', 'hexagon2', 'octagon', 'star', 'hexagram', 
                'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide']
            with sub_col1:
                symbol_Up = st.selectbox('选择上调点的形状：', symbol_list, index=0)
            with sub_col2:
                symbol_Nonsignificant = st.selectbox('选择无显著性点的形状：', symbol_list, index=0)
            with sub_col3:
                symbol_Down = st.selectbox('选择下调点的形状：', symbol_list, index=0)
            symbol_shape = [symbol_Down, symbol_Nonsignificant, symbol_Up]
            if_p_lg = st.radio('P 值是否取对数？', ('yes', 'no'), horizontal=True, index=0)

            sub_col1, sub_col2= st.columns(2)
            with sub_col1:
                p_threshold = st.slider('P 值阈值：', min_value=0.0, max_value=1.0, value=0.05, step=0.01)
            with sub_col2:
                logFC_threshold = st.slider('log2 Fold Change 阈值：', min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            if_text = st.radio('是否显示文本', ('yes', 'no'), horizontal=True, index=1)
            # 指定显示文本
            selected_text = st.text_input('输入指定显示文本（用英文逗号隔开，不输入则为索引名）：')
            # 检查selected_text是否为空
            if selected_text.strip():
                # 如果不为空，则分割字符串并去除每个元素的空白
                selected_text = [text.strip().upper() for text in selected_text.split(',')]
            else:
                # 如果为空，则返回一个空列表
                selected_text = []   
            sub_col1, sub_col2= st.columns(2)
            with sub_col1:
                if_top_num = st.slider('显示 Top 点文本：', min_value=0, max_value=100, value=0)
            with sub_col2:
                marker_font_size = st.slider('文本字体大小：', min_value=0, max_value=100, value=14)
            if_no_bg = st.radio('是否显示背景（下载为透明背景）？', ('yes', 'no'), horizontal=True, index=1)

        # 通用参数设置
            st.markdown('***')
            st.subheader('通用参数：')
            # 以下是根据图片中的界面创建的参数设置
            sub_col1, sub_col2= st.columns(2)    
            with sub_col1:
                # 图片标题
                title = st.text_input('图片标题（不显示则为空）):', 'Volcano Plot')
                            # X轴标题
                x_title = st.text_input('X 轴标题（不显示则为空）:','log2 Fold Change')
                            # Y轴标题
                y_title = st.text_input('Y 轴标题（不显示则为空）:', '-log10(P.Value)')
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
            # error_placeholder = st.empty()
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
                volcano_plot = Volcano_plot(df_data, if_p_lg=if_p_lg, p_threshold=p_threshold, logFC_threshold=logFC_threshold, 
                                            symbol_num=if_top_num, bubble_size=marker_size, marker_font_size=marker_font_size, group_color=selected_color, 
                                            symbol_shape=symbol_shape, if_text=if_text, selected_text=selected_text, if_no_bg=if_no_bg,
                                            title=title, x_title=x_title, y_title=y_title, if_legend=if_legend, legent_text=legent_text, 
                                            legend_orientation=legend_orientation, font_family=font_family, font_size=font_size, 
                                            plotly_template=plotly_template, fig_formats=fig_formats, workdir=None,
                                            width=width, height=height, opacity=opacity, title_font_size=title_font_size,
                                            legend_font_size=legend_font_size, x_title_font_size=x_title_font_size, 
                                            y_title_font_size=y_title_font_size)

                st.plotly_chart(volcano_plot, use_container_width=False, theme=None)
    except Exception as e:
        error_placeholder.error(f'参数设置错误，请检查：{e}')

def Volcano_plot(df_data, if_p_lg='yes', p_threshold=None, logFC_threshold=1, symbol_num=0, # up_color='#f08d1a', down_color='#7fa4ca', 
                bubble_size=8, marker_font_size=14, group_color=None, symbol_shape=['circle'], if_text='no', selected_text=None, if_no_bg='no',
                title='DE Analysis Volcano Plot', x_title='log2 Fold Change', y_title='-log10(P.Value)', if_legend='yes', legent_text='Conditions',
                legend_orientation=None, font_family=None, font_size=None, 
                plotly_template=None, fig_formats=None, workdir=None,
                width=None, height=None, opacity=None, title_font_size=None,
                legend_font_size=None, x_title_font_size=None, y_title_font_size=None):

    # 重新设置列名
    df_data.columns = ['logFC', 'P.Value']
    # 参数验证
    if not isinstance(df_data, pd.DataFrame):
        raise ValueError("df_data 应该是一个 pandas DataFrame")
    # 处理宽度和高度参数
    width = width * 100 if width else None
    height = height * 100 if height else None
    # 设置颜色方案
    if group_color:
        down_color = group_color[0]
        nonsignificant_color = group_color[1]
        up_color = group_color[2]
    else:
        up_color = '#FA7F6F'
        nonsignificant_color = '#A9A9A9'
        down_color = '#99CC99'
    # 点的形状
    if symbol_shape:
        down_symbol = symbol_shape[0]
        nonsignificant_symbol = symbol_shape[1]
        up_symbol = symbol_shape[2]
    else:
        up_symbol = 'circle'
        nonsignificant_symbol = 'circle'
        down_symbol = 'circle'

    # 设置主题
    plot_bgcolor, paper_bgcolor, font_color = update_layout_by_theme(plotly_template)
    plotly_template = None if plotly_template == 'none' else plotly_template

    mode = 'markers+text' if if_text == 'yes' else 'markers'

    # 如果df中有空值，删除该行
    df_data.dropna(inplace=True)

    # 提取数据
    gene_names = df_data.index.values
    logFC = df_data['logFC'].values
    pvalue = -np.log10(df_data['P.Value'].values) if if_p_lg == 'yes' else df_data['P.Value'].values

    # 根据阈值判断显著性
    significant = (np.abs(logFC) > logFC_threshold) & (df_data['P.Value'].values < p_threshold)
    upregulated = significant & (logFC > 0)
    downregulated = significant & (logFC < 0)
    nonsignificant = ~significant
    
    # 设置图例
    if_legend = True if if_legend == 'yes' else False
    if if_legend:
        # 计算上调和下调基因的数量，并在图像中左上角添加注释
        upregulated_num = np.sum(upregulated)
        up_name = 'Up: '+str(upregulated_num)
        nonsignificant_num = np.sum(nonsignificant)
        no_name = 'Nonsignificant: '+str(nonsignificant_num)
        downregulated_num = np.sum(downregulated)
        down_name = 'Down: '+str(downregulated_num)
    else:
        up_name = None
        no_name = None
        down_name = None

    fig = go.Figure()
    # opacity: 透明度
    # line: 点边界的线条属性
    # sizemode: 指定气泡大小的计算方式
    fig.add_trace(go.Scatter(x=logFC[upregulated], y=pvalue[upregulated], mode=mode,
                            marker=dict(color=up_color, size=bubble_size, sizemode='area',symbol=up_symbol,opacity=opacity,
                                        line=dict(color='black',width=0.4)),
                            name=up_name, showlegend=if_legend, hovertext=df_data[upregulated].index,
                            text=[text if text in selected_text else None for text in df_data[upregulated].index] if selected_text else df_data[upregulated].index, 
                            textposition='top right', textfont=dict(size=marker_font_size)))  # 上调基因的气泡图
    fig.add_trace(go.Scatter(x=logFC[nonsignificant], y=pvalue[nonsignificant], mode=mode,
                            marker=dict(color=nonsignificant_color, size=bubble_size, sizemode='area',symbol=nonsignificant_symbol,opacity=opacity-0.3,
                                        line=dict(color='black',width=0.4)), 
                            name=no_name, showlegend=if_legend, hovertext=df_data[nonsignificant].index,
                            text=[text if text in selected_text else None for text in df_data[nonsignificant].index] if selected_text else df_data[nonsignificant].index,
                            textposition='top center', textfont=dict(size=marker_font_size)))  # 非显著性差异基因的气泡图
    fig.add_trace(go.Scatter(x=logFC[downregulated], y=pvalue[downregulated], mode=mode,
                            marker=dict(color=down_color, size=bubble_size, sizemode='area',symbol=down_symbol,opacity=opacity,
                                        line=dict(color='black',width=0.4)), 
                            name=down_name, showlegend=if_legend, hovertext=df_data[downregulated].index,
                            text=[text if text in selected_text else None for text in df_data[downregulated].index] if selected_text else df_data[downregulated].index, 
                            textposition='top left', textfont=dict(size=marker_font_size)))  # 下调基因的气泡图

    # 判断是否标记所有差异基因,TOP基因
    if symbol_num == 'all':
        symbol_num = len(df_data)
    else:
        symbol_num = int(symbol_num)
    # 给差异最显著的基因添加标签
    df_upregulated = df_data[upregulated].nlargest(symbol_num, 'logFC')
    df_downregulated = df_data[downregulated].nsmallest(symbol_num, 'logFC')
    
    # 添加差异显著的标签信息
    for index, row in df_upregulated.iterrows():
        fig.add_trace(go.Scatter(x=[row['logFC']], y=[-np.log10(row['P.Value'])],
                                 marker=dict(color=up_color, size=bubble_size, sizemode='area',symbol=up_symbol,opacity=0),
                                 text=[index], mode='text+markers',
                                 textposition="top right",
                                 textfont=dict(size=marker_font_size),
                                 showlegend=False,
                                 ))
        
    for index, row in df_downregulated.iterrows():
        fig.add_trace(go.Scatter(x=[row['logFC']], y=[-np.log10(row['P.Value'])],
                                 marker=dict(color=down_color, size=bubble_size, sizemode='area',symbol=down_symbol,opacity=0), 
                                 text=[index], mode='text+markers',
                                 textposition="top left",
                                 # 定义字体大小
                                 textfont=dict(size=marker_font_size),
                                 showlegend=False))

    # 添加阈值线
    x_min = np.min(logFC)
    x_max = np.max(logFC)
    fig.update_layout(shapes=[
        dict(type="line", x0=x_min-1, x1=x_max+1, y0=-np.log10(p_threshold), y1=-np.log10(p_threshold), line=dict(color="Red", width=1.5, dash="dash")),
        dict(type="line", x0=logFC_threshold, x1=logFC_threshold, y0=0, y1=max(pvalue)+2, line=dict(color="Black", width=1.5, dash="dash")),
        dict(type="line", x0=-logFC_threshold, x1=-logFC_threshold, y0=0, y1=max(pvalue)+2, line=dict(color="Black", width=1.5, dash="dash"))
    ])
    
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
            filename = f"Volcano_Plot"
            create_download_button(fig, file_format, width=width, height=height, scale=2, filename=filename)
    return fig