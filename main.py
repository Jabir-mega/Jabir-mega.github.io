from website import create_app # IMPORTS create_app function from the website package

app = create_app() # creates an instance of the Flask app by calling the create_app function
# This is the main entry point of the application, where the Flask app is created and run.
# The create_app function initializes the Flask app, sets up the database, and registers blueprints for routing.
# The app instance is created and can be used to define routes, handle requests, and manage the application lifecycle.

if __name__ == '__main__': #makes sure that the web server only runs if this file is run hence the condition  
    app.run(debug=True) # debug is true ensures the whole is rerun after everychamges rather than us doing manually although not recommended when in production
    