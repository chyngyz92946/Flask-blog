from flask import Blueprint, render_template, request
from flask import redirect, url_for

from flask_security import login_required

from models import Post, Tag
from .forms import PostForm
from app import db

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		try:
			post = Post(title=title, content=content)
			db.session.add(post)
			db.session.commit()

		except Exception as e:
			print(e)

		return redirect(url_for('posts.index'))

	else:
		form = PostForm()
		args = {
			"form": form
		}
		return render_template('posts/create_post.html', args=args)

@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
	post = Post.query.filter(Post.slug == slug).first_or_404()

	if request.method == 'POST':
		form = PostForm(formdata=request.form, obj=post)
		form.populate_obj(post)
		db.session.commit()

		return redirect(url_for('posts.post_detail', slug=post.slug))
	else:

		form = PostForm(obj=post)
		args = {
			"post": post,
			"form": form
		}
		return render_template('posts/edit_post.html', args=args)


@posts.route('/')
def index():
	q = request.args.get('q')

	page = request.args.get('page')

	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	if q:
		posts = Post.query.filter(Post.title.contains(q) | Post.content.contains(q))
	else:
		posts = Post.query.order_by(Post.create_date.desc())

	pages = posts.paginate(page=page, per_page=5)

	args = {
		"pages": pages
	}
	return render_template('posts/index.html', args=args)


@posts.route('/<slug>')
def post_detail(slug):
	post = Post.query.filter(Post.slug == slug).first_or_404()
	tags = post.tags
	args = {
		"post": post,
		"tags": tags
	}
	return render_template('posts/post_detail.html', args=args)


@posts.route('/tag/<slug>')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first_or_404()
	posts = tag.posts.all()
	args = {
		"tag": tag,
		"posts": posts
	}
	return render_template('posts/tag_detail.html', args=args)
