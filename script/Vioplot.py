import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def load_data(uploaded_file):
    """
    Load data from an uploaded file.

    Args:
    uploaded_file: Uploaded file object.

    Returns:
    pd.DataFrame: Loaded data as a DataFrame.
    """
    if uploaded_file is not None:
        try:
            # Check the file format and load data accordingly
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.tsv'):
                return pd.read_csv(uploaded_file, sep='\t')
            elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                return pd.read_excel(uploaded_file)
            else:
                st.error('Unsupported file format!')
                return None
        except Exception as e:
            st.error(f'Error loading data: {e}')
            return None
    else:
        return None

def user_interface():
    """
    Create user interface elements for violin plot settings.

    Returns:
    dict: Dictionary of user settings.
    """
    user_settings = {
        'title': st.text_input('Title of the Plot'),
        'x_title': st.text_input('X-axis Title'),
        'y_title': st.text_input('Y-axis Title'),
        # Add more settings as required
    }

    return user_settings

def draw_violin_plot(data, settings):
    """
    Draw a violin plot using Plotly based on the provided data and settings.

    Args:
    data (pd.DataFrame): Data to plot.
    settings (dict): Plot settings provided by the user.

    Returns:
    plotly.graph_objs.Figure: The generated violin plot.
    """
    fig = go.Figure()

    # Plot each column as a separate violin
    for column in data.columns:
        fig.add_trace(go.Violin(y=data[column], name=column))

    # Apply user-defined settings
    fig.update_layout(
        title=settings.get('title'),
        xaxis_title=settings.get('x_title'),
        yaxis_title=settings.get('y_title'),
        # Add more settings as required
    )

    return fig

def main():
    st.title("Violin Plot Generator")

    # Upload and process data
    uploaded_file = st.file_uploader("Upload your data file", type=['csv', 'tsv', 'xlsx', 'xls'])
    data = load_data(uploaded_file)

    if data is not None:
        # User Interface for settings
        settings = user_interface()

        # Draw Plot
        fig = draw_violin_plot(data, settings)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
