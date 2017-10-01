from app import create_app
import sys

app = create_app(sys.argv[1])

if __name__ == '__main__':
    app.run()
