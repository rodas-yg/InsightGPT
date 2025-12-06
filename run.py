from app import create_app

# Creates and runs the Flask application instance.
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
