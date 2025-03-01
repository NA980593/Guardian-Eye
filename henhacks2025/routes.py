from flask import render_template, url_for, flash, redirect
from henhacks2025 import app, db, bcrypt

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RestrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)