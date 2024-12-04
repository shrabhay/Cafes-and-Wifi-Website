from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
import random
from flask_bootstrap import Bootstrap5
from forms import AddNewCafe, SearchCafeForm, EditCafe
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('Flask_Secret_Key')
bootstrap = Bootstrap5(app)

db = sqlite3.connect('cafes.db')
cursor = db.cursor()

# cursor.execute("CREATE TABLE cafes ("
#                "id INTEGER PRIMARY KEY NOT NULL,"
#                "name VARCHAR(500) UNIQUE NOT NULL,"
#                "map_url VARCHAR(500) NOT NULL,"
#                "img_url VARCHAR(500) NOT NULL,"
#                "location VARCHAR(500) NOT NULL,"
#                "has_sockets BOOLEAN NOT NULL,"
#                "has_toilet BOOLEAN NOT NULL,"
#                "has_wifi BOOLEAN NOT NULL,"
#                "can_take_calls BOOLEAN NOT NULL,"
#                "seats VARCHAR(100) NOT NULL,"
#                "coffee_price VARCHAR(100) NOT NULL)")

query = """
INSERT INTO cafes (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats,
coffee_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

#
# cursor.execute(query, (
#     'FORA Borough',
#     'https://g.page/fora---borough?share',
#     'https://lh3.googleusercontent.com/p/AF1QipOhkJk2MBtFW1RydPU0zf3bf8upGkTQWyhDpXzZ=s0',
#     'Borough', 1, 0, 1, 1, '20-30', '£2.40'
# ))
# db.commit()


def to_dict(data):
    data_dict = {
        'id': data[0],
        'name': data[1],
        'map_url': data[2],
        'img_url': data[3],
        'location': data[4],
        'has_sockets': data[5],
        'has_toilet': data[6],
        'has_wifi': data[7],
        'can_take_calls': data[8],
        'seats': data[9],
        'coffee_price': data[10]
    }
    return data_dict


@app.route('/')
def home():
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes')
    all_cafes = cur.fetchall()
    return render_template("index.html", cafes=all_cafes)


@app.route('/random')
def get_random_cafe():
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes')
    all_cafes = cur.fetchall()
    random_cafe = random.choice(all_cafes)
    cur.close()
    conn.close()
    return render_template('random.html', cafe=random_cafe)


@app.route('/random-cafe-api')
def get_random_cafe_api():
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes')
    all_cafes = cur.fetchall()
    random_cafe = random.choice(all_cafes)
    cur.close()
    conn.close()
    return jsonify(cafe=to_dict(data=random_cafe))


@app.route('/all')
def get_all_cafes():
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes')
    all_cafes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cafes=[to_dict(data=cafe) for cafe in all_cafes])


@app.route('/search', methods=['GET', 'POST'])
def get_cafes_at_location():
    search_cafe = SearchCafeForm()
    cafes_at_location = None
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    if search_cafe.validate_on_submit():
        search_location = search_cafe.location.data
        cur.execute('SELECT * FROM cafes WHERE location = ?', (search_location,))
        cafes_at_location = cur.fetchall()
        cur.close()
        conn.close()
    return render_template('search_by_location.html', cafes=cafes_at_location, form=search_cafe)


@app.route('/search-cafe-api')
def get_cafes_at_location_api():
    query_location = request.args.get('loc')
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes WHERE location = ?', (query_location,))
    cafes_at_location = cur.fetchall()
    cur.close()
    conn.close()

    if cafes_at_location:
        return jsonify(cafes=[to_dict(data=cafe) for cafe in cafes_at_location])
    else:
        return jsonify(error={
            'Not found': "Sorry, we don't have a cafe at that location."
        }), 404


@app.route('/add', methods=['GET', 'POST'])
def add_new_cafe():
    add_cafe = AddNewCafe()
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    if add_cafe.validate_on_submit():
        name = add_cafe.name.data
        map_url = add_cafe.map_url.data
        img_url = add_cafe.image_url.data
        location = add_cafe.location.data
        has_sockets = '1' if add_cafe.has_sockets.data == 'Yes' else '0'
        has_toilet = '1' if add_cafe.has_toilet.data == 'Yes' else '0'
        has_wifi = '1' if add_cafe.has_wifi.data == 'Yes' else '0'
        can_take_calls = '1' if add_cafe.can_take_calls.data == 'Yes' else '0'
        seats = add_cafe.seats.data
        coffee_price = add_cafe.coffee_price.data

        cur.execute(query, (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi,
                            can_take_calls, seats, coffee_price))
        conn.commit()
        cur.close()
        conn.close()
        add_another_cafe = AddNewCafe()
        return render_template('add_cafe.html', form_submitted=True, form=add_another_cafe)
    return render_template('add_cafe.html', form=add_cafe)


@app.route('/add-cafe-api', methods=['GET', 'POST'])
def add_new_cafe_api():
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        map_url = request.form.get('map_url')
        img_url = request.form.get('img_url')
        location = request.form.get('location')
        has_sockets = request.form.get('has_sockets')
        has_toilet = request.form.get('has_toilet')
        has_wifi = request.form.get('has_wifi')
        can_take_calls = request.form.get('can_take_calls')
        seats = request.form.get('seats')
        coffee_price = request.form.get('coffee_price')

        cur.execute(query, (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi,
                            can_take_calls, seats, coffee_price))
        conn.commit()
    cur.close()
    conn.close()

    return jsonify(response={
        'Success': 'Successfully added the new cafe.'
    })


@app.route('/edit-cafe/<int:cafe_id>', methods=['GET', 'POST', 'PATCH'])
def edit_cafe(cafe_id):
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes WHERE id = ?', (cafe_id,))
    cafe = cur.fetchone()

    if cafe:
        cafe_values = {
            'name': cafe[1],
            'map_url': cafe[2],
            'image_url': cafe[3],
            'location': cafe[4],
            'has_sockets': 'Yes' if cafe[5] == '1' else 'No',
            'has_toilet': 'Yes' if cafe[6] == '1' else 'No',
            'has_wifi': 'Yes' if cafe[7] == '1' else 'No',
            'can_take_calls': 'Yes' if cafe[8] == '1' else 'No',
            'seats': cafe[9],
            'coffee_price': cafe[10]
        }
        edit_cafe_values = EditCafe(**cafe_values)

        if edit_cafe_values.validate_on_submit():
            new_name = edit_cafe_values.name.data
            new_map_url = edit_cafe_values.map_url.data
            new_img_url = edit_cafe_values.image_url.data
            new_location = edit_cafe_values.location.data
            new_has_sockets = '1' if edit_cafe_values.has_sockets.data == 'Yes' else '0'
            new_has_toilet = '1' if edit_cafe_values.has_toilet.data == 'Yes' else '0'
            new_has_wifi = '1' if edit_cafe_values.has_wifi.data == 'Yes' else '0'
            new_can_take_calls = '1' if edit_cafe_values.can_take_calls.data == 'Yes' else '0'
            new_seats = edit_cafe_values.seats.data
            new_coffee_price = edit_cafe_values.coffee_price.data

            cur.execute('UPDATE cafes SET name = ? WHERE id = ?', (new_name, cafe_id))
            cur.execute('UPDATE cafes SET map_url = ? WHERE id = ?', (new_map_url, cafe_id))
            cur.execute('UPDATE cafes SET img_url = ? WHERE id = ?', (new_img_url, cafe_id))
            cur.execute('UPDATE cafes SET location = ? WHERE id = ?', (new_location, cafe_id))
            cur.execute('UPDATE cafes SET has_sockets = ? WHERE id = ?', (new_has_sockets, cafe_id))
            cur.execute('UPDATE cafes SET has_toilet = ? WHERE id = ?', (new_has_toilet, cafe_id))
            cur.execute('UPDATE cafes SET has_wifi = ? WHERE id = ?', (new_has_wifi, cafe_id))
            cur.execute('UPDATE cafes SET can_take_calls = ? WHERE id = ?', (new_can_take_calls, cafe_id))
            cur.execute('UPDATE cafes SET seats = ? WHERE id = ?', (new_seats, cafe_id))
            cur.execute('UPDATE cafes SET coffee_price = ? WHERE id = ?', (new_coffee_price, cafe_id))
            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('home'))
        return render_template('edit_cafe.html', form=edit_cafe_values)


@app.route('/report_closed/<int:cafe_id>', methods=['GET', 'POST', 'DELETE'])
def delete_cafe(cafe_id):
    conn = sqlite3.connect('cafes.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM cafes WHERE id = ?', (cafe_id,))
    cafe = cur.fetchone()

    if cafe:
        cur.execute('DELETE FROM cafes WHERE id = ?', (cafe_id,))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
