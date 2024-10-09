import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
import io
from sklearn.preprocessing import LabelEncoder
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report





def is_normalized(df):
    # Check if data is approximately in the range [0, 1] or [-1, 1]
    return np.all((df.min() >= -1.001) & (df.max() <= 1.001))

    #/////////////////////////////
    
def generate_data_profile(df):
    profile = pandas_profiling.ProfileReport(df, title="Pandas Profiling Report", explorative=True)
    return profile.to_html()

    #/////////////////////////////
    
def data_operations(df):
    st.sidebar.title("🛠️ Data Operations")
    
    #/////////////////////////////
    
def is_normalized(series):
    # Check if data is approximately in the range [0, 1] or [-1, 1]
    return np.all((series.min() >= -1.001) & (series.max() <= 1.001))

   #/////////////////////////////

def display_preview(dataframe, num_rows=5):
    st.subheader("Dataset Preview (First 5 rows)")
    st.dataframe(dataframe.head(num_rows))
    st.write(f"Total rows: {len(dataframe)}, Total columns: {len(dataframe.columns)}")
    
def train_model(df, target_column, feature_columns):
    X = df[feature_columns]
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.fit(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
#/////////////////////////////         

def data_operations(df):
    st.sidebar.title("🛠️ Data Operations")
    operation_type = st.sidebar.radio("Select Operation Type", ["check Data details","Column Handling", "Pre-Processing", "Advanced Operations", "Feature Engineering","Model Training"])

    display_preview(df)
    
    if operation_type == "check Data details":
         st.write("### Generate Data Profile")
         if st.button("Generate Data Profile"):
                with st.spinner("Generating Data Profile... This may take a moment."):
                    profile_html = generate_data_profile(df)
                    st.components.v1.html(profile_html, height=600, scrolling=True)
 
 #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   

    elif operation_type == "Column Handling":
        st.sidebar.subheader("Column Handling")
        column_operation = st.sidebar.selectbox("Select Column Operation", 
            ["Column Preview", "Column Statistics", "Rename Column", "Add New Column", 
             "Drop Column", "Add Duplicate Column", "Check Duplicate Columns", 
             "Change Data Type", "Check Unique Values"])

        if column_operation == "Column Preview":
            preview_columns = st.sidebar.multiselect("Select columns to preview", df.columns)
            if preview_columns:
                st.write("### Column Preview")
                st.write(df[preview_columns])
                

        elif column_operation == "Column Statistics":
            stat_column = st.sidebar.selectbox("Select a column for statistics", df.columns)
            stat_operations = st.sidebar.multiselect("Select operations", ["Mode", "Median", "Mean"])
            if stat_operations:
                st.write(f"### Statistics for {stat_column}")
                if "Mode" in stat_operations:
                    mode_value = df[stat_column].mode().values
                    st.write(f"Mode: {mode_value}")
                if "Median" in stat_operations:
                    median_value = df[stat_column].median()
                    st.write(f"Median: {median_value}")
                if "Mean" in stat_operations:
                    mean_value = df[stat_column].mean()
                    st.write(f"Mean: {mean_value}")

        elif column_operation == "Rename Column":
            rename_column = st.sidebar.selectbox("Select a column to rename", df.columns)
            new_name = st.sidebar.text_input("New name for the column", "")
            if st.sidebar.button("Rename Column"):
                if new_name:
                    df.rename(columns={rename_column: new_name}, inplace=True)
                    st.success(f"Column '{rename_column}' renamed to '{new_name}'")
                    display_preview(df)
                else:
                    st.warning("Please enter a new name for the column.")

        elif column_operation == "Add New Column":
            new_col_name = st.sidebar.text_input("Enter new column name")
            new_col_value = st.sidebar.text_input("Enter value or formula (use 'df' for existing columns)")
            if st.sidebar.button("Add New Column"):
                if new_col_name and new_col_value:
                    try:
                        df[new_col_name] = eval(new_col_value)
                        st.success(f"Added new column '{new_col_name}'")
                        display_preview(df)
                    except Exception as e:
                        st.error(f"Error adding new column: {e}")
                else:
                    st.warning("Please enter both column name and value/formula")

        elif column_operation == "Drop Column":
            columns_to_drop = st.sidebar.multiselect("Select columns to drop", df.columns)
            if st.sidebar.button("Drop Selected Columns"):
                df.drop(columns=columns_to_drop, inplace=True)
                st.success(f"Dropped columns: {', '.join(columns_to_drop)}")
                display_preview(df)

        elif column_operation == "Add Duplicate Column":
            col_to_duplicate = st.sidebar.selectbox("Select column to duplicate", df.columns)
            new_col_name = st.sidebar.text_input("Enter name for the duplicate column")
            if st.sidebar.button("Add Duplicate Column"):
                if new_col_name:
                    df[new_col_name] = df[col_to_duplicate]
                    st.success(f"Created duplicate column '{new_col_name}' from '{col_to_duplicate}'")
                    display_preview(df)
                else:
                    st.warning("Please enter a name for the duplicate column")

        elif column_operation == "Check Duplicate Columns":
            st.write("### Duplicate Columns Check")
            duplicate_cols = df.columns[df.columns.duplicated()].unique()
            if len(duplicate_cols) > 0:
                st.write("Duplicate columns found:")
                st.write(duplicate_cols)
            else:
                st.write("No duplicate columns found.")

        elif column_operation == "Change Data Type":
            col_to_change = st.sidebar.selectbox("Select column to change data type", df.columns)
            new_dtype = st.sidebar.selectbox("Select new data type", ["int64", "float64", "string", "datetime64"])
            if st.sidebar.button("Change Data Type"):
                try:
                    if new_dtype == "datetime64":
                        df[col_to_change] = pd.to_datetime(df[col_to_change])
                    else:
                        df[col_to_change] = df[col_to_change].astype(new_dtype)
                    st.success(f"Changed data type of '{col_to_change}' to {new_dtype}")
                    display_preview(df)
                except Exception as e:
                    st.error(f"Error changing data type: {e}")

        elif column_operation == "Check Unique Values":
            unique_col = st.sidebar.selectbox("Select column to check unique values", df.columns)
            if st.sidebar.button("Show Unique Values"):
                unique_values = df[unique_col].unique()
                st.write(f"### Unique Values in {unique_col}")
                st.write(unique_values)
                
    #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                     #<       preprocessing    >

    elif operation_type == "Pre-Processing":
        st.sidebar.subheader("Pre-Processing")
        preprocessing_operation = st.sidebar.selectbox("Select Pre-Processing Operation", 
            ["Check Basic Stats", "Data Summary", "Find Missing Values", "Handle Missing Values", 
             "Detect Outliers", "Check Data Types", "Normalize Data"])
        
        if preprocessing_operation == "Data Summary":
            st.write("### Data Summary")
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)

        elif preprocessing_operation == "Check Basic Stats":
            st.write("### Basic Statistics")
            st.write(df.describe())

        elif preprocessing_operation == "Find Missing Values":
            st.write("### Missing Values Summary")
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
            st.write(missing_data)
            
            if not missing_data.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                missing_data.plot(kind='bar', ax=ax)
                plt.title('Missing Values by Column')
                plt.ylabel('Count of Missing Values')
                st.pyplot(fig)

        elif preprocessing_operation == "Handle Missing Values":
            column_to_handle = st.sidebar.selectbox("Select column to handle missing values", df.columns)
            handling_method = st.sidebar.selectbox("Select handling method", 
                ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode", "Fill with custom value"])
            
            if handling_method == "Fill with custom value":
                custom_value = st.sidebar.text_input("Enter custom value")
            
            if st.sidebar.button("Apply Handling"):
                if handling_method == "Drop rows":
                    df.dropna(subset=[column_to_handle], inplace=True)
                elif handling_method == "Fill with mean":
                    df[column_to_handle].fillna(df[column_to_handle].mean(), inplace=True)
                elif handling_method == "Fill with median":
                    df[column_to_handle].fillna(df[column_to_handle].median(), inplace=True)
                elif handling_method == "Fill with mode":
                    df[column_to_handle].fillna(df[column_to_handle].mode()[0], inplace=True)
                elif handling_method == "Fill with custom value":
                    df[column_to_handle].fillna(custom_value, inplace=True)
                
                st.success(f"Applied {handling_method} to column {column_to_handle}")
                display_preview(df)

        elif preprocessing_operation == "Detect Outliers":
            column_to_check = st.sidebar.selectbox("Select column to check for outliers", df.select_dtypes(include=[np.number]).columns)
            
            Q1 = df[column_to_check].quantile(0.25)
            Q3 = df[column_to_check].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[column_to_check] < lower_bound) | (df[column_to_check] > upper_bound)]
            
            st.write(f"### Outliers in {column_to_check}")
            st.write(f"Number of outliers: {len(outliers)}")
            st.write("Outlier rows:")
            st.write(outliers)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x=df[column_to_check], ax=ax)
            plt.title(f'Boxplot of {column_to_check}')
            st.pyplot(fig)

        elif preprocessing_operation == "Check Data Types":
            st.write("### Data Types")
            st.write(df.dtypes)

        elif preprocessing_operation == "Normalize Data":
            col_to_normalize = st.sidebar.selectbox("Select column to normalize", df.select_dtypes(include=[np.number]).columns)
            normalization_method = st.sidebar.selectbox("Select normalization method", ["Min-Max Scaling", "Standardization"])
            
            if st.sidebar.button("Normalize"):
                if normalization_method == "Min-Max Scaling":
                    scaler = MinMaxScaler()
                    df[col_to_normalize] = scaler.fit_transform(df[[col_to_normalize]])
                elif normalization_method == "Standardization":
                    scaler = StandardScaler()
                    df[col_to_normalize] = scaler.fit_transform(df[[col_to_normalize]])
                
                st.success(f"Normalized column '{col_to_normalize}' using {normalization_method}")
                display_preview(df)
                
                
                
    #////////////////////////////////////////////////////////////////////////////////////////////////////
                        #///  ADVANCE OPERATIONS ///
                        
                        
                        
    elif operation_type == "Advanced Operations":
        st.sidebar.subheader("Advanced Operations")
        advanced_operation = st.sidebar.selectbox("Select Advanced Operation", 
            ["Group By","Pivot Table", "Merge DataFrames","Compare Columns","Encode categorical data","Feature Engineering"])
        
        if advanced_operation == "Group By":
            group_by_col = st.sidebar.selectbox("Select column to group by", df.columns)
            agg_function = st.sidebar.selectbox("Select aggregation function", ["mean", "sum", "count", "min", "max"])
            if st.sidebar.button("Apply Group By"):
                grouped_data = df.groupby(group_by_col).agg(agg_function)
                st.write("### Grouped Data")
                st.write(grouped_data)

        elif advanced_operation == "Pivot Table":
            index_col = st.sidebar.selectbox("Select index column", df.columns)
            columns_col = st.sidebar.selectbox("Select columns for pivot", df.columns)
            values_col = st.sidebar.selectbox("Select values column", df.columns)
            agg_function = st.sidebar.selectbox("Select aggregation function", ["mean", "sum", "count", "min", "max"])
            if st.sidebar.button("Create Pivot Table"):
                pivot_data = pd.pivot_table(df, index=index_col, columns=columns_col, values=values_col, aggfunc=agg_function)
                st.write("### Pivot Table")
                st.write(pivot_data)

        elif advanced_operation == "Merge DataFrames":
            st.write("### Merge DataFrames")
            merge_type = st.sidebar.selectbox("Select Merge Type", ["inner", "outer", "left", "right"])
            st.sidebar.text("DataFrame to merge")
            uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
            if uploaded_file:
                new_df = pd.read_csv(uploaded_file)
                merge_on = st.sidebar.selectbox("Select column to merge on", df.columns.intersection(new_df.columns))
                if st.sidebar.button("Merge DataFrames"):
                    merged_df = pd.merge(df, new_df, on=merge_on, how=merge_type)
                    st.write("### Merged DataFrame")
                    display_preview(merged_df)      
    
    if st.sidebar.checkbox("Compare Columns"):
     st.write("### Compare Two Columns Note : Please before doing any filteration fill the missing values first")
    column1 = st.sidebar.selectbox("Select the first column for comparison", df.columns)
    column2 = st.sidebar.selectbox("Select the second column for comparison", df.columns)
    unique_values_column2 = df[column2].unique()
    selected_values_column2 = st.sidebar.multiselect(
        f"Select values from {column2}",
        unique_values_column2
    )

    # Button to compare the columns
    if st.sidebar.button("Compare Columns"):
        # Filter the DataFrame based on selected values
        filtered_data = df[
            #(df[column1].isin(selected_values_column1)) &
            (df[column2].isin(selected_values_column2))
        ]

        # Create a DataFrame to show the comparison
        comparison_data = filtered_data[[column1, column2]].copy()

        # Create a new column to indicate whether the values in the two columns are equal or not
        comparison_data['Comparison Result'] = comparison_data[column1] == comparison_data[column2]

        # Display the comparison DataFrame
        st.write("### Comparison Result")
        st.write(comparison_data)
    
    if operation_type == "Feature Engineering":
        st.subheader("Feature Engineering")
        feature_operation = st.selectbox(
            "Select Feature Engineering Operation",
            ["Create New Column", "Transform Existing Column", "Feature Scaling", "Feature Encoding", "Binning"]
        )

        if feature_operation == "Create New Column":
            column1 = st.selectbox("Select the first column", df.columns)
            column2 = st.selectbox("Select the second column", df.columns)
            operation = st.selectbox("Select the operation", ["Add", "Subtract", "Multiply", "Divide"])
            
            if st.button("Create New Column"):
                if operation == "Add":
                    df['New Column'] = df[column1] + df[column2]
                elif operation == "Subtract":
                    df['New Column'] = df[column1] - df[column2]
                elif operation == "Multiply":
                    df['New Column'] = df[column1] * df[column2]
                elif operation == "Divide":
                    df['New Column'] = df[column1] / df[column2].replace(0, np.nan)
                
                st.success("New column created successfully!")
                st.write(df[['New Column']].head())

        elif feature_operation == "Transform Existing Column":
            column_to_transform = st.sidebar.selectbox("Select the column to transform", df.columns)
            transformation = st.sidebar.selectbox("Select transformation", ["Log", "Square Root", "Square"])
            
            if st.sidebar.button("Transform Column"):
                if transformation == "Log":
                    df['Transformed Column'] = np.log(df[column_to_transform].replace(0, np.nan))
                elif transformation == "Square Root":
                    df['Transformed Column'] = np.sqrt(df[column_to_transform].replace(0, np.nan))
                elif transformation == "Square":
                    df['Transformed Column'] = df[column_to_transform] ** 2
                
                st.success("Column transformed successfully!")
                st.write(df[['Transformed Column']].head())

        elif feature_operation == "Feature Scaling":
            column_to_scale = st.sidebar.selectbox("Select the column to scale", df.columns)
            scaling_method = st.sidebar.selectbox("Select Scaling Method", ["Standardization", "Normalization"])
            
            if st.sidebar.button("Scale Column"):
                if scaling_method == "Standardization":
                    df['Scaled Column'] = (df[column_to_scale] - df[column_to_scale].mean()) / df[column_to_scale].std()
                elif scaling_method == "Normalization":
                    df['Scaled Column'] = (df[column_to_scale] - df[column_to_scale].min()) / (df[column_to_scale].max() - df[column_to_scale].min())
                
                st.success("Column scaled successfully!")
                st.write(df[['Scaled Column']].head())

        elif feature_operation == "Feature Encoding":
            column_to_encode = st.sidebar.selectbox("Select the column to encode", df.columns)
            encoding_method = st.sidebar.selectbox("Select Encoding Method", ["Label Encoding", "One-Hot Encoding"])
            
            if st.sidebar.button("Encode Column"):
                if encoding_method == "Label Encoding":
                    le = LabelEncoder()
                    df['Encoded Column'] = le.fit_transform(df[column_to_encode])
                elif encoding_method == "One-Hot Encoding":
                    df = pd.get_dummies(df, columns=[column_to_encode], drop_first=True)
                    
                st.success("Column encoded successfully!")
                st.write(df.head())

        elif feature_operation == "Binning":
            column_to_bin = st.sidebar.selectbox("Select the column to bin", df.select_dtypes(include=[np.number]).columns)
            binning_method = st.sidebar.selectbox("Select Binning Method", ["Equal-Width Binning", "Custom Binning"])
            
            if binning_method == "Equal-Width Binning":
                num_bins = st.sidebar.slider("Select number of bins", 2, 10, 5)
                if st.sidebar.button("Bin Column"):
                    df['Binned Column'] = pd.cut(df[column_to_bin], bins=num_bins)
                    st.success(f"Column binned into {num_bins} bins!")
                    st.write(df[['Binned Column']].head())
            
            elif binning_method == "Custom Binning":
                bin_edges = st.sidebar.text_input("Enter custom bin edges (comma-separated values)", "0, 10, 20, 30, 50")
                labels = st.sidebar.text_input("Enter labels for the bins (comma-separated)", "Low, Medium, High")
                
                if st.sidebar.button("Bin Column with Custom Ranges"):
                    try:
                        bin_edges = [float(x) for x in bin_edges.split(',')]
                        labels = labels.split(',')
                        df['Binned Column'] = pd.cut(df[column_to_bin], bins=bin_edges, labels=labels)
                        st.success("Column binned with custom ranges successfully!")
                        st.write(df[['Binned Column']].head())
                    except:
                        st.error("Please ensure the bin edges and labels are correctly entered.")
                        
    #elif operation_type =="Model Training":
    # train_model(df, target_column, feature_columns):
    #X = df[feature_columns]
    #y = df[target_column]
   # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    #model = RandomForestClassifier(n_estimators=100, random_state=42)
    #model.fit(X_train, y_train)
    
    #predictions = model.fit(X_test)
    #accuracy = accuracy_score(y_test, predictions)
    #report = classification_report(y_test, predictions)
    
    #return accuracy, report

# In the main function:
    #if st.sidebar.checkbox("Enable Machine Learning"):
     #t#arget_column = st.selectbox("Select target column", df.columns)
     #feature_columns = st.multiselect("Select feature columns", df.columns)
    #if st.button("Train Model"):
        #accuracy, report = train_model(df, target_column, feature_columns)
        #st.write(f"Model Accuracy: {accuracy}")
        #st.text(report)
        
        