# 全局注释：
# 1. 本程序为ProAnaVis的主程序，用于调用各个模块
# 2. 本程序使用streamlit框架，用于快速搭建网页应用
# 3. 本程序使用了多个第三方库，包括streamlit、plotly等

import streamlit as st
import pandas as pd
import numpy as np
import os

from script.ScatterPlots import ScatterPlot
from script.ScatterPlots import LinearRegressionPlot
from script.ScatterPlots import BubblePlot
# from script.ScatterPlots import PCAPlot
# from script.ScatterPlots import CumulativeFrequencyPlot
from script.ScatterPlots import VolcanoPlot


from script.BarPlots import BarPlot
# from script.BarPlots import BarPlotErrorBars
from script.BarPlots import BarandLinePlot
# from script.BarPlots import HistogramPlot
from script.BarPlots import BoxPlot
from script.BarPlots import ViolinPlot

from script.Help import Manual


def main():
    # 设置工作目录
    workdir = 'ProAnaVis'
    # 设置网页标题
    st.set_page_config(page_title='ProAnaVis', layout='wide')

    # 主要功能选择的选项列表
    main_functions = [
        'Home',
        'Scatter Plots',
        # 'Line Plots',
        'Bar Plots',
        # 'Correlation Plots',
        # 'Area Plots',
        # '3D Plots',
        # 'Map Plots',
        'Help'
    ]
    # 不同模块下的子功能选项列表
    sub_functions = {
        'Scatter Plots': [
            'Scatter Plot',
            'Linear regression Plot',
            'Bubble Plot',
            # 'PCA Plot',
            # 'Cumulative frequency Plot',
            'Volcano Plot',
        ],

        'Line Plots': [
            'Line Plot',
            'Line Plot (Error Bars)',
            'Double Y-axis Line Plot',
        ],

        'Bar Plots': [
            'Bar Plot',
            # 'Bar Plot (Error Bars)',
            'Bar and Line Plot',
            # 'Histogram Plot',
            'Box Plot',
            'Violin Plot',
        ],

        'Correlation Plots': [
            'Heatmap',
            'Corr Heatmap',
            'Corr Scatter Plot',
            'Box Plot',
            'Violin Plot',
        ],

        'Area Plots': [
            'Area Plot',
        ],

        '3D Plots': [
            '3D Scatter Plot',
            '3D Line Plot',
        ],

        'Map Plots': [
            'Map Plot',
        ],

        'Help': [
            'Manual',
        ],
    }
    
    # 创建一个侧边栏，包含菜单选项
    with st.sidebar:
        st.title('ProAnaVis')
        # 创建一个单选按钮来选择活跃的组
        active_group = st.radio('Function selection:', main_functions) # 选择主功能，页面1-8
        st.markdown('<hr style="border-top: 2px solid #bbb; margin-top: 0.5rem; margin-bottom:0.5rem;"/>', unsafe_allow_html=True)

    # 主页面
    # 根据侧边栏的选择，显示不同的页面内容
    if active_group == 'Home':
        # 主内容区域
        st.title('ProAnaVis：简单快速的蛋白质组学数据交互式可视化平台')
        st.write('<p style="font-size: 20px;"> \
                ProAnaVis 是一个针对蛋白质组学数据分析和科学图表制作的在线工具，旨在提供动态交互式的可视化图表制作体验。\
                 该平台支持从标准数据矩阵或其他输入格式生成多种交互式图表，如散点图、线形图、条形图、柱状图、箱形图和小提琴图。\
                 ProAnaVis 基于 streamlit 框架开发，提供了一个直观且用户友好的界面。\
                 一个显著的特点是，ProAnaVis 使得用户无需任何编程技能，便可以轻松快速地完成蛋白质组学数据的可视化，创建适合发表的图表。\
                 通常情况下，绘制图表仅需几次鼠标点击。对于部分图表类型，用户上传数据后即可直接获得可视化结果。\
                 此外，ProAnaVis 提供了多达 33 个自定义参数，以满足各种具体需求。该工具还包括针对专门组学数据分析的特殊图表类型，如火山图和功能富集气泡图。\
                 总而言之，ProAnaVis 是一款高效且功能强大的工具，能够帮助研究人员全面地可视化和解析湿实验室及干实验室产生的数据。 </p>', 
                unsafe_allow_html=True)
        st.markdown('<hr style="border-top: 2px solid #bbb; margin-top: 0.5rem; margin-bottom:0.5rem;"/>', unsafe_allow_html=True)
        # 主内容区域 - 目录部分
        st.subheader('目录：')
        # 创建主页目录
        # 创建两列
        function_description = ['''该部分用于绘制散点图类型的交互式图表。<br>\
            1. Scatter Plot (散点图): 直观展示两个变量间关系，常用于比较不同样本下蛋白质表达水平的相关性。<br>\
            2. Linear Regression Plot (线性回归图): 描述变量间线性关系的强度与方向，适用于分析和预测蛋白质表达量的变化趋势。<br>\
            3. Bubble Plot (气泡图): 散点图的扩展，通过气泡大小展示第三个量化变量，如蛋白质表达量与统计显著性，主要用于富集分析结果可视化。<br>\
            4. PCA Plot (主成分分析图): 主成分分析（PCA）减少数据维度，突出样本间差异和聚类，用于识别数据模式和异常值。<br>\
            5. Volcano Plot (火山图): 展示蛋白质表达差异的显著性，横轴表示表达变化，纵轴显示统计显著性，用于识别显著变化的蛋白质，主要用于差异分析结果可视化。<br>\
                          ''', # 5. Cumulative Frequency Plot (累积频率图): 显示特定值以下观测值的频率，有助于了解蛋白质表达水平的分布范围。<br>\
                          '''该部分用于绘制条形图类型的交互式图表。<br>\
            1. Bar Plot (条形图): 直观展示不同类别的蛋白质表达量，每个条形代表一个类别，长度或高度表现数值大小。<br>\
            2. Bar Plot with Error Bars (带误差线的条形图): 在基础条形图上增加误差线，显示数据变异性或不确定性，关键于展现实验数据的稳定性和可靠性。<br>\
            3. Bar and Line Plot (条形图和线形图结合): 结合条形图和线形图，同时展示蛋白质表达量及其变化趋势，适用于比较多个变量。<br>\
            4. Box Plot (箱形图): 展示数据分布，强调中位数、四分位数和异常值，适合比较不同组别蛋白质表达量的分布特征。<br>\
            5. Violin Plot (小提琴图): 结合箱形图和密度图，详细展示数据分布，特别适用于展示非对称或多峰分布，显示中位数、四分位数及分布形状。<br>\
            ''', # 4. 直方图 (Histogram Plot): 显示数据分布，将数据分组展示频率或数量，有助于识别蛋白质表达的正常范围和异常值。<br>\
            '''用户使用说明。''',]
        col1, col2 = st.columns(2)
        current_col = col1
        for index, function in enumerate(main_functions[1:]):  # 从第二个元素开始，到Help结束
            with current_col:
                st.subheader(function)
                
                st.write(f'<p style="font-size: 20px;">{function_description[index]}</p>', unsafe_allow_html=True)
                df = pd.DataFrame(sub_functions[function], columns=['Functions'])
                st.dataframe(df, hide_index=False, use_container_width=True)
                # 在列之间切换
                if index % 2 == 0:
                    current_col = col2
                else:
                    current_col = col1

    def display_function_content(active_group, page, sub_functions):
        """显示给定功能区块的内容"""
        if page:
            st.title(f'ProAnaVis：简单快速的蛋白质组学数据交互式可视化平台')
            st.markdown("---")
            if page == 'Manual':
                pass
            else:
                st.subheader(page)

            # 调用相应的处理函数
            if page in sub_functions[active_group]:
                process_function = function_processing_mapping.get(page)
                if process_function:
                    process_function(workdir)
                else:
                    st.write("此功能尚未实现。")
            else:
                st.write("未知的子功能。")

    # 每个子功能对应的处理函数
    function_processing_mapping = {
        'Scatter Plot': ScatterPlot.layout_interface,
        'Linear regression Plot': LinearRegressionPlot.layout_interface,
        'Bubble Plot': BubblePlot.layout_interface,
        # 'PCA Plot': PCAPlot.layout_interface,
        # 'Cumulative frequency Plot': CumulativeFrequencyPlot.layout_interface,
        'Volcano Plot': VolcanoPlot.layout_interface,

        
        'Bar Plot': BarPlot.layout_interface,
        'Bar and Line Plot': BarandLinePlot.layout_interface,
        # 'Bar Plot (Error Bars)': BarPlotErrorBars.layout_interface,
        # 'Histogram Plot': HistogramPlot.layout_interface,
        'Box Plot': BoxPlot.layout_interface,
        'Violin Plot': ViolinPlot.layout_interface,
        # ... 其他子功能对应的处理函数
        'Manual': Manual.manual,
    }

    # 每个页面的内容
    for function in main_functions[1:]:
        st.sidebar.header(function)
        page = None
        if active_group == function:
            page = st.sidebar.radio('Function selection:', sub_functions[active_group])
        if page:
            display_function_content(active_group, page, sub_functions)
        st.sidebar.markdown('<hr style="border-top: 2px solid #bbb; margin-top: 0.5rem; margin-bottom:0.5rem;"/>', unsafe_allow_html=True)


    # 版权声明
    st.sidebar.markdown(
                '<h6><p style="font-size: 16px;">Made in  by <a href="https://github.com/Zhangzq-1026?tab=repositories">@ZQ</a></p></h6> ',
                unsafe_allow_html=True,
            )

# 定义主函数mian入口
if __name__ == '__main__':
    main()