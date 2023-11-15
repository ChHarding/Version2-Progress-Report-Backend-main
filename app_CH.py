from flask import Flask, render_template, request
import pandas as pd
import stripe
import os

from keys import SECRET_KEY, PUBLISHABLE_KEY

#stripe.api_key = stripe_keys['secret_key']
stripe.api_key = SECRET_KEY

app = Flask(__name__, template_folder='Templates/E-commerce Website Template',
                      static_folder='Templates/E-commerce Website Template')

# Load the cleaned data into a pandas dataframe
df = pd.read_excel('ecommerce_clothing.xlsx') # CH this started with /  !!!!

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search query and filter values from the form
        search_query = request.form['search_query']
        max_price = request.form['max_price']
        min_rating = request.form['min_rating']
        
        # Filter the dataframe based on the search query and filter values
        filtered_df = df[df['product_name'].str.contains(search_query, case=False)]
        if max_price:
            filtered_df = filtered_df[filtered_df['price'] <= float(max_price)]
        if min_rating:
            filtered_df = filtered_df[filtered_df['average_review_rating'] >= float(min_rating)]
        
        # Render the template with the filtered dataframe (sorted by rating and price)
        filtered_df = filtered_df.sort_values(['average_review_rating', 'price'], ascending=[False, True])
        return render_template('index.html', products=filtered_df.to_dict('records'))
    else:
        # Render the template with no dataframe at the start
        return render_template('index.html')
    

# CH Why another / index() route? 
#@app.route('/')
#def index():
#    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)


if __name__ == '__main__':
    app.run(debug=False)

''' How to make files in images, css and js in index.html work:

<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/flag-uk.png') }}" alt="UK Flag">

url_for('static'  will figure out where that css folder is based on the value of static_folder in the app object.
'''