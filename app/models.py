from app import db
import datetime


class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Comment.alta)')

    def __repr__(self):
        return '{} {} {} {}'.format(self.title, self.content, self.id, self.user_id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_post_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def get_all():
        return Post.query.all()


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    alta = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, usuario_id, post_id, comentario):
        self.usuario_id = usuario_id
        self.post_id = post_id
        self.comentario = comentario

    def __repr__(self):
        return 'Comentario: {}'.format(self.comentario)

    def save(self):
        if not self.id:
            print('self -->', self.id, self.usuario_id, self.post_id, self.comentario)
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_comment_id(comment_id):
        return Comment.query.get(comment_id)

    @staticmethod
    def get_all_comments():
        return Comment.query.all()



