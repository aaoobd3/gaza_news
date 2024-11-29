import streamlit as st
import json

# Load JSON file
@st.cache_data
def load_news_data(file_path):
    with open(file_path, 'r') as file:
        news_data = json.load(file)
    return news_data['news']

# Render news cards
# Render news cards in a gallery layout
def render_news_cards(news_list):
    st.header("Latest News")
    # Determine the number of columns for the card gallery
    columns_per_row = 3  # Customize as needed
    num_news = len(news_list)
    
    for start_idx in range(0, num_news, columns_per_row):
        cols = st.columns(columns_per_row)
        for idx, col in enumerate(cols):
            news_idx = start_idx + idx
            if news_idx < num_news:  # Ensure we don't go out of bounds
                news = news_list[news_idx]
                with col:
                    # Card content
                    if news["top_image"]:
                        col.image(news["top_image"], use_container_width =True)
                    col.subheader(news["title"])
                    st.write(f"**Published on:** {news['published_date']}")
                    # Read More button
                    if col.button("Read More", key=f"read_more_{news_idx}"):
                        st.query_params.news_id=news_idx

# Render full news details
def render_full_news(news):
    st.image(news["top_image"], width=700)
    st.title(news["title"])
    st.write(f"**Published on:** {news['published_date']}")
    st.write(f"**Authors:** {', '.join(news['authors']) if news['authors'] else 'N/A'}")
    st.write("---")
    st.write(news["text"])
    st.write(f"[Original Article]({news['link']})")

# Main Streamlit App
def main():
    
    st.image(
        "https://raw.githubusercontent.com/aaoobd3/gaza_news/refs/heads/main/images/logo.png",width=100
    )
    
    st.divider()
    
    file_path = "news.json"  # Path to your JSON file
    news_list = load_news_data(file_path)
    
    # Check query parameters for navigation
    query_params = st.query_params
    if "news_id" in query_params:
        try:
            news_id = int(query_params["news_id"][0])
            render_full_news(news_list[news_id])
            if st.button("Go Back"):
                del st.query_params['news_id']
        except (ValueError, IndexError):
            st.error("Invalid news ID!")
    else:
        render_news_cards(news_list)

if __name__ == "__main__":
    main()
