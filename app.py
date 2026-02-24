import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(
    page_title="myNalanda AI Analytics",
    layout="wide"
)



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */

.stApp{
background: linear-gradient(135deg,#0f051d,#1a0b2e,#0f051d);
color:white;
}


/* SIDEBAR */

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#140824,#0f051d);
border-right:1px solid #a855f7;
}


/* KPI CARD */

.kpi-card{

background: linear-gradient(145deg,#1a0b2e,#140824);

padding:20px;

border-radius:15px;

border:1px solid #9333ea;

box-shadow:0 0 15px rgba(168,85,247,0.3);

}


/* LOGIN BOX */

.login-box{

    width:400px;
    height:90px;

    border:2px solid #a855f7;
    border-radius:20px;

    margin:auto;
    margin-top:20px;
    margin-bottom:20px;

    display:flex;
    justify-content:center;
    align-items:center;

    box-shadow:0 0 25px rgba(168,85,247,0.7);
}

.login-title{

    color:#c084fc;
    font-size:40px;
    font-weight:bold;
    margin:0;

}


/* BUTTON */

.stButton>button{

background: linear-gradient(90deg,#9333ea,#c084fc);

color:white;

border:none;

border-radius:10px;

height:45px;

}


/* TEACHER CARD */

.teacher-card{

background: rgba(255,255,255,0.03);

padding:25px;

border-radius:15px;

border:1px solid #9333ea;

}

</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():

    return pd.read_csv("Teacher_Dataset.csv")

df = load_data()




if "auth" not in st.session_state:

    st.session_state.auth=False


def login():

    col1,col2,col3=st.columns([1,1.5,1])

    with col2:

        st.markdown("""
	<div class='login-box'>
    		<h1 class='login-title'>myNalanda</h1>
	</div>
	""", unsafe_allow_html=True)

        user=st.text_input("Username")

        pwd=st.text_input("Password",type="password")

        if st.button("Login"):

            if user=="user" and pwd=="1234":

                st.session_state.auth=True

                st.rerun()

        st.markdown("</div>",unsafe_allow_html=True)




def sidebar():

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(

        "",

        [

            "Dashboard",

            "Teacher Analytics",

            "Late Count & Attrition"

        ]

    )

    if st.sidebar.button("Logout"):

        st.session_state.auth=False

        st.rerun()

    return page




def kpi(title,value):

    st.markdown(f"""

    <div class="kpi-card">

    <h4>{title}</h4>

    <h2 style="color:#c084fc">{value}</h2>

    </div>

    """,unsafe_allow_html=True)




def dashboard():

    st.title("Dashboard")


    c1,c2,c3,c4=st.columns(4)

    with c1:
        kpi("Teachers",df["Teacher"].nunique())

    with c2:
        kpi("Avg Score",round(df["Score"].mean(),2))

    with c3:
        kpi("Avg Attendance",round(df["Attendance"].mean(),2))

    with c4:
        kpi("Total Late",df["LateCount"].sum())


    st.divider()


    fig=px.bar(

    df,

    x="Teacher",

    y="Score",

    color="Section"

    )

    st.plotly_chart(fig,use_container_width=True)



def teacher():

    st.title("Teacher Analytics")




    teacher_list = df["Teacher"].unique()

    name=st.selectbox("Select Teacher",teacher_list)


 

    teacher_df=df[df["Teacher"]==name]


  

    student_list = teacher_df["Student"].unique()

    student=st.selectbox("Select Student",student_list)


 

    t=teacher_df[teacher_df["Student"]==student].iloc[0]


    col1,col2=st.columns([2,1])


    with col1:

        st.markdown(f"""

        <div class="teacher-card">

        <h2>{name}</h2>

        <p>Section : {t['Section']}</p>

        <p>Student : {t['Student']}</p>

        <p>Score : {t['Score']}</p>

        <p>Attendance : {t['Attendance']}</p>

        <p>Late Count : {t['LateCount']}</p>

        <p>Attrition : {t['Attrition']}</p>

        <p>Remarks : {t['Remarks']}</p>

        </div>

        """,unsafe_allow_html=True)


    with col2:

        fig=go.Figure(go.Indicator(

        mode="gauge+number",

        value=t["Score"],

        gauge={'axis':{'range':[0,10]}}

        ))

        st.plotly_chart(fig,use_container_width=True)

def late_attrition():

    st.title("Late Count & Attrition Insights")

    st.divider()

    col1, col2 = st.columns([1.2, 1])


    with col1:

        st.subheader("Late Attendance Analysis")

        late_fig = px.bar(

            df,
            x="Teacher",
            y="LateCount",
            color="Section",
            title="Late Count by Teacher",

            color_discrete_map={
                "A": "#c084fc",
                "B": "#9333ea",
                "C": "#6b21a8"
            },

            height=500

        )

        late_fig.update_layout(

            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",

            margin=dict(l=20, r=20, t=50, b=20)

        )

        st.plotly_chart(late_fig, use_container_width=True)



    with col2:

        st.subheader("Attrition Trends")

        attrition_count = df["Attrition"].value_counts().reset_index()

        attrition_count.columns = ["Attrition", "Count"]


        attr_fig = px.pie(

            attrition_count,
            names="Attrition",
            values="Count",

            hole=0.6,

            color_discrete_sequence=["#9333ea", "#c084fc"]

        )

        attr_fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"

        )

        st.plotly_chart(attr_fig, use_container_width=True)


    st.divider()




    st.subheader("Comparative Performance Insight")


    comp_fig = px.scatter(

        df,

        x="Attendance",

        y="Score",

        color="Attrition",

        size="LateCount",

        hover_data=["Teacher","Student"],

        color_discrete_sequence=["#22c55e","#ef4444"]

    )


    comp_fig.update_layout(

        plot_bgcolor="rgba(0,0,0,0)",

        paper_bgcolor="rgba(0,0,0,0)",

        font_color="white"

    )


    st.plotly_chart(comp_fig, use_container_width=True)


    st.divider()


    st.subheader("Detailed Data")

    st.dataframe(df, use_container_width=True)


if not st.session_state.auth:

    login()

else:

    page=sidebar()

    if page=="Dashboard":

    	dashboard()

    elif page=="Teacher Analytics":

    	teacher()

    elif page=="Late Count & Attrition":

        late_attrition()