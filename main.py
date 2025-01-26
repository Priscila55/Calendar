from website import create_app

app = create_app()

# only if we run the file we will execute the line below
if __name__ == '__main__':
    app.run(debug=True) # run flask application
    
    

