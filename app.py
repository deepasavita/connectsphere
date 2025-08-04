import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_for_testing")

# In-memory data storage
users = {}
posts = []
user_counter = 1
post_counter = 1

# Admin configuration
ADMIN_EMAIL = "admin@procommunity.com"
ADMIN_PASSWORD = "admin123"  # In production, use environment variable

# Sample Indian users data
sample_users = [
    {
        'name': 'Arjun Sharma',
        'email': 'arjun.sharma@email.com',
        'bio': 'Software Engineer passionate about building scalable web applications. Love coding in Python and JavaScript.',
        'password': 'password123'
    },
    {
        'name': 'Priya Patel',
        'email': 'priya.patel@email.com',
        'bio': 'Full Stack Developer with 3+ years experience. Interested in AI/ML and cloud technologies.',
        'password': 'password123'
    },
    {
        'name': 'Rahul Gupta',
        'email': 'rahul.gupta@email.com',
        'bio': 'Data Scientist working on machine learning projects. Python enthusiast and tech blogger.',
        'password': 'password123'
    },
    {
        'name': 'Sneha Reddy',
        'email': 'sneha.reddy@email.com',
        'bio': 'UI/UX Designer and Frontend Developer. Creating beautiful and intuitive user experiences.',
        'password': 'password123'
    }
]

# Initialize sample data
def init_sample_data():
    global user_counter, post_counter
    
    # Create admin user first
    admin_id = user_counter
    users[admin_id] = {
        'id': admin_id,
        'name': 'Admin User',
        'email': ADMIN_EMAIL,
        'bio': 'Platform Administrator - Managing the ProCommunity platform',
        'password_hash': generate_password_hash(ADMIN_PASSWORD),
        'is_admin': True
    }
    user_counter += 1
    
    # Create sample users
    for user_data in sample_users:
        user_id = user_counter
        users[user_id] = {
            'id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'bio': user_data['bio'],
            'password_hash': generate_password_hash(user_data['password']),
            'is_admin': False
        }
        user_counter += 1
    
    # Create sample posts
    sample_posts = [
        {
            'user_id': 1,
            'content': 'Excited to share that I just completed a new web application using Flask and JavaScript! The journey of learning new technologies never stops. 🚀'
        },
        {
            'user_id': 2,
            'content': 'Just finished reading an amazing article about the future of AI in software development. The possibilities are endless!'
        },
        {
            'user_id': 3,
            'content': 'Working on a machine learning model that can predict user behavior. Data science is truly fascinating! 📊'
        },
        {
            'user_id': 4,
            'content': 'Designed a new user interface for a mobile app today. Clean, minimal, and user-friendly. Design matters! ✨'
        },
        {
            'user_id': 1,
            'content': 'Attending a tech conference next week. Looking forward to networking with fellow developers and learning about new technologies.'
        }
    ]
    
    for post_data in sample_posts:
        post_id = post_counter
        posts.append({
            'id': post_id,
            'user_id': post_data['user_id'],
            'content': post_data['content'],
            'timestamp': datetime.now(),
            'author_name': users[post_data['user_id']]['name']
        })
        post_counter += 1

# Initialize sample data on startup
init_sample_data()

@app.route('/')
def index():
    """Home page showing all posts"""
    # Sort posts by timestamp (newest first)
    sorted_posts = sorted(posts, key=lambda x: x['timestamp'], reverse=True)
    return render_template('index.html', posts=sorted_posts, current_user_id=session.get('user_id'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Find user by email
        user = None
        for u in users.values():
            if u['email'] == email:
                user = u
                break
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['is_admin'] = user.get('is_admin', False)
            flash('Login successful!', 'success')
            
            # Redirect admin users to admin dashboard
            if user.get('is_admin'):
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        bio = request.form['bio']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        # Check if email already exists
        for u in users.values():
            if u['email'] == email:
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('register.html')
        
        # Create new user
        global user_counter
        user_id = user_counter
        users[user_id] = {
            'id': user_id,
            'name': name,
            'email': email,
            'bio': bio,
            'password_hash': generate_password_hash(password),
            'is_admin': False
        }
        user_counter += 1
        
        # Auto-login after registration
        session['user_id'] = user_id
        session['user_name'] = name
        session['is_admin'] = False
        flash('Registration successful! Welcome to the community!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    """Create a new post"""
    if 'user_id' not in session:
        flash('Please login to create a post.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        content = request.form['content']
        
        if not content.strip():
            flash('Post content cannot be empty.', 'error')
            return render_template('create_post.html')
        
        # Create new post
        global post_counter
        post_id = post_counter
        posts.append({
            'id': post_id,
            'user_id': session['user_id'],
            'content': content,
            'timestamp': datetime.now(),
            'author_name': session['user_name']
        })
        post_counter += 1
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_post.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    """View user profile and their posts"""
    if user_id not in users:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    user = users[user_id]
    
    # Get user's posts
    user_posts = [post for post in posts if post['user_id'] == user_id]
    user_posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    is_own_profile = session.get('user_id') == user_id
    
    return render_template('profile.html', user=user, posts=user_posts, 
                         is_own_profile=is_own_profile, current_user_id=session.get('user_id'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """Edit user profile"""
    if 'user_id' not in session:
        flash('Please login to edit your profile.', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = users[user_id]
    
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']
        
        if not name.strip():
            flash('Name cannot be empty.', 'error')
            return render_template('profile.html', user=user, posts=[], 
                                 is_own_profile=True, edit_mode=True)
        
        # Update user info
        users[user_id]['name'] = name
        users[user_id]['bio'] = bio
        session['user_name'] = name
        
        # Update author name in existing posts
        for post in posts:
            if post['user_id'] == user_id:
                post['author_name'] = name
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile', user_id=user_id))
    
    # GET request - show edit form
    user_posts = [post for post in posts if post['user_id'] == user_id]
    user_posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('profile.html', user=user, posts=user_posts, 
                         is_own_profile=True, edit_mode=True, current_user_id=user_id)

# Admin helper function
def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        
        if not session.get('is_admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with platform statistics"""
    total_users = len([u for u in users.values() if not u.get('is_admin', False)])
    total_posts = len(posts)
    total_admins = len([u for u in users.values() if u.get('is_admin', False)])
    
    # Recent users (last 5)
    recent_users = sorted(
        [u for u in users.values() if not u.get('is_admin', False)], 
        key=lambda x: x['id'], 
        reverse=True
    )[:5]
    
    # Recent posts (last 5)
    recent_posts = sorted(posts, key=lambda x: x['timestamp'], reverse=True)[:5]
    
    stats = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_admins': total_admins,
        'recent_users': recent_users,
        'recent_posts': recent_posts
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin user management"""
    # Get all non-admin users
    all_users = [u for u in users.values() if not u.get('is_admin', False)]
    all_users.sort(key=lambda x: x['id'], reverse=True)
    
    return render_template('admin/users.html', users=all_users)

@app.route('/admin/posts')
@admin_required
def admin_posts():
    """Admin post management"""
    # Get all posts with user info
    all_posts = []
    for post in posts:
        post_with_user = post.copy()
        post_with_user['user'] = users.get(post['user_id'], {})
        all_posts.append(post_with_user)
    
    all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('admin/posts.html', posts=all_posts)

@app.route('/admin/delete_post/<int:post_id>', methods=['POST'])
@admin_required
def admin_delete_post(post_id):
    """Delete a post (admin only)"""
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('admin_posts'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete a user and their posts (admin only)"""
    global posts
    
    if user_id in users and not users[user_id].get('is_admin', False):
        # Delete user's posts
        posts = [p for p in posts if p['user_id'] != user_id]
        
        # Delete user
        del users[user_id]
        
        flash('User and their posts deleted successfully.', 'success')
    else:
        flash('Cannot delete admin users or user not found.', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/make_admin/<int:user_id>', methods=['POST'])
@admin_required
def admin_make_admin(user_id):
    """Make a user an admin"""
    if user_id in users:
        users[user_id]['is_admin'] = True
        flash(f'{users[user_id]["name"]} is now an administrator.', 'success')
    else:
        flash('User not found.', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/settings')
@admin_required
def admin_settings():
    """Admin settings page"""
    return render_template('admin/settings.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
