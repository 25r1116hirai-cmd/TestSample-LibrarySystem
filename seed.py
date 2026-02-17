from app import create_app
from app.db import get_db
from werkzeug.security import generate_password_hash

app = create_app()
#sqlファイルを読み込んで実行
with app.app_context():
    db = get_db()
    
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # 1. ユーザーデータの初期化
    db.execute('DELETE FROM user')
    db.execute('DELETE FROM sqlite_sequence WHERE name="user"')

    # 2. 初期ユーザーの追加
    users = [
        ('admin', 'adminpass', 'admin'),
        ('user01', 'password', 'user'),
        ('user02', 'password', 'user'),
    ]
    
    for username, password, role in users:
        db.execute(
            'INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), role)
        )
        
    # 3. 書籍データの初期化
    db.execute('DELETE FROM book')
    db.execute('DELETE FROM sqlite_sequence WHERE name="book"')
    
    # 4. 初期書籍データの投入
    books = [
        ('Python入門', '978-4-0000-0001-1', 'Guido', 'OReilly', 5),
        ('Flask Web開発', '978-4-0000-0002-8', 'Miguel', 'OReilly', 3),
        ('SQLアンチパターン', '978-4-0000-0003-5', 'Bill', 'OReilly', 2),
        ('リーダブルコード', '978-4-0000-0004-2', 'Boswell', 'OReilly', 0), # 在庫0件のケース
        ('人月の神話', '978-4-0000-0005-9', 'Brooks', 'Pearson', 1),
        ('達人プログラマー', '978-4-0000-0006-6', 'Andrew', 'Ohmsha', 2),
        ('Clean Code', '978-4-0000-0007-3', 'Martin', 'Pearson', 2),
        ('テスト駆動開発', '978-4-0000-0008-0', 'Kent', 'Ohmsha', 2),
    ]

    for title, isbn, author, publisher, stock in books:
        db.execute(
            'INSERT INTO book (title, isbn, author, publisher, stock_count) VALUES (?, ?, ?, ?, ?)',
            (title, isbn, author, publisher, stock)
        )
        
    # 5. 貸出記録の初期化
    db.execute('DELETE FROM loan')
    db.execute('DELETE FROM sqlite_sequence WHERE name="loan"')

from datetime import datetime, timedelta
    now = datetime.now()

    # テスト用データ案
    # user01: 現在9冊貸出中（あと1冊借りられるかテスト用）
    for i in range(1, 10):
        db.execute(
            'INSERT INTO loan (user_id, book_id, loan_date, return_deadline) VALUES (?, ?, ?, ?)',
            (2, i, now.strftime('%Y-%m-%d %H:%M:%S'), (now + timedelta(days=14)).strftime('%Y-%m-%d'))
        )

    # user02: 3年以上前の古い履歴（削除バッチのテスト用）
    three_years_ago = now - timedelta(days=365 * 3 + 10)
    db.execute(
        'INSERT INTO loan (user_id, book_id, loan_date, return_deadline, return_date) VALUES (?, ?, ?, ?, ?)',
        (3, 1, three_years_ago.strftime('%Y-%m-%d %H:%M:%S'), '2022-01-01', '2022-01-10')
    )
    
    db.commit()
    print("初期データの投入が完了しました。")
