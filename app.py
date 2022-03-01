from projectCode import create


"""
三种配置模式
    "development"
    "production"
    "test"
"""

app = create("development")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4000)
