import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import io



#////////////////////////////////////// ** Single column** /////////////////////////////////#

def visualization(df):
    st.sidebar.title("📊 Visualization Options")
    
    plot_type = st.sidebar.radio("Select Plot Type", ["Single Column", "X vs Y", "Multiple Columns"])
    
    if plot_type == "Single Column":
        single_column_plot(df)
    elif plot_type == "X vs Y":
        x_vs_y_plot(df)
    else:
        multiple_column_plot(df)

def single_column_plot(df):
    st.sidebar.subheader('Single Column Plot')
    
    single_col = st.sidebar.selectbox("Select a column for single-column plot", df.columns)
    single_plot_type = st.sidebar.selectbox("Select plot type", [
        'Histogram', 
        'Box Plot',
        'Pie Chart', 
        'Bar Chart', 
        'Heatmap', 
        'Dot Plot', 
        'Radar Chart', 
        'Density Plot'
    ])

    color = st.sidebar.color_picker("Select color for plot", "#1f77b4")

    # Number of bins input for Histogram and Density Plot
    bins = st.sidebar.number_input("Number of bins", min_value=1, value=10)

    if st.sidebar.button("Generate Single Column Plot"):
        st.write(f"### {single_plot_type}: {single_col}")
        fig, ax = plt.subplots()

        if single_plot_type == 'Histogram':
            sns.histplot(df[single_col], bins=bins, color=color, ax=ax)
        
        elif single_plot_type == 'Box Plot':
            sns.boxplot(y=df[single_col], ax=ax, color=color)

        elif single_plot_type == 'Pie Chart':
            # Prepare data for pie chart
            if df[single_col].dtype == 'object':  # Ensure it's categorical data
                counts = df[single_col].value_counts()
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
                ax.axis('equal')  # Equal aspect ratio ensures pie chart is circular.

        elif single_plot_type == 'Bar Chart':
            # Ensure the column is categorical
            if df[single_col].dtype == 'object':
                counts = df[single_col].value_counts()
                sns.barplot(x=counts.index, y=counts.values, ax=ax, color=color)
                ax.set_xticklabels(counts.index, rotation=45)

        elif single_plot_type == 'Heatmap':
            # Create a simple heatmap for a correlation matrix
            corr = df.corr()  # Calculate correlation matrix
            sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)

        elif single_plot_type == 'Dot Plot':
            # Create a dot plot
            sns.stripplot(y=df[single_col], ax=ax, color=color, jitter=True)

        elif single_plot_type == 'Radar Chart':
            # Prepare data for radar chart
            if df[single_col].dtype == 'object':
                counts = df[single_col].value_counts()
                categories = counts.index
                values = counts.values
                angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

                # Complete the loop
                values = np.concatenate((values,[values[0]]))
                angles += angles[:1]

                ax.fill(angles, values, color=color, alpha=0.25)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(categories)
                ax.set_yticklabels([])  # Hide y-tick labels

        elif single_plot_type == 'Density Plot':
            sns.kdeplot(df[single_col], ax=ax, color=color, fill=True, bw_adjust=bins)

        st.pyplot(fig)
       
       
#//////////////////////////////////////////******* X VS Y MULTICOLUMN*****//////////////////////////////////////////////////#
 
def x_vs_y_plot(df):
    st.sidebar.subheader('X vs Y Column Plot')
    x_col = st.sidebar.selectbox("Select X-axis column", df.columns)
    y_col = st.sidebar.selectbox("Select Y-axis column", df.columns)
    plot_type = st.sidebar.selectbox("Select plot type", ['Scatter Plot', 'Line Plot', 'Bar Plot', 'Box Plot', 'Histogram','funnel'])

    if plot_type == 'Histogram':
        bins = st.sidebar.number_input("Number of bins for histogram", min_value=1, value=10)
    color = st.sidebar.color_picker("Select color for plot", "#1f77b4")

    if st.sidebar.button("Generate X vs Y Plot"):
        st.write(f"### {plot_type}: {x_col} vs {y_col}")
        if plot_type == 'Scatter Plot':
            fig = px.scatter(df, x=x_col, y=y_col, color_discrete_sequence=[color])
        elif plot_type == 'Line Plot':
            fig = px.line(df, x=x_col, y=y_col, line_shape='linear', color_discrete_sequence=[color])
        elif plot_type == 'Bar Plot':
            fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=[color])
        elif plot_type == 'Box Plot':
            fig = px.box(df, x=x_col, y=y_col, color_discrete_sequence=[color])
        elif plot_type == 'Histogram':
            fig = px.histogram(df, x=x_col, y=y_col, nbins=bins, color_discrete_sequence=[color])
        elif plot_type == 'funnel':
            fig = px.funnel(df, x=x_col, y=y_col,  color_discrete_sequence=[color])
        st.plotly_chart(fig)


 #//////////////////////////////////////////*******MULTICOLUMN*****//////////////////////////////////////////////////#
 
 
def multiple_column_plot(df):
    st.sidebar.subheader('Multi-Column Visualization')
    multi_columns = st.sidebar.multiselect("Select columns for multi-column visualizations", df.columns)
    multi_plot_type = st.sidebar.selectbox("Select plot type for multi-columns", 
                                           ['Pair Plot', 'Scatter Plot', 'Box Plot', 'Histogram', 'funnel chart'])

    bins = st.sidebar.number_input("Number of bins (for applicable plots)", min_value=1, value=10)

    if st.sidebar.button("Generate Multi-Column Plot"):
        if len(multi_columns) < 2:
            st.warning("Please select at least two columns.")
        else:
            st.write(f"### {multi_plot_type} of {', '.join(multi_columns)}")
            if multi_plot_type == 'Pair Plot':
                pair_plot = sns.pairplot(df[multi_columns])
                st.pyplot(pair_plot.fig)
            elif multi_plot_type == 'Scatter Plot':
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=multi_columns[0], y=multi_columns[1], ax=ax)
                plt.title(f'Scatter Plot: {multi_columns[0]} vs {multi_columns[1]}')
                st.pyplot(fig)
            elif multi_plot_type == 'Box Plot':
                fig, ax = plt.subplots()
                sns.boxplot(data=df[multi_columns], ax=ax)
                plt.title(f'Box Plot of {", ".join(multi_columns)}')
                st.pyplot(fig)
            elif multi_plot_type == 'Histogram':
                fig, ax = plt.subplots()
                for col in multi_columns:
                    sns.histplot(df[col], bins=bins, label=col, kde=True, ax=ax)
                plt.title('Histogram of Selected Columns')
                plt.legend()
                st.pyplot(fig)
