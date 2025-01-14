import streamlit as st
import google.generativeai as genai

# Gemini Model Wrapper
class GeminiModel:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def get_recommendations(self, language, age_group, genre):
        # Create a prompt for the Gemini model
        prompt = (f"Recommend books in {language} for age group {age_group} in the genre {', '.join(genre)}. "
                  f"Provide the book title, a brief context and summary, and a purchase link for each book. "
                  f"Format the response as follows:\n\n"
                  f"Book Title: <title>\nContext and Summary: <context and summary>\nPurchase Link: <purchase link>\n\n")

        # Initialize the Gemini model
        model = genai.GenerativeModel(self.model_name)

        # Make an API call to the Gemini model
        response = model.generate_content(prompt)

        # Parse the response to get book recommendations
        recommendations = self.parse_response(response.text)
        return recommendations

    def parse_response(self, response_text):
        # Parse the response text from the Gemini model
        recommendations = []
        book_sections = response_text.strip().split('\n\n')
        for section in book_sections:
            lines = section.split('\n')
            if len(lines) >= 3:
                book = {
                    "Book Title": lines[0].replace("Book Title: ", ""),
                    "Context and Summary": lines[1].replace("Context and Summary: ", ""),
                    "Purchase Link": lines[2].replace("Purchase Link: ", "")
                }
                recommendations.append(book)
        return recommendations

# Streamlit UI
def main():
    st.title("Personalized AI Book Recommendation")

    # Sidebar for user inputs
    st.sidebar.header("User Inputs")

    language = st.sidebar.selectbox("Select Language", ["English", "Tamil", "Hindi", "Malayalam", "French"])
    age_group = st.sidebar.selectbox("Select Age Group", ["1 to 10", "10 to 20", "20 to 30", "30 to 40", "40 to 50", "50 to 60"])
    genre = st.sidebar.multiselect("Select Genre", ["Education", "Tech", "Horror", "Thriller", "Philosophy", "Comic", "Spiritual"])

    if st.sidebar.button("Get Recommendations"):
        # Initialize the Gemini model
        model_name = "gemini-1.5-flash"
        api_key = "Replace with your actual API key"  
        gemini_model = GeminiModel(model_name, api_key)

        # Get recommendations
        recommendations = gemini_model.get_recommendations(language, age_group, genre)

        # Display recommendations
        st.header("Book Recommendations")
        for book in recommendations:
            st.subheader(book["Book Title"])
            st.write(book["Context and Summary"])
            st.markdown(f"[Purchase Link]({book['Purchase Link']})")
            st.write("---")  # Add a separator between books

    # Custom styling
    st.markdown(
        """
        <style>
        .main .block-container{{
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }}
        .sidebar .sidebar-content {{
            background-color: #f0f0f0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()