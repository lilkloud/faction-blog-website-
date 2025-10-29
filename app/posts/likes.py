from flask import jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from . import posts_bp
from ..models import Post, Like, db

@posts_bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if user already liked the post
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if like:
        # Unlike the post
        db.session.delete(like)
        db.session.commit()
        liked = False
    else:
        # Like the post
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        liked = True
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
    flash('Post liked!', 'success' if liked else 'info')
    return redirect(url_for('posts.post', post_id=post.id))

@posts_bp.route('/post/<int:post_id>/likes')
def post_likes(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    likes = post.likes.order_by(Like.timestamp.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return jsonify({
        'likes_count': likes.total,
        'likes': [{
            'username': like.user.username,
            'profile_url': url_for('user.profile', username=like.user.username),
            'avatar_url': url_for('static', filename=f'profile_pics/{like.user.image_file}'),
            'timestamp': like.timestamp.isoformat()
        } for like in likes.items]
    })
