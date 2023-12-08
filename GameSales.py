import streamlit as st
import pandas as pd
import plotly.express as px

# Create Interface
st.set_page_config(layout="wide")
st.sidebar.title("Choose a visualization:")
genre = st.sidebar.radio(
    "Choose the data you wish to see:", ["1: Popular gaming platform", "2: Popular game genres", "3: The top 5 games in each genre"],
    captions = ["See the most popular gaming platforms", "See the most popular game genres", "See the best selling games from each genre"])

if genre == '1: Popular gaming platform':
    # Open the data
    gameSales = pd.read_csv("vgsales.csv")

    # Q1 What is the most popular gaming platform?
    # clean up data
    # Remove rows where Year has no value
    gameSales = gameSales.dropna(subset=['Year'])

    # Create a sidebar with a radio button filter for Region
    selected_region = st.sidebar.radio("Select the Region You Wish to See:", ['All Regions', 'North America', 'Europe', 'Japan', 'Other'])

    # Display the selected region
    st.title("Most Popular Gaming Platforms Across Multiple Regions:")

    # Map selected region to the corresponding sales column
    sales_column_mapping = {
        'All Regions': 'Global_Sales',
        'North America': 'NA_Sales',
        'Europe': 'EU_Sales',
        'Japan': 'JP_Sales',
        'Other': 'Other_Sales'
    }

    selected_sales_column = sales_column_mapping.get(selected_region, 'Global_Sales')

    # Set the minimum and maximum range of the Year slider
    min_year, max_year = int(gameSales['Year'].min()), int(gameSales['Year'].max())
    selected_year_range = st.sidebar.slider("Select the Year Range:", min_year, max_year, (min_year, max_year))

    st.subheader(
        f'Total Sales by Platform in {selected_region} for the Year Range {selected_year_range[0]} to {selected_year_range[1]}')

    # Filter data based on the selected year range
    filtered_data_by_year = gameSales[(gameSales['Year'] >= selected_year_range[0]) & (gameSales['Year'] <= selected_year_range[1])]

    # Convert 'Platform' column to string
    filtered_data_by_year['Platform'] = filtered_data_by_year['Platform'].astype(str)

    # Calculate and display the total number of sales based on the platform
    total_sales_by_platform_filtered = filtered_data_by_year.groupby('Platform')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']].sum()
    total_sales_by_platform_filtered = total_sales_by_platform_filtered.sort_values(by='Global_Sales', ascending=False)

    # Display the table
    # st.write(f"Total Sales by Platform in the Year Range {selected_year_range[0]} to {selected_year_range[1]}:")
    # st.write(total_sales_by_platform_filtered)

    # Create a bar chart using Plotly Express for the selected region and year range
    fig = px.bar(
        filtered_data_by_year.groupby('Platform')[[selected_sales_column]].sum().sort_values(by=selected_sales_column, ascending=False).reset_index(),
        x='Platform', y=selected_sales_column,
        labels={selected_sales_column: f'Sales in {selected_region} (in millions)', 'Platform': 'Game Platform'},
        )

    # Set the 'Platform' column as category to ensure correct ordering on the x-axis
    fig.update_xaxes(type='category')
    #fig.update_layout(width=1000)

    # Display the bar chart
    st.plotly_chart(fig)

elif genre == '2: Popular game genres':
    # Open the data
    gameSales = pd.read_csv("vgsales.csv")

    # Q2 What are the most popular game genres?
    # clean up data
    # Remove rows where Year has no value
    gameSales = gameSales.dropna(subset=['Year'])

    # Create a sidebar with a radio button filter for Region
    selected_region = st.sidebar.radio("Select the Region You Wish to See:",
                                       ['All Regions', 'North America Regions', 'Europe Regions', 'Japan Regions', 'Other Regions'])

    # Display the selected region
    st.title("Most Popular Game Genres:")

    # Map selected region to the corresponding sales column
    sales_column_mapping = {
        'All Regions': 'Global_Sales',
        'North America Regions': 'NA_Sales',
        'Europe Regions': 'EU_Sales',
        'Japan Regions': 'JP_Sales',
        'Other Regions': 'Other_Sales'
    }

    # Radio button to choose between "Top 5 Genres" and "All Genres"
    display_option = st.sidebar.radio("Choose Display Option:", ['Top 5 Genres', 'All Genres'])

    # Set the minimum and maximum range of the Year slider
    min_year, max_year = int(gameSales['Year'].min()), int(gameSales['Year'].max())
    selected_year_range = st.sidebar.slider("Select the Year Range:", min_year, max_year, (min_year, max_year))

    # Define a function to show the bar chart based on a sales column
    def show_bar_chart(sales_column, region_name, display_option, year_range):
        st.subheader(f"{display_option} in {region_name} ({year_range[0]} - {year_range[1]}):")

        # Filter data based on the selected year range
        filtered_data_by_year = gameSales[(gameSales['Year'] >= year_range[0]) & (gameSales['Year'] <= year_range[1])]

        # Calculate total sales and get all genres if All Genres option is selected
        if display_option == 'All Genres':
            total_sales_by_genre = filtered_data_by_year.groupby('Genre')[sales_column].sum().sort_values(
                ascending=False)
        else:
            # Get the top 5 genres
            total_sales_by_genre = filtered_data_by_year.groupby('Genre')[sales_column].sum().sort_values(
                ascending=False).head(5)

        # Create a bar chart using Plotly Express
        fig = px.bar(total_sales_by_genre, x=total_sales_by_genre.index, y=sales_column,
                     labels={sales_column: f'Sales in {region_name} (in millions)', 'index': 'Game Genre'},
                     )
        # Set height width
        #fig.update_layout(width=600, margin=dict(l=20, r=60, t=40, b=20))

        # Display the selected bar chart
        st.plotly_chart(fig)

    # Define a function to show the pie chart based on a sales column
    def show_pie_chart(sales_column, region_name, display_option, year_range):
        st.subheader(f"Percentage of {display_option} in {region_name} ({year_range[0]} - {year_range[1]}):")

        # Filter data based on the selected year range
        filtered_data_by_year = gameSales[(gameSales['Year'] >= year_range[0]) & (gameSales['Year'] <= year_range[1])]

        # Calculate total sales and get the top 5 genres if Top 5 Genres option is selected
        if display_option == 'Top 5 Genres':
            total_sales_by_genre = filtered_data_by_year.groupby('Genre')[sales_column].sum().sort_values(
                ascending=False)
            top_genres = total_sales_by_genre.head(5)
        else:
            total_sales_by_genre = filtered_data_by_year.groupby('Genre')[sales_column].sum().sort_values(
                ascending=False)
            top_genres = total_sales_by_genre

        # Calculate the percentage of total sales for each genre
        percentage_data = (top_genres / top_genres.sum()) * 100

        # Create a pie chart using Plotly Express
        fig_pie = px.pie(percentage_data, names=percentage_data.index, values=sales_column,
                         labels={'value': f'Sales Percentage', 'index': 'Game Genre'},
                         )
        # Set height width
        #fig_pie.update_layout(width=550, margin=dict(l=70, r=30, t=0, b=60))

        # Display the selected pie chart
        st.plotly_chart(fig_pie)

    # Show bar and pie charts one below the other
    for region, sales_column in sales_column_mapping.items():
        if region == selected_region:
            # Show bar chart
            show_bar_chart(sales_column, selected_region, display_option, selected_year_range)

            # Show pie chart
            show_pie_chart(sales_column, selected_region, display_option, selected_year_range)

else:
    # Open the data
    gameSales = pd.read_csv("vgsales.csv")

    # Q3 What are the top 5 games in each genre and region?
    # Clean up data
    # Remove rows where Year has no value
    gameSales = gameSales.dropna(subset=['Year'])

    # Specify the sales columns with displaying text
    sales_columns_mapping = {
        'Global_Sales': 'All Regions',
        'NA_Sales': 'North America Regions',
        'EU_Sales': 'Europe Regions',
        'JP_Sales': 'Japan Regions',
        'Other_Sales': 'Other Regions'
    }

    # Create a sidebar with a select box filter for Region
    selected_region = st.sidebar.radio("Select the Region:", list(sales_columns_mapping.values()))

    # Create a sidebar with a multiselect filter for Genre
    all_genres = gameSales['Genre'].unique()
    selected_genres = st.sidebar.multiselect("Select Game Genre(s):", all_genres, default=all_genres)

    # Find the corresponding sales column based on the selected region
    selected_sales_column = next(key for key, value in sales_columns_mapping.items() if value == selected_region)

    # Create a sidebar with a slider filter for Year
    min_year, max_year = int(gameSales['Year'].min()), int(gameSales['Year'].max())
    selected_year_range = st.sidebar.slider("Select the Year Range:", min_year, max_year, (min_year, max_year))

    # Display the selected region and year range within the title
    st.title("Top 5 Games Sales in Each Genre")

    # Display the subheader
    st.subheader(f"Top 5 Games by Genre in {selected_region} from {selected_year_range[0]} to {selected_year_range[1]}")

    # Create two columns for the buttons
    chart_view_button, table_view_button = st.columns([1,5])

    # Add buttons to toggle between Chart view and Table view
    chart_view_clicked = chart_view_button.button("Chart View", key="chart_button", help="Switch to Chart view")
    table_view_clicked = table_view_button.button("Table View", key="table_button", help="Switch to Table view")

    # Set the default view to Chart view
    view_mode = "table" if table_view_clicked else "chart"

    # Display the top 5 games for each selected genre, based on the selected sales column and within the selected year range
    filtered_data = gameSales[
        (gameSales['Genre'].isin(selected_genres)) & (gameSales['Year'] >= selected_year_range[0]) & (
                gameSales['Year'] <= selected_year_range[1])]
    top_games_by_genre = filtered_data.groupby('Genre').apply(
        lambda group: group.nlargest(5, selected_sales_column)).reset_index(drop=True)

    # Add Platform information in parentheses
    top_games_by_genre['Name'] = top_games_by_genre.apply(lambda row: f"{row['Name']} ({row['Platform']})", axis=1)

    # Toggle between Chart view and Table view based on the button click
    if view_mode == "chart":
        # Create a bar chart using Plotly Express with inverted x-axis and y-axis
        fig = px.bar(top_games_by_genre.sort_values(by=selected_sales_column, ascending=False), x='Name',
                     y=selected_sales_column,
                     labels={'Name': 'Game Name', selected_sales_column: 'Sales'},
                     color='Genre',  # Use a different color for each genre
                     category_orders={"Genre": top_games_by_genre['Genre'].unique()}
                     )
        # Set height width
        #fig.update_layout(height=650, width=1200)

        # Display the bar chart
        st.plotly_chart(fig)
    else:
        # Display the corresponding table for the selected region
        selected_region_table = top_games_by_genre[['Name', 'Genre', 'Year', 'Publisher', selected_sales_column]].copy()

        # Convert 'Year' column to string and remove ".0"
        selected_region_table['Year'] = selected_region_table['Year'].astype(int).astype(str)

        # Apply formatting for sales values
        selected_region_table[selected_sales_column] = selected_region_table[selected_sales_column].apply(
            lambda x: f"{x:.2f} million")

        # Rename the columns
        selected_region_table = selected_region_table.rename(columns={
            'Name': 'Game Title',
            'Genre': 'Game Genre',
            'Year': 'Release Year',
            'Publisher': 'Game Publisher',
            selected_sales_column: f'Sales ({sales_columns_mapping[selected_sales_column]})'
        })

        st.write(selected_region_table)
