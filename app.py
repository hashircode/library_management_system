import streamlit as st

st.set_page_config(page_title="Library Management System", layout="wide")

if "books" not in st.session_state:
    st.session_state.books = []

menu = ["Home", "Add Book", "View Books", "Search Books", "Update Book", "Delete Book"]
choice = st.sidebar.radio("📌 Navigation", menu)

st.title("📚 Library Management System")

def display_books(books):
   
    if books:
        st.markdown("---")
        for book in books:
            col_id, col_title, col_author, col_year, col_status = st.columns([1, 3, 2, 1, 1.5])
            
            with col_id:
                st.markdown(f"**ID:** `{book['id']}`")
            with col_title:
                st.markdown(f"**Title:** **{book['title']}**")
            with col_author:
                st.markdown(f"**Author:** {book['author']}")
            with col_year:
                st.markdown(f"**Year:** {book['year']}")
            with col_status:
                if book['status'] == "Available":
                    st.success(f"🟢 {book['status']}")
                else:
                    st.warning(f"🟠 {book['status']}")
            st.divider()
    else:
        st.info("No books available yet.")

if choice == "Home":
    st.header("Welcome to Your Digital Library! 📚")

    st.markdown("""
    Managing your book collection has never been easier. This **Library Management System**
    is designed for simplicity and efficiency, helping you keep track of all your books
    and their current status.
    """)

    st.divider()
    
    st.subheader("🚀 Quick Actions")
    
    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.info("""
        ### Add a Book
        Quickly expand your library! Use the **Add Book** option to input new titles,
        authors, and publication details.
        
        *Hint: Make sure the Book ID is unique!*
        """)
        
    with action_col2:
        st.success("""
        ### View & Search
        Need to find a specific book? Go to **View Books** for the full list, or use
        **Search Books** for instant results by title or author.
        
        *Keep your collection organized!*
        """)
    
    st.markdown("---")
    st.caption("Use the **📌 Navigation** menu on the sidebar to access all management tools.")

elif choice == "Add Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_form", clear_on_submit=True):
        col_id, col_title = st.columns(2)
        with col_id:
            book_id = st.text_input("Book ID (e.g., 101, ISBN-123)")
        with col_title:
            title = st.text_input("Book Title")
            
        col_author, col_year, col_status = st.columns(3)
        with col_author:
            author = st.text_input("Author")
        with col_year:
            year = st.number_input("Published Year", min_value=1000, max_value=2100, step=1, value=2024)
        with col_status:
            status = st.selectbox("Status", ["Available", "Issued"])
        
        is_id_unique = book_id not in [b['id'] for b in st.session_state.books]

        submitted = st.form_submit_button("Add Book")

        if submitted:
            if book_id and title and author:
                if is_id_unique:
                    st.session_state.books.append({
                        "id": book_id,
                        "title": title,
                        "author": author,
                        "year": int(year),
                        "status": status
                    })
                    st.success(f"✅ Book '{title}' added successfully!")
                else:
                    st.error(f"⚠ Book ID '{book_id}' already exists. Please use a unique ID.")
            else:
                st.error("⚠ Please fill all required fields (ID, Title, Author)!")

elif choice == "View Books":
    st.subheader("📖 All Books")
    display_books(st.session_state.books)

elif choice == "Search Books":
    st.subheader("🔍 Search Books")
    keyword = st.text_input("Enter title or author to search").strip()
    
    if keyword:
        results = [
            b for b in st.session_state.books 
            if keyword.lower() in b["title"].lower() or keyword.lower() in b["author"].lower()
        ]
        
        st.info(f"Showing {len(results)} result(s) for keyword: **{keyword}**")
        display_books(results)
    else:
        st.info("Start typing a title or author name to find books.")

elif choice == "Update Book":
    st.subheader("✏ Update Book")
    if st.session_state.books:
        ids = [b["id"] for b in st.session_state.books]
        selected_id = st.selectbox("Select Book ID to Update", ids)
        
        book = next(b for b in st.session_state.books if b["id"] == selected_id)

        with st.form("update_form"):
            new_title = st.text_input("Book Title", value=book["title"])
            new_author = st.text_input("Author", value=book["author"])
            new_year = st.number_input("Published Year", min_value=1000, max_value=2100, step=1, value=book["year"])
            
            current_status_index = 0 if book["status"] == "Available" else 1
            new_status = st.selectbox("Status", ["Available", "Issued"], index=current_status_index)
            
            updated = st.form_submit_button("Update Book Details")

            if updated:
                book.update({
                    "title": new_title,
                    "author": new_author,
                    "year": int(new_year),
                    "status": new_status
                })
                st.success(f"✅ Book ID **{selected_id}** updated successfully!")
    else:
        st.warning("No books to update! Please add a book first.")

elif choice == "Delete Book":
    st.subheader("🗑 Delete Book")
    if st.session_state.books:
        ids = [b["id"] for b in st.session_state.books]
        
        col_select, col_button = st.columns([3, 1])
        with col_select:
            selected_id = st.selectbox("Select Book ID to Delete", ids)
        
        st.divider()
        st.error(f"⚠️ **Warning:** You are about to delete book with ID: **{selected_id}**")
        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Confirm Delete", type="primary"):
                st.session_state.books = [b for b in st.session_state.books if b["id"] != selected_id]
                st.success(f"✅ Book with ID **{selected_id}** has been permanently deleted!")
                st.rerun() 
    else:
        st.warning("No books to delete!")