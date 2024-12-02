import streamlit as st
import requests
import pandas as pd

def fetch_products():
    response = requests.get('https://fakestoreapi.com/products')
    return response.json()

def fetch_categories():
    response = requests.get('https://fakestoreapi.com/products/categories')
    return response.json()

def filter_products_by_category(products, category):
    return [product for product in products if product['category'] == category]

def filter_products_by_search(products, search_term):
    return [product for product in products if search_term.lower() in product['title'].lower()]

def main():
    st.set_page_config(page_title="Review Genius", layout="wide")

    st.markdown("""
        <style>
        /* Theme and Base */
        [data-testid="stAppViewContainer"], .stApp { background-color: #1E1E1E; }
        * { color: #0d8eda !important; }
        
        /* Layout Components */
        .main-title { text-align: center; padding: 20px; font-size: 3em; }
        .product-card {
            background-color: #2D2D2D;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 20px;
        }
        .search-container { 
            background-color: #2D2D2D; 
            padding: 20px; 
            border-radius: 10px; 
        }
        
        /* Product Elements */
        .product-image { width: 100%; height: 200px; object-fit: contain; }
        .rating-badge {
            background-color: #0d8eda;
            padding: 5px 10px;
            border-radius: 15px;
            color: #fff !important;
        }
        
        /* UI Components */
        .css-1d391kg { background-color: #2D2D2D !important; }
        .stTextInput > div > div, .stSelectbox > div > div { background-color: #2D2D2D; }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 class='main-title'>Review Genius</h1>", unsafe_allow_html=True)

    # Get data
    products = fetch_products()
    categories = fetch_categories()

    # Search bar
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    search_term = st.text_input("🔍 Search products", "")
    st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("<div class='sidebar-title'>Filters</div>", unsafe_allow_html=True)
    selected_category = st.sidebar.selectbox("Select a category", ["All"] + categories)
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
    price_range = st.sidebar.slider("Price Range ($)", 0, 1000, (0, 1000))
    sort_option = st.sidebar.selectbox(
        "Sort By",
        ["Price: Low to High", "Price: High to Low", "Rating: High to Low"]
    )

    # Filter products
    if selected_category != "All":
        filtered_products = filter_products_by_category(products, selected_category)
    else:
        filtered_products = products

    if search_term:
        filtered_products = filter_products_by_search(filtered_products, search_term)

    filtered_products = [p for p in filtered_products if p["rating"]["rate"] >= min_rating]
    filtered_products = [p for p in filtered_products if price_range[0] <= p["price"] <= price_range[1]]

    # Sort products
    if sort_option == "Price: Low to High":
        filtered_products = sorted(filtered_products, key=lambda x: x["price"])
    elif sort_option == "Price: High to Low":
        filtered_products = sorted(filtered_products, key=lambda x: x["price"], reverse=True)
    elif sort_option == "Rating: High to Low":
        filtered_products = sorted(filtered_products, key=lambda x: x["rating"]["rate"], reverse=True)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Products", len(filtered_products))
    with col2:
        st.metric("Categories", len(categories))
    with col3:
        if filtered_products:
            avg_price = sum(p["price"] for p in filtered_products) / len(filtered_products)
            st.metric("Average Price", f"${avg_price:.2f}")

    # Display products
    if not filtered_products:
        st.info("No products found matching your search criteria.")
    else:
        cols = st.columns(3)
        for idx, product in enumerate(filtered_products):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class='product-card'>
                        <img src='{product["image"]}' class='product-image'>
                        <h3 class='product-text'>{product["title"]}</h3>
                        <p class='product-text'>{product["description"][:100]}...</p>
                        <p class='product-text'>${product["price"]}</p>
                        <div class='rating-badge'>
                            ⭐ {product["rating"]["rate"]}/5 ({product["rating"]["count"]} reviews)
                        </div>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
