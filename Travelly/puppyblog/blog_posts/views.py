from puppyblog import render_template,url_for,flash,\
    request,redirect, Blueprint,current_user,login_required,db
from puppyblog.blog_posts.models import Blogpost
from puppyblog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts',__name__)

#Blog Create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = Blogpost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()

        flash('New Blog POST Created')

        return redirect(url_for('core.index'),flash=flash)

    return render_template('createpost.html',form=form)

#Blog VIew

@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    return render_template('blogpost.html',title=blog_post.title,
                           date=blog_post.date,post=blog_post)


@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def blog_update(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    #print (blog_post.text)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()


    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        print (blog_post)

        print ("in here")
        db.session.commit()

        flash('Blog POST Updated')

        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post_id,flash=flash))

    elif request.method == 'GET':

        blog_post.title = blog_post.title
        blog_post.text = blog_post.text

    return render_template('updatepost.html',title='Updating',form=form,blog_post=blog_post,flash=form.errors)



#Blog Delete

@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def blog_delete(blog_post_id):

    blog_post = Blogpost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash ('Blog Post Deleted')

    return redirect(url_for('core.index'))
