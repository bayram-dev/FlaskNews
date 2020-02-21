#TODO
# 1) Доделать query в /news
# 2) Добавить минимальный CSS во все старницы
# 3) Проверить подклюение через телефон
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from datetime import datetime
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Todo(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	Title = db.Column(db.String(200), nullable=False)
	Content = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
class Users(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	rank = db.Column(db.String(200), nullable=True)
				

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		news_title = request.form['title']
		news_content = request.form['content']
		if len(news_title) < 1:
			return "Title cant be empty"
		elif len(news_content) < 1:
			return "Content cant be empty"
		else:
			some_new_news = Todo(Title=news_title, Content=news_content)
			try:
				db.session.add(some_new_news)
				db.session.commit()
				return redirect('/')
			except:
				return "Something went wrong! Check out your logs"
	else:
		all_news = Todo.query.order_by(Todo.date_created).all()
		return render_template('index.html', news=all_news)
@app.route('/news/<int:news_id>')
def news(news_id):
	try:
		news = Todo.query.get(news_id)
		html_things = ("<br>", "<br><br>")
		main_content = news.Content.format(html_things)
		return render_template('news.html', news=news, content=main_content)
		session.close()
	except:
		return "Something went wrong!"
@app.route('/delete/<int:news_id>')
def delete(news_id):
	news_to_delete = Todo.query.get_or_404(news_id)
	try:
		db.session.delete(news_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return "Something went wrong"

@app.route('/update/<int:news_id>', methods=['GET', 'POST'])
def update(news_id):
	news = Todo.query.get_or_404(news_id)
	if request.method == 'POST':
		news.Title = request.form['title']
		news.Content = request.form['content']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "There was an issue updating this news"
	else:
		return render_template('update.html', news=news)
if __name__ == "__main__":
    app.run(debug=True)

