from app import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application
    app.run(debug=True)
