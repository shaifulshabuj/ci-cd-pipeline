import streamlit as st
import requests
import json
from datetime import datetime

# API_URL set to the backend service - adjust this if needed
API_URL = "http://localhost:3001/api"  # Assuming your API is running on port 3001

st.set_page_config(
    page_title="Point Management Tool",
    page_icon="🏆",
    layout="wide"
)

# Apply some custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2196F3;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Point Management System</h1>", unsafe_allow_html=True)

def fetch_users():
    """Fetch all users from the API"""
    try:
        response = requests.get(f"{API_URL}/users")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching users: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return []

def create_user(name):
    """Create a new user"""
    try:
        response = requests.post(f"{API_URL}/users", json={"name": name})
        if response.status_code == 201:
            st.success(f"User {name} created successfully!")
            return response.json()
        else:
            st.error(f"Error creating user: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return None

def update_points(user_id, points, operation="set"):
    """Update or add points to a user"""
    try:
        if operation == "add":
            response = requests.post(f"{API_URL}/users/{user_id}/points", json={"points": points})
        else:
            response = requests.patch(f"{API_URL}/users/{user_id}/points", json={"points": points})
        
        if response.status_code == 200:
            st.success(f"Points updated successfully!")
            return response.json()
        else:
            st.error(f"Error updating points: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return None

def delete_user(user_id):
    """Delete a user"""
    try:
        response = requests.delete(f"{API_URL}/users/{user_id}")
        
        if response.status_code == 204:
            st.success("User deleted successfully!")
            return True
        else:
            st.error(f"Error deleting user: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return False

# Create sidebar for application navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Users Dashboard", "Add User", "Manage Points", "API Status"])

# Users Dashboard
if page == "Users Dashboard":
    st.markdown("<h2 class='subheader'>Users Dashboard</h2>", unsafe_allow_html=True)
    
    # Add a refresh button
    if st.button("Refresh Users"):
        st.rerun()
    
    users = fetch_users()
    
    if not users:
        st.info("No users found. Add some users to get started!")
    else:
        # Sort users by points (highest first)
        users.sort(key=lambda x: x.get('points', 0), reverse=True)
        
        # Display top users
        st.markdown("<h3>Top Users</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        
        for i, user in enumerate(users[:3]):
            with cols[i]:
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                st.markdown(f"""
                <div class='card'>
                    <h4>{medal} {user.get('name', 'Unknown User')}</h4>
                    <p><b>Points:</b> {user.get('points', 0)}</p>
                    <p><small>ID: {user.get('id', 'N/A')[:8]}...</small></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Display all users in a table
        st.markdown("<h3>All Users</h3>", unsafe_allow_html=True)
        
        user_data = []
        for user in users:
            created_at = user.get('createdAt', '')
            try:
                if created_at:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                else:
                    created_date = 'N/A'
            except:
                created_date = 'N/A'
                
            user_data.append({
                "ID": user.get('id', 'N/A')[:8] + '...',
                "Name": user.get('name', 'Unknown'),
                "Points": user.get('points', 0),
                "Created": created_date,
            })
        
        st.table(user_data)

# Add User Page
elif page == "Add User":
    st.markdown("<h2 class='subheader'>Add New User</h2>", unsafe_allow_html=True)
    
    with st.form("add_user_form"):
        name = st.text_input("User Name")
        submitted = st.form_submit_button("Create User")
        
        if submitted and name:
            new_user = create_user(name)
            if new_user:
                st.json(new_user)
        elif submitted:
            st.warning("Please enter a name for the user")

# Manage Points Page
elif page == "Manage Points":
    st.markdown("<h2 class='subheader'>Manage Points</h2>", unsafe_allow_html=True)
    
    users = fetch_users()
    
    if not users:
        st.info("No users found. Add some users first!")
    else:
        # Create a dictionary of user names mapped to IDs for selection
        user_options = {user.get('name', f"Unknown ({user.get('id')[:8]})"): user.get('id') for user in users}
        
        selected_user_name = st.selectbox("Select User", list(user_options.keys()))
        selected_user_id = user_options.get(selected_user_name)
        
        # Find the selected user's current points
        selected_user = next((user for user in users if user.get('id') == selected_user_id), None)
        current_points = selected_user.get('points', 0) if selected_user else 0
        
        st.info(f"Current points: {current_points}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>Set Points</h3>", unsafe_allow_html=True)
            with st.form("set_points_form"):
                new_points = st.number_input("New Points Value", min_value=0, value=current_points)
                set_submitted = st.form_submit_button("Set Points")
                
                if set_submitted:
                    updated_user = update_points(selected_user_id, new_points, "set")
                    if updated_user:
                        st.success(f"Points for {selected_user_name} set to {new_points}")
                        st.json(updated_user)
        
        with col2:
            st.markdown("<h3>Add Points</h3>", unsafe_allow_html=True)
            with st.form("add_points_form"):
                add_points = st.number_input("Points to Add", min_value=0, value=0)
                add_submitted = st.form_submit_button("Add Points")
                
                if add_submitted and add_points > 0:
                    updated_user = update_points(selected_user_id, add_points, "add")
                    if updated_user:
                        st.success(f"Added {add_points} points to {selected_user_name}")
                        st.json(updated_user)
                elif add_submitted:
                    st.warning("Please enter a positive number of points to add")
        
        # Delete user section
        st.markdown("<h3>Delete User</h3>", unsafe_allow_html=True)
        if st.button(f"Delete {selected_user_name}", key="delete_user"):
            confirmation = st.checkbox("Confirm deletion - this cannot be undone!")
            if confirmation:
                if delete_user(selected_user_id):
                    st.success(f"{selected_user_name} has been deleted")
                    st.rerun()

# API Status Page
elif page == "API Status":
    st.markdown("<h2 class='subheader'>API Status</h2>", unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_URL.split('/api')[0]}")
        
        if response.status_code == 200:
            status_data = response.json()
            st.markdown("""
            <div class='card' style='background-color: #e7f3e8;'>
                <h3>✅ API is Online</h3>
                <p><b>Status:</b> {status}</p>
                <p><b>Version:</b> {version}</p>
                <p><b>Message:</b> {message}</p>
            </div>
            """.format(
                status=status_data.get('status', 'Unknown'),
                version=status_data.get('version', 'Unknown'),
                message=status_data.get('message', 'No message')
            ), unsafe_allow_html=True)
            
            # Also check the health endpoint
            try:
                health_response = requests.get(f"{API_URL.split('/api')[0]}/health")
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    st.markdown(f"""
                    <div class='card' style='background-color: #e7f3e8;'>
                        <h3>Health Check</h3>
                        <p><b>Status:</b> {health_data.get('status', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                st.warning("Health check endpoint not accessible")
            
            # Provide the current API URL for reference
            st.markdown(f"**Current API URL:** `{API_URL}`")
        else:
            st.markdown("""
            <div class='card' style='background-color: #f3e7e8;'>
                <h3>⚠️ API Error</h3>
                <p>Status Code: {status}</p>
                <p>Response: {response}</p>
            </div>
            """.format(
                status=response.status_code,
                response=response.text
            ), unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class='card' style='background-color: #f3e7e8;'>
            <h3>❌ API Offline</h3>
            <p>The API doesn't appear to be running at <code>{API_URL}</code></p>
            <p>Error: {str(e)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### Troubleshooting
        
        1. Make sure the API server is running
        2. Check the API URL in this application
        3. Verify network connectivity
        """)

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center;'>
    <small>Point Management Tool © 2025 | SRE Personal Project</small>
</p>
""", unsafe_allow_html=True)