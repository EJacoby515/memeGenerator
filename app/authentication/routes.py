from app.forms import UserLoginForm, SignInForm, SignUpForm
from app.models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            print(email, password)

            user = User(email, first_name, last_name, password=password)

            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.profile'))
    except Exception as e:
        print(f"Signup Error: {str(e)}")
        raise Exception('Invalid form data: Please check your form')

    return render_template('sign_up.html', form=form, signup=True)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(f"Attempting to sign in with  email: {email}")

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                print(f"Sign in successful. User {logged_user}")
                login_user(logged_user)
                print('Sign in successful')
                flash('You were successful in your initiation. Congratulations, and welcome to the Jedi Knights', 'auth-sucess')
                return redirect(url_for('site.profile'))
            else:
                print("Sign in Failed")
                flash('You have failed in your attempt to access this content', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except Exception as e:
        print(f"Signin Error: {str(e)}")
        raise Exception('Invalid Form Data: Please Check your Form')
    
    print("rendering sign_in.html")
    return render_template('sign_in.html', form=form, signup=False)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))