"""
Streamlit web application for the Copyright Detection System.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

from main import CopyrightDetectionSystem


# Page configuration
st.set_page_config(
    page_title="AI Copyright Detection System",
    page_icon="©️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A5F;
        text-align: center;
        padding: 1rem 0;
    }
    .risk-high {
        background-color: #FFCDD2;
        border-left: 4px solid #F44336;
        padding: 1rem;
        border-radius: 4px;
    }
    .risk-medium {
        background-color: #FFE0B2;
        border-left: 4px solid #FF9800;
        padding: 1rem;
        border-radius: 4px;
    }
    .risk-low {
        background-color: #FFF9C4;
        border-left: 4px solid #FFEB3B;
        padding: 1rem;
        border-radius: 4px;
    }
    .risk-none {
        background-color: #C8E6C9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 4px;
    }
    .metric-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_system():
    """Load and cache the detection system."""
    system = CopyrightDetectionSystem()
    system.initialize()
    return system


def get_risk_color(risk_level: str) -> str:
    """Get color for risk level."""
    colors = {
        "HIGH": "#F44336",
        "MEDIUM": "#FF9800",
        "LOW": "#FFEB3B",
        "NONE": "#4CAF50"
    }
    return colors.get(risk_level, "#9E9E9E")


def create_similarity_gauge(similarity: float):
    """Create a gauge chart for similarity score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=similarity * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Similarity Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 55], 'color': "#C8E6C9"},
                {'range': [55, 70], 'color': "#FFF9C4"},
                {'range': [70, 85], 'color': "#FFE0B2"},
                {'range': [85, 100], 'color': "#FFCDD2"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_matches_chart(matches: list):
    """Create a bar chart of matched content."""
    if not matches:
        return None
    
    df = pd.DataFrame([{
        'Title': m['title'][:30] + '...' if len(m['title']) > 30 else m['title'],
        'Similarity': m['similarity_score'] * 100,
        'Type': m['content_type']
    } for m in matches])
    
    fig = px.bar(
        df, 
        x='Similarity', 
        y='Title', 
        orientation='h',
        color='Type',
        title='Matched Content Similarity',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        height=300,
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Similarity (%)',
        yaxis_title=''
    )
    return fig


def main():
    # Header
    st.markdown('<h1 class="main-header">©️ AI Copyright Detection System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load system
    with st.spinner("Loading detection system..."):
        system = load_system()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        top_k = st.slider("Maximum matches to return", 1, 10, 5)
        
        use_purpose = st.selectbox(
            "Intended use purpose",
            ["general", "education", "research", "criticism", "parody", "news", "commercial"]
        )
        
        citation_style = st.selectbox(
            "Citation style",
            ["APA", "MLA", "Chicago", "Harvard"]
        )
        
        st.markdown("---")
        
        st.header("📊 System Status")
        stats = system.vector_store.get_stats()
        st.metric("Indexed Works", stats["total_vectors"])
        st.metric("Embedding Dimension", stats["dimension"])
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This system helps detect potential copyright 
        issues in AI-generated content by comparing 
        against a database of protected works.
        """)
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🔍 Detection", "📋 Batch Check", "📚 Database"])
    
    with tab1:
        st.header("Content Analysis")
        
        # Text input
        text_input = st.text_area(
            "Enter text to analyze",
            height=200,
            placeholder="Paste AI-generated content here to check for potential copyright issues..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        with col2:
            quick_check = st.button("⚡ Quick Check", use_container_width=True)
        
        if analyze_button and text_input:
            with st.spinner("Analyzing content..."):
                report = system.analyze(
                    text=text_input,
                    top_k=top_k,
                    use_purpose=use_purpose,
                    citation_style=citation_style
                )
            
            # Results
            st.markdown("---")
            st.header("Analysis Results")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                risk_level = report.detection_summary["risk_level"]
                color = get_risk_color(risk_level)
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {color};">Risk Level</h3>
                    <h2 style="color: {color};">{risk_level}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Matches Found</h3>
                    <h2>{report.detection_summary['matches_found']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Compliance Status</h3>
                    <h2>{report.compliance_assessment['status']}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                license_text = "Yes" if report.compliance_assessment['requires_license'] else "No"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>License Required</h3>
                    <h2>{license_text}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_similarity_gauge(report.detection_summary["highest_similarity"]),
                    use_container_width=True
                )
            
            with col2:
                if report.attributions:
                    chart = create_matches_chart(report.attributions)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
            
            # Detailed results
            if report.attributions:
                st.subheader("📖 Matched Works")
                for i, attr in enumerate(report.attributions, 1):
                    with st.expander(f"{i}. {attr['title']} - {attr['similarity_score']:.1%} match"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Author:** {attr['author']}")
                            st.write(f"**Type:** {attr['content_type']}")
                            st.write(f"**Published:** {attr['publication_date']}")
                        with col2:
                            st.write(f"**Publisher:** {attr['publisher']}")
                            st.write(f"**Confidence:** {attr['confidence']}")
                        st.write(f"**Citation:** {attr['citation']}")
            
            # Recommendations
            st.subheader("💡 Recommendations")
            
            risk_class = f"risk-{risk_level.lower()}"
            st.markdown(f"""
            <div class="{risk_class}">
                <strong>Overall Recommendation:</strong><br>
                {report.overall_recommendation}
            </div>
            """, unsafe_allow_html=True)
            
            if report.compliance_assessment['recommendations']:
                st.write("**Specific Actions:**")
                for rec in report.compliance_assessment['recommendations']:
                    icon = "🔴" if rec['priority'] == "HIGH" else "🟡" if rec['priority'] == "MEDIUM" else "🟢"
                    st.write(f"{icon} **{rec['category']}:** {rec['action']}")
            
            if report.compliance_assessment['suggested_modifications']:
                st.write("**Suggested Modifications:**")
                for mod in report.compliance_assessment['suggested_modifications']:
                    st.write(f"• {mod}")
            
            # Download report
            st.markdown("---")
            report_text = system.report_generator.format_report_text(report)
            st.download_button(
                label="📥 Download Full Report",
                data=report_text,
                file_name=f"copyright_report_{report.report_id}.txt",
                mime="text/plain"
            )
        
        elif quick_check and text_input:
            with st.spinner("Checking..."):
                has_issues, risk_level, similarity = system.detector.quick_check(text_input)
            
            if has_issues:
                st.error(f"⚠️ Potential issues detected! Risk: {risk_level}, Similarity: {similarity:.1%}")
            else:
                st.success(f"✅ No significant issues detected. Similarity: {similarity:.1%}")
    
    with tab2:
        st.header("Batch Content Check")
        st.write("Check multiple pieces of content at once.")
        
        batch_input = st.text_area(
            "Enter multiple texts (one per line)",
            height=300,
            placeholder="Enter each piece of content on a new line..."
        )
        
        if st.button("🔍 Check All", type="primary"):
            texts = [t.strip() for t in batch_input.split("\n") if t.strip()]
            
            if texts:
                results = []
                progress = st.progress(0)
                
                for i, text in enumerate(texts):
                    has_issues, risk_level, similarity = system.detector.quick_check(text)
                    results.append({
                        "Text": text[:50] + "..." if len(text) > 50 else text,
                        "Has Issues": "⚠️ Yes" if has_issues else "✅ No",
                        "Risk Level": risk_level,
                        "Similarity": f"{similarity:.1%}"
                    })
                    progress.progress((i + 1) / len(texts))
                
                st.dataframe(pd.DataFrame(results), use_container_width=True)
                
                issues_count = sum(1 for r in results if "Yes" in r["Has Issues"])
                st.metric("Texts with Issues", f"{issues_count} / {len(texts)}")
    
    with tab3:
        st.header("Copyright Database")
        st.write("View the indexed copyrighted works in the system.")
        
        # Get metadata from vector store
        metadata = system.vector_store.metadata
        
        if metadata:
            df = pd.DataFrame(metadata)
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                type_filter = st.multiselect(
                    "Filter by type",
                    options=df["content_type"].unique().tolist(),
                    default=[]
                )
            with col2:
                search_term = st.text_input("Search by title")
            
            filtered_df = df.copy()
            if type_filter:
                filtered_df = filtered_df[filtered_df["content_type"].isin(type_filter)]
            if search_term:
                filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False)]
            
            # Display
            st.dataframe(
                filtered_df[["title", "author_name", "content_type", "publisher", "publication_date"]],
                use_container_width=True
            )
            
            # Stats
            st.subheader("Database Statistics")
            col1, col2 = st.columns(2)
            
            with col1:
                type_counts = df["content_type"].value_counts()
                fig = px.pie(values=type_counts.values, names=type_counts.index, title="Content by Type")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                author_counts = df["author_name"].value_counts().head(10)
                fig = px.bar(x=author_counts.values, y=author_counts.index, orientation='h', title="Top Authors")
                st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
