#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import random
import string

import services
import models

class UserRegister(tornado.web.RequestHandler):
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")

        salt = generate_salt()
        hashed_password = hash_password(password, salt)
        api_key = generate_api_key()

        user = {
            "email": email,
            "password": hashed_password,
            "salt": salt,
            "api_key": api_key,
        }

        users_collection.insert_one(user)

        send_email(email, "Registration Successful", f"Your API key is: {api_key}")

        self.write({"message": "Registration successful"})


class UserReset(tornado.web.RequestHandler):
    def post(self):
        email = self.get_argument("email")

        user = users_collection.find_one({"email": email})

        if user:
            new_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=16)
            )
            new_salt = generate_salt()
            new_hashed_password = hash_password(new_password, new_salt)

            users_collection.update_one(
                {"email": email},
                {"$set": {"password": new_hashed_password, "salt": new_salt}},
            )

            send_email(email, "Password Reset", f"Your new password is: {new_password}")

            self.write({"message": "Password reset successful"})
        else:
            self.write({"message": "User not found"}, status=404)


class SearchBooksHandler(tornado.web.RequestHandler):
    def get(self):
        title = self.get_argument("title")

        results = books_collection.find({"$text": {"$search": title}}).limit(10)

        books = []
        for book in results:
            books.append(book)

        self.write({"books": books})


class UserUpload(tornado.web.RequestHandler):
    def post(self):
        user_id = self.get_argument("user_id")
        file = self.request.files["file"][0]

        with open(f"/user/{user_id}/metadata.db", "wb") as f:
            f.write(file["body"])

        self.write({"message": "File uploaded successfully"})

        # 执行 merge_service() 服务
        # 假设 merge_service() 是一个异步函数
        tornado.ioloop.IOLoop.current().spawn_callback(merge_service)
