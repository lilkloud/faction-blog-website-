from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.models import Post, Message
from app import db
from sqlalchemy import or_, and_, not_
from datetime import datetime

main = Blueprint('main', __name__)

# Home/Portfolio Route
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    # Get featured posts for the carousel/slider
    featured_posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    # Get latest posts for the blog section
    latest_posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    
    return render_template('home.html',
                         featured_posts=featured_posts,
                         posts=latest_posts,
                         title='Home')

# Blog Route
@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('blog.html', posts=posts, title='Blog')

# About Route
@main.route("/about")
def about():
    return render_template('about.html', title='About')

# Projects Route
@main.route("/projects")
def projects():
    return render_template('projects.html', title='Projects')

# Contact Form Submission
@main.route("/contact", methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Create new message
        new_message = Message(
            name=name,
            email=email,
            subject=subject,
            message=message,
            date_received=datetime.utcnow()
        )
        
        # Save to database
        db.session.add(new_message)
        db.session.commit()
        
        # Here you would typically send an email notification
        # send_contact_email(name, email, subject, message)
        
        return jsonify({'success': True, 'message': 'Your message has been sent successfully!'})
    
    return jsonify({'success': False, 'message': 'Invalid request'}), 400

# Category Route
@main.route('/category/<string:category_name>')
def category(category_name):
    page = request.args.get('page', 1, type=int)
    try:
        # Use a more explicit query with proper SQLAlchemy syntax
        from sqlalchemy import text
        posts = db.session.query(Post).filter(text("post.category = :category")).params(category=category_name).order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
        return render_template('category.html', title=f'Category: {category_name}', posts=posts, category_name=category_name)
    except Exception as e:
        print(f"Error in category route: {str(e)}")
        return str(e), 500

# Blog Post Route
@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# Delete Post Route
@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.blog'))
